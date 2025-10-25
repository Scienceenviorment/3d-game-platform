#!/usr/bin/env python3
"""
Echoes of the Horizon - Simple Ancient Bharat Server
Complete 3D multiplayer game in a single Python file
No Git, no complexity, just pure Ancient Bharat adventure!

Requirements: Python 3.8+ and just 3 packages (auto-installed)
- pip install fastapi uvicorn websockets
"""

# Standard Python library imports (built-in, no installation needed)
import json
import time
import math
import random
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum
from pathlib import Path

# Third-party imports (will be auto-installed)
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError:
    print("📦 Installing required packages...")
    import subprocess
    import sys
    
    packages = ["fastapi", "uvicorn[standard]", "websockets"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✅ Packages installed! Please restart the script.")
    sys.exit(0)


# ============================================================================
# GAME DATA STRUCTURES (Python dataclasses - simple and clean)
# ============================================================================

class Region(Enum):
    """The five mystical regions of Ancient Bharat"""
    DUST_PLAINS = "dust_plains"          # Desert with ancient ruins
    HIMALAYAN_PEAKS = "himalayan_peaks"  # Mountains with monasteries
    INDRAPURA_CITY = "indrapura_city"    # Cultural center with NPCs
    NARMADA_FOREST = "narmada_forest"    # Sacred forest with spirits
    OCEAN_FRONTIER = "ocean_frontier"    # Starting coastal region


@dataclass
class Position:
    """3D position in the world"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Player:
    """Player information and progress"""
    player_id: str                       # Unique player identifier
    name: str                            # Display name
    position: Position                   # Current 3D position
    current_region: Region = Region.OCEAN_FRONTIER  # Current region
    websocket: Optional[WebSocket] = None  # WebSocket connection
    
    # Player progression
    level: int = 1                       # Player level
    experience: int = 0                  # Experience points
    regions_visited: List[str] = None    # Regions discovered
    quests_completed: List[str] = None   # Completed quests
    last_active: float = 0.0            # Last activity timestamp
    
    def __post_init__(self):
        """Initialize default lists"""
        if self.regions_visited is None:
            self.regions_visited = ["ocean_frontier"]
        if self.quests_completed is None:
            self.quests_completed = []


@dataclass
class NPC:
    """Non-Player Character with personality"""
    npc_id: str                          # Unique NPC identifier
    name: str                            # Display name
    sanskrit_name: str                   # Sanskrit name
    title: str                           # Job/role title
    region: Region                       # Home region
    
    # Personality and dialogue
    personality: str                     # Personality type
    greeting: str                        # First meeting greeting
    quest_dialogue: str                  # Quest-related dialogue
    wisdom_quotes: List[str]            # Random wisdom quotes
    
    # Schedule and availability
    daily_schedule: Dict[str, str]      # Time-based activities
    reputation_threshold: int = 0        # Reputation needed to access


@dataclass
class Quest:
    """Game quest with objectives"""
    quest_id: str                        # Unique quest identifier
    title: str                           # Quest display title
    description: str                     # Quest description
    giver_npc: str                      # Which NPC gives this quest
    objectives: List[str]               # List of objective descriptions
    completion_message: str             # Message when quest completed
    
    # Quest requirements and rewards
    level_required: int = 1              # Minimum player level
    region_required: str = ""            # Required region (empty = any)
    experience_reward: int = 100         # XP reward for completion


# ============================================================================
# GAME DATA (All NPCs, Quests, and World Info)
# ============================================================================

# Ancient Bharat NPCs with cultural authenticity
GAME_NPCS = {
    "veda_scholar_arunima": NPC(
        npc_id="veda_scholar_arunima",
        name="Arunima",
        sanskrit_name="अरुणिमा (Aruṇimā)",
        title="Veda Scholar",
        region=Region.INDRAPURA_CITY,
        personality="wise_teacher",
        greeting="Welcome, seeker of knowledge. I am Arunima, keeper of ancient wisdom.",
        quest_dialogue="The Sarasvati Map fragments hold the key to our lost heritage. Will you help recover them?",
        wisdom_quotes=[
            "यत्र नार्यस्तु पूज्यन्ते रमन्ते तत्र देवताः - Where women are honored, there the gods are pleased.",
            "विद्या ददाति विनयं - Knowledge gives humility.",
            "सत्यमेव जयते - Truth alone triumphs."
        ],
        daily_schedule={
            "morning": "Studying ancient texts in the Temple of Knowledge",
            "afternoon": "Teaching students about Vedic traditions", 
            "evening": "Meditating and offering prayers at sunset"
        },
        reputation_threshold=0
    ),
    
    "ranger_devraj": NPC(
        npc_id="ranger_devraj",
        name="Devraj",
        sanskrit_name="देवराज (Devarāja)",
        title="Forest Ranger",
        region=Region.NARMADA_FOREST,
        personality="practical_guide",
        greeting="Greetings, traveler! I'm Devraj. The wilderness has much to teach those who listen.",
        quest_dialogue="The forest paths are dangerous but rewarding. Let me teach you survival skills.",
        wisdom_quotes=[
            "वसुधैव कुटुम्बकम् - The world is one family.",
            "Nature is the best teacher for those who observe carefully.",
            "Every tree has a story, every path has wisdom."
        ],
        daily_schedule={
            "morning": "Patrolling forest boundaries and checking animal tracks",
            "afternoon": "Resting in the shade and maintaining equipment",
            "evening": "Teaching wilderness skills to visitors"
        },
        reputation_threshold=0
    ),
    
    "village_elder_rukmini": NPC(
        npc_id="village_elder_rukmini",
        name="Rukmini",
        sanskrit_name="रुक्मिणी (Rukmiṇī)",
        title="Village Elder",
        region=Region.INDRAPURA_CITY,
        personality="nurturing_elder",
        greeting="Namaste, child. I am Rukmini, elder of this village. How may I assist you?",
        quest_dialogue="Our village needs help preserving traditions. Would you learn our ancient ways?",
        wisdom_quotes=[
            "गुरुर्ब्रह्मा गुरुर्विष्णु - The teacher is Brahma, the teacher is Vishnu.",
            "Tradition is the bridge between past and future.",
            "Every craft tells the story of our ancestors."
        ],
        daily_schedule={
            "morning": "Overseeing village activities and resolving disputes",
            "afternoon": "Teaching traditional crafts to young villagers",
            "evening": "Sharing stories and wisdom with the community"
        },
        reputation_threshold=0
    )
}

# Game Quests with cultural themes
GAME_QUESTS = {
    "main_sarasvati_map": Quest(
        quest_id="main_sarasvati_map",
        title="The Lost Sarasvati Map",
        description="Discover the seven fragments of the ancient Sarasvati Map scattered across Ancient Bharat.",
        giver_npc="veda_scholar_arunima",
        level_required=1,
        region_required="",
        experience_reward=1000,
        objectives=[
            "Speak with Arunima about the Sarasvati Map legend",
            "Visit all five regions of Ancient Bharat",
            "Find ancient fragment sites in each region",
            "Collect all seven map fragments",
            "Return to Arunima with the complete map"
        ],
        completion_message="The Sarasvati Map is complete! You have helped preserve ancient knowledge."
    ),
    
    "wilderness_training": Quest(
        quest_id="wilderness_training", 
        title="Paths of the Forest",
        description="Learn wilderness survival skills from Devraj the Ranger.",
        giver_npc="ranger_devraj",
        level_required=2,
        region_required="narmada_forest",
        experience_reward=250,
        objectives=[
            "Meet Devraj in Narmada Forest",
            "Learn to identify 5 different plant species", 
            "Practice tracking animal movements",
            "Navigate through unmarked forest paths",
            "Demonstrate survival skills to Devraj"
        ],
        completion_message="You have learned the ways of the forest. Nature will guide your path."
    ),
    
    "village_traditions": Quest(
        quest_id="village_traditions",
        title="Preserving Ancient Ways",
        description="Help Rukmini preserve traditional village crafts and customs.",
        giver_npc="village_elder_rukmini", 
        level_required=1,
        region_required="indrapura_city",
        experience_reward=200,
        objectives=[
            "Learn about traditional pottery techniques",
            "Help repair the village temple",
            "Participate in morning prayer ceremony",
            "Assist with community feast preparation",
            "Document village stories and customs"
        ],
        completion_message="The village traditions live on through your efforts. You honor our ancestors."
    ),
    
    "cultural_discovery": Quest(
        quest_id="cultural_discovery",
        title="Echoes of Ancient Wisdom", 
        description="Explore all regions and discover the cultural heritage of Ancient Bharat.",
        giver_npc="veda_scholar_arunima",
        level_required=3,
        region_required="",
        experience_reward=500,
        objectives=[
            "Visit sacred sites in each region",
            "Interact with all three key NPCs",
            "Learn about regional cultural differences",
            "Collect traditional stories and legends",
            "Share knowledge with other travelers"
        ],
        completion_message="You have become a bridge between cultures. Your journey spreads wisdom."
    )
}

# World regions with cultural information
REGION_INFO = {
    Region.DUST_PLAINS: {
        "name": "Dust Plains",
        "sanskrit_name": "धूलि प्रदेश (Dhūli Pradeśa)",
        "description": "Vast arid plains dotted with ancient ruins and archaeological mysteries.",
        "cultural_elements": ["Stone pillars with royal decrees", "Buddhist stupas", "Desert caravans"],
        "boundaries": {"x_min": -500, "x_max": -200, "z_min": -500, "z_max": 500}
    },
    Region.HIMALAYAN_PEAKS: {
        "name": "Himalayan Peaks", 
        "sanskrit_name": "हिमालय शिखर (Himālaya Śikhara)",
        "description": "Snow-capped mountains housing ancient monasteries and meditation caves.",
        "cultural_elements": ["Mountain monasteries", "Prayer flags", "Sacred caves"],
        "boundaries": {"x_min": -500, "x_max": 500, "z_min": 200, "z_max": 500}
    },
    Region.INDRAPURA_CITY: {
        "name": "Indrapura City",
        "sanskrit_name": "इन्द्रपुर नगर (Indrapura Nagara)",
        "description": "Bustling ancient city with grand temples, markets, and centers of learning.",
        "cultural_elements": ["Grand temples", "Scholarly libraries", "Traditional markets"],
        "boundaries": {"x_min": -200, "x_max": 200, "z_min": -100, "z_max": 200}
    },
    Region.NARMADA_FOREST: {
        "name": "Narmada Forest",
        "sanskrit_name": "नर्मदा वन (Narmadā Vana)",
        "description": "Dense sacred forest with ancient trees, hidden groves, and forest spirits.",
        "cultural_elements": ["Sacred groves", "Forest ashrams", "Ancient banyan trees"],
        "boundaries": {"x_min": -500, "x_max": 500, "z_min": -500, "z_max": -100}
    },
    Region.OCEAN_FRONTIER: {
        "name": "Ocean Frontier", 
        "sanskrit_name": "सागर सीमा (Sāgara Sīmā)",
        "description": "Coastal region with fishing villages, lighthouses, and maritime traditions.",
        "cultural_elements": ["Coastal temples", "Fishing boats", "Lighthouse"],
        "boundaries": {"x_min": 200, "x_max": 500, "z_min": -500, "z_max": 500}
    }
}


# ============================================================================
# GAME SERVER CLASS (All game logic in one place)
# ============================================================================

class SimpleAncientBharatServer:
    """Complete Ancient Bharat game server in one class"""
    
    def __init__(self):
        """Initialize the game server"""
        print("🏛️ Starting Echoes of the Horizon - Ancient Bharat Server")
        
        # Game state
        self.connected_players: Dict[str, Player] = {}
        self.chat_history: List[Dict] = []
        self.game_data_dir = Path("game_data")
        self.game_data_dir.mkdir(exist_ok=True)
        
        # Load persistent data
        self.load_game_data()
        
        print("✅ Game server initialized successfully")
    
    def determine_region(self, x: float, z: float) -> Region:
        """Determine which region contains the given coordinates"""
        for region, info in REGION_INFO.items():
            bounds = info["boundaries"]
            if (bounds["x_min"] <= x <= bounds["x_max"] and 
                bounds["z_min"] <= z <= bounds["z_max"]):
                return region
        
        # Default to Ocean Frontier if coordinates are outside all regions
        return Region.OCEAN_FRONTIER
    
    async def connect_player(self, websocket: WebSocket, player_id: str, player_name: str):
        """Handle new player connection"""
        try:
            await websocket.accept()
            
            # Load or create player data
            player_data = self.load_player_data(player_id)
            
            # Create player object
            player = Player(
                player_id=player_id,
                name=player_data.get("name", player_name),
                position=Position(**player_data.get("position", {"x": 0, "y": 0, "z": 0})),
                websocket=websocket,
                level=player_data.get("level", 1),
                experience=player_data.get("experience", 0),
                regions_visited=player_data.get("regions_visited", ["ocean_frontier"]),
                quests_completed=player_data.get("quests_completed", []),
                last_active=time.time()
            )
            
            # Update current region based on position
            player.current_region = self.determine_region(player.position.x, player.position.z)
            
            # Add to connected players
            self.connected_players[player_id] = player
            
            # Send welcome data
            welcome_message = {
                "type": "player_connected",
                "player_data": {
                    "player_id": player_id,
                    "name": player.name,
                    "position": asdict(player.position),
                    "current_region": player.current_region.value,
                    "level": player.level,
                    "experience": player.experience,
                    "regions_visited": player.regions_visited
                },
                "region_info": REGION_INFO[player.current_region],
                "available_npcs": self.get_region_npcs(player.current_region),
                "available_quests": self.get_available_quests(player_id),
                "chat_history": self.chat_history[-10:]  # Last 10 messages
            }
            
            await websocket.send_text(json.dumps(welcome_message))
            
            # Notify other players
            await self.broadcast_to_others(player_id, {
                "type": "player_joined",
                "player_id": player_id,
                "name": player.name,
                "current_region": player.current_region.value
            })
            
            print(f"🎮 Player {player.name} ({player_id}) connected in {player.current_region.value}")
            
        except Exception as e:
            print(f"❌ Error connecting player {player_id}: {e}")
    
    async def disconnect_player(self, player_id: str):
        """Handle player disconnection"""
        if player_id in self.connected_players:
            player = self.connected_players[player_id]
            
            # Save player data before disconnecting
            self.save_player_data(player)
            
            # Remove from connected players
            del self.connected_players[player_id]
            
            # Notify other players
            await self.broadcast_to_all({
                "type": "player_left",
                "player_id": player_id,
                "name": player.name
            })
            
            print(f"👋 Player {player.name} ({player_id}) disconnected")
    
    async def handle_player_movement(self, player_id: str, movement_data: dict):
        """Handle player movement with region detection"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        
        # Update position
        player.position.x = movement_data.get("x", player.position.x)
        player.position.y = movement_data.get("y", player.position.y)
        player.position.z = movement_data.get("z", player.position.z)
        player.last_active = time.time()
        
        # Check for region change
        new_region = self.determine_region(player.position.x, player.position.z)
        
        if new_region != player.current_region:
            old_region = player.current_region
            player.current_region = new_region
            
            # Add to visited regions if new
            region_name = new_region.value
            if region_name not in player.regions_visited:
                player.regions_visited.append(region_name)
                player.experience += 100  # Exploration reward
            
            # Send region change notification
            region_change_data = {
                "type": "region_changed",
                "old_region": old_region.value,
                "new_region": new_region.value,
                "region_info": REGION_INFO[new_region],
                "available_npcs": self.get_region_npcs(new_region),
                "experience_gained": 100 if region_name not in player.regions_visited else 0
            }
            await player.websocket.send_text(json.dumps(region_change_data))
        
        # Broadcast movement to other players
        await self.broadcast_to_others(player_id, {
            "type": "player_moved",
            "player_id": player_id,
            "position": asdict(player.position),
            "current_region": player.current_region.value
        })
    
    async def handle_chat_message(self, player_id: str, message_data: dict):
        """Handle chat messages"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        message = message_data.get("message", "").strip()
        
        if not message:
            return
        
        # Create chat message
        chat_message = {
            "type": "chat_message",
            "player_id": player_id,
            "player_name": player.name,
            "message": message,
            "timestamp": time.time(),
            "region": player.current_region.value
        }
        
        # Add to history (keep last 50 messages)
        self.chat_history.append(chat_message)
        if len(self.chat_history) > 50:
            self.chat_history.pop(0)
        
        # Broadcast to all players
        await self.broadcast_to_all(chat_message)
    
    async def handle_npc_interaction(self, player_id: str, interaction_data: dict):
        """Handle NPC interactions"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        npc_id = interaction_data.get("npc_id")
        
        if npc_id not in GAME_NPCS:
            return
        
        npc = GAME_NPCS[npc_id]
        
        # Check if NPC is in same region
        if npc.region != player.current_region:
            return
        
        # Get NPC response based on interaction type
        interaction_type = interaction_data.get("interaction_type", "greeting")
        
        if interaction_type == "greeting":
            response = npc.greeting
        elif interaction_type == "quest":
            response = npc.quest_dialogue
        elif interaction_type == "wisdom":
            response = random.choice(npc.wisdom_quotes)
        else:
            response = npc.greeting
        
        # Send NPC response
        npc_response = {
            "type": "npc_response",
            "npc_id": npc_id,
            "npc_name": npc.name,
            "npc_sanskrit_name": npc.sanskrit_name,
            "response": response,
            "available_quests": [q_id for q_id, quest in GAME_QUESTS.items() 
                               if quest.giver_npc == npc_id and q_id not in player.quests_completed]
        }
        
        await player.websocket.send_text(json.dumps(npc_response))
    
    async def handle_quest_action(self, player_id: str, quest_data: dict):
        """Handle quest-related actions"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        action = quest_data.get("action")
        quest_id = quest_data.get("quest_id")
        
        if quest_id not in GAME_QUESTS:
            return
        
        quest = GAME_QUESTS[quest_id]
        
        if action == "start":
            # Check requirements
            if (player.level >= quest.level_required and
                quest_id not in player.quests_completed and
                (not quest.region_required or quest.region_required == player.current_region.value)):
                
                # Award experience for starting quest
                player.experience += 25
                
                quest_response = {
                    "type": "quest_started", 
                    "quest": {
                        "quest_id": quest_id,
                        "title": quest.title,
                        "description": quest.description,
                        "objectives": quest.objectives,
                        "experience_reward": quest.experience_reward
                    },
                    "experience_gained": 25
                }
                
                await player.websocket.send_text(json.dumps(quest_response))
        
        elif action == "complete":
            # Complete quest (simplified - assume objectives met)
            if quest_id not in player.quests_completed:
                player.quests_completed.append(quest_id)
                player.experience += quest.experience_reward
                
                # Level up check (every 1000 XP)
                new_level = (player.experience // 1000) + 1
                level_up = new_level > player.level
                player.level = new_level
                
                quest_response = {
                    "type": "quest_completed",
                    "quest_id": quest_id,
                    "completion_message": quest.completion_message,
                    "experience_gained": quest.experience_reward,
                    "level_up": level_up,
                    "new_level": player.level if level_up else None
                }
                
                await player.websocket.send_text(json.dumps(quest_response))
    
    def get_region_npcs(self, region: Region) -> List[Dict]:
        """Get NPCs available in a specific region"""
        return [
            {
                "npc_id": npc.npc_id,
                "name": npc.name,
                "sanskrit_name": npc.sanskrit_name,
                "title": npc.title,
                "personality": npc.personality
            }
            for npc in GAME_NPCS.values()
            if npc.region == region
        ]
    
    def get_available_quests(self, player_id: str) -> List[Dict]:
        """Get quests available to a player"""
        if player_id not in self.connected_players:
            return []
        
        player = self.connected_players[player_id]
        
        available_quests = []
        for quest_id, quest in GAME_QUESTS.items():
            if (quest_id not in player.quests_completed and
                player.level >= quest.level_required and
                (not quest.region_required or quest.region_required == player.current_region.value)):
                
                available_quests.append({
                    "quest_id": quest_id,
                    "title": quest.title,
                    "description": quest.description,
                    "giver_npc": quest.giver_npc,
                    "experience_reward": quest.experience_reward
                })
        
        return available_quests
    
    async def broadcast_to_all(self, data: dict):
        """Broadcast message to all connected players"""
        message = json.dumps(data)
        disconnected = []
        
        for player_id, player in self.connected_players.items():
            try:
                await player.websocket.send_text(message)
            except:
                disconnected.append(player_id)
        
        # Clean up disconnected players
        for player_id in disconnected:
            await self.disconnect_player(player_id)
    
    async def broadcast_to_others(self, sender_id: str, data: dict):
        """Broadcast message to all players except sender"""
        message = json.dumps(data)
        disconnected = []
        
        for player_id, player in self.connected_players.items():
            if player_id != sender_id:
                try:
                    await player.websocket.send_text(message)
                except:
                    disconnected.append(player_id)
        
        # Clean up disconnected players
        for player_id in disconnected:
            await self.disconnect_player(player_id)
    
    def load_player_data(self, player_id: str) -> dict:
        """Load player data from file"""
        player_file = self.game_data_dir / f"player_{player_id}.json"
        
        if player_file.exists():
            try:
                with open(player_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Return default player data
        return {
            "name": f"Player_{player_id[:8]}",
            "position": {"x": 0, "y": 0, "z": 0},
            "level": 1,
            "experience": 0,
            "regions_visited": ["ocean_frontier"],
            "quests_completed": []
        }
    
    def save_player_data(self, player: Player):
        """Save player data to file"""
        player_file = self.game_data_dir / f"player_{player.player_id}.json"
        
        player_data = {
            "name": player.name,
            "position": asdict(player.position),
            "level": player.level,
            "experience": player.experience,
            "regions_visited": player.regions_visited,
            "quests_completed": player.quests_completed,
            "last_login": player.last_active
        }
        
        try:
            with open(player_file, 'w') as f:
                json.dump(player_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save player data: {e}")
    
    def load_game_data(self):
        """Load game state from files"""
        # Load chat history
        chat_file = self.game_data_dir / "chat_history.json"
        if chat_file.exists():
            try:
                with open(chat_file, 'r') as f:
                    self.chat_history = json.load(f)
            except:
                self.chat_history = []
    
    def save_game_data(self):
        """Save game state to files"""
        # Save chat history
        chat_file = self.game_data_dir / "chat_history.json"
        try:
            with open(chat_file, 'w') as f:
                json.dump(self.chat_history[-50:], f, indent=2)  # Keep last 50 messages
        except Exception as e:
            print(f"⚠️ Could not save chat history: {e}")
        
        # Save all connected player data
        for player in self.connected_players.values():
            self.save_player_data(player)
    
    async def handle_websocket_message(self, websocket: WebSocket, player_id: str):
        """Main WebSocket message handler"""
        try:
            while True:
                # Receive message
                data = await websocket.receive_text()
                message = json.loads(data)
                message_type = message.get("type")
                
                # Handle different message types
                if message_type == "movement":
                    await self.handle_player_movement(player_id, message)
                elif message_type == "chat":
                    await self.handle_chat_message(player_id, message)
                elif message_type == "npc_interaction":
                    await self.handle_npc_interaction(player_id, message)
                elif message_type == "quest_action":
                    await self.handle_quest_action(player_id, message)
                else:
                    print(f"⚠️ Unknown message type: {message_type}")
        
        except WebSocketDisconnect:
            await self.disconnect_player(player_id)
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
            await self.disconnect_player(player_id)
    
    def get_server_status(self) -> dict:
        """Get server status information"""
        return {
            "game_name": "Echoes of the Horizon - Ancient Bharat",
            "connected_players": len(self.connected_players),
            "regions": [region.value for region in Region],
            "total_npcs": len(GAME_NPCS),
            "total_quests": len(GAME_QUESTS),
            "players": [
                {
                    "name": player.name,
                    "level": player.level,
                    "region": player.current_region.value,
                    "experience": player.experience
                }
                for player in self.connected_players.values()
            ]
        }


# ============================================================================
# FASTAPI WEB SERVER SETUP
# ============================================================================

# Create game server instance
game_server = SimpleAncientBharatServer()

# Create FastAPI app
app = FastAPI(title="Echoes of the Horizon - Ancient Bharat")

# Add CORS for browser compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-save task
async def auto_save_task():
    """Save game data every 5 minutes"""
    while True:
        await asyncio.sleep(300)  # 5 minutes
        try:
            game_server.save_game_data()
            print(f"💾 Auto-save completed at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"❌ Auto-save error: {e}")

# ============================================================================
# WEB ENDPOINTS
# ============================================================================

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for player connections"""
    player_name = websocket.query_params.get("name", f"Player_{player_id[:8]}")
    
    # Connect player
    await game_server.connect_player(websocket, player_id, player_name)
    
    # Handle messages
    await game_server.handle_websocket_message(websocket, player_id)

@app.get("/")
async def root():
    """Server status page"""
    return game_server.get_server_status()

@app.get("/status")
async def server_status():
    """Detailed server status"""
    return game_server.get_server_status()

@app.get("/client")
async def game_client():
    """Serve the game client"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of the Horizon - Ancient Bharat</title>
    <style>
        body {
            margin: 0;
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #8B4513 0%, #D2B48C 100%);
            color: #8B4513;
            overflow: hidden;
        }
        
        .game-container {
            display: flex;
            height: 100vh;
        }
        
        .game-world {
            flex: 1;
            background: linear-gradient(180deg, #87CEEB 0%, #228B22 50%, #8B4513 100%);
            position: relative;
            overflow: hidden;
        }
        
        .ui-panel {
            width: 300px;
            background: rgba(139, 69, 19, 0.9);
            color: #F5DEB3;
            padding: 20px;
            overflow-y: auto;
            border-left: 3px solid #DAA520;
        }
        
        .region-display {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(139, 69, 19, 0.8);
            color: #F5DEB3;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #DAA520;
        }
        
        .player-avatar {
            position: absolute;
            width: 30px;
            height: 30px;
            background: #FF6B35;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            border: 3px solid #DAA520;
            box-shadow: 0 0 15px rgba(255, 107, 53, 0.6);
        }
        
        .chat-section {
            height: 200px;
            border: 2px solid #DAA520;
            margin-bottom: 15px;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
        }
        
        .chat-messages {
            height: 150px;
            overflow-y: auto;
            padding: 10px;
            font-size: 12px;
        }
        
        .chat-input {
            width: 100%;
            padding: 8px;
            background: rgba(0, 0, 0, 0.5);
            border: none;
            color: #F5DEB3;
            border-radius: 0 0 6px 6px;
        }
        
        .npc-section, .quest-section {
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            border: 2px solid #DAA520;
        }
        
        .npc-item, .quest-item {
            margin: 10px 0;
            padding: 10px;
            background: rgba(218, 165, 32, 0.2);
            border-radius: 5px;
            cursor: pointer;
            border: 1px solid #DAA520;
        }
        
        .npc-item:hover, .quest-item:hover {
            background: rgba(218, 165, 32, 0.4);
        }
        
        .player-info {
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            border: 2px solid #DAA520;
        }
        
        .controls-info {
            font-size: 11px;
            margin-top: 15px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }
        
        .sanskrit-text {
            font-style: italic;
            color: #DAA520;
            font-size: 11px;
        }
        
        h3 {
            color: #DAA520;
            margin-top: 0;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="game-world">
            <div class="region-display" id="regionDisplay">
                <strong>Ocean Frontier</strong><br>
                <span class="sanskrit-text">सागर सीमा (Sāgara Sīmā)</span><br>
                Starting coastal region
            </div>
            <div class="player-avatar" id="playerAvatar"></div>
        </div>
        
        <div class="ui-panel">
            <div class="player-info" id="playerInfo">
                <strong>Welcome to Ancient Bharat!</strong><br>
                <span id="playerName">Enter your name below</span><br>
                Level: <span id="playerLevel">1</span> | XP: <span id="playerXP">0</span>
            </div>
            
            <div class="chat-section">
                <h3>Traveler's Chronicle</h3>
                <div class="chat-messages" id="chatMessages"></div>
                <input type="text" class="chat-input" id="chatInput" placeholder="Share your journey...">
            </div>
            
            <div class="npc-section">
                <h3>Wise Guides</h3>
                <div id="npcList">Connect to meet the guides...</div>
            </div>
            
            <div class="quest-section">
                <h3>Sacred Quests</h3>
                <div id="questList">Connect to discover quests...</div>
            </div>
            
            <div class="controls-info">
                <strong>Controls:</strong><br>
                Arrow Keys: Move around<br>
                Enter: Send chat message<br>
                Click NPCs/Quests: Interact
            </div>
        </div>
    </div>

    <script>
        // Game client JavaScript
        let ws = null;
        let playerName = "";
        let playerData = {};
        let currentRegion = "ocean_frontier";
        
        // Get player name and connect
        function connectToGame() {
            playerName = prompt("Enter your traveler name:") || `Traveler_${Math.random().toString(36).substr(2, 6)}`;
            document.getElementById('playerName').textContent = playerName;
            
            const playerId = `player_${Math.random().toString(36).substr(2, 9)}`;
            const wsUrl = `ws://${window.location.host}/ws/${playerId}?name=${encodeURIComponent(playerName)}`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                console.log("Connected to Ancient Bharat!");
                addChatMessage("System", "Connected to Ancient Bharat! Welcome, traveler!");
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleServerMessage(data);
            };
            
            ws.onclose = function() {
                addChatMessage("System", "Connection lost. Please refresh to reconnect.");
            };
            
            ws.onerror = function(error) {
                console.error("WebSocket error:", error);
            };
        }
        
        function handleServerMessage(data) {
            switch(data.type) {
                case 'player_connected':
                    playerData = data.player_data;
                    updatePlayerInfo();
                    updateRegionDisplay(data.region_info);
                    updateNPCList(data.available_npcs);
                    updateQuestList(data.available_quests);
                    if(data.chat_history) {
                        data.chat_history.forEach(msg => {
                            addChatMessage(msg.player_name, msg.message);
                        });
                    }
                    break;
                    
                case 'region_changed':
                    currentRegion = data.new_region;
                    updateRegionDisplay(data.region_info);
                    updateNPCList(data.available_npcs);
                    addChatMessage("System", `You entered ${data.region_info.name}!`);
                    if(data.experience_gained > 0) {
                        addChatMessage("System", `+${data.experience_gained} XP for exploration!`);
                        playerData.experience += data.experience_gained;
                        updatePlayerInfo();
                    }
                    break;
                    
                case 'chat_message':
                    addChatMessage(data.player_name, data.message);
                    break;
                    
                case 'npc_response':
                    addChatMessage(`${data.npc_name} (${data.npc_sanskrit_name})`, data.response);
                    break;
                    
                case 'quest_started':
                    addChatMessage("System", `Quest started: ${data.quest.title}`);
                    playerData.experience += data.experience_gained;
                    updatePlayerInfo();
                    break;
                    
                case 'quest_completed':
                    addChatMessage("System", `Quest completed! ${data.completion_message}`);
                    playerData.experience += data.experience_gained;
                    if(data.level_up) {
                        addChatMessage("System", `Level up! You are now level ${data.new_level}!`);
                        playerData.level = data.new_level;
                    }
                    updatePlayerInfo();
                    break;
                    
                case 'player_joined':
                    addChatMessage("System", `${data.name} joined the world`);
                    break;
                    
                case 'player_left':
                    addChatMessage("System", `${data.name} left the world`);
                    break;
            }
        }
        
        function updatePlayerInfo() {
            document.getElementById('playerLevel').textContent = playerData.level || 1;
            document.getElementById('playerXP').textContent = playerData.experience || 0;
        }
        
        function updateRegionDisplay(regionInfo) {
            const display = document.getElementById('regionDisplay');
            display.innerHTML = `
                <strong>${regionInfo.name}</strong><br>
                <span class="sanskrit-text">${regionInfo.sanskrit_name}</span><br>
                ${regionInfo.description}
            `;
        }
        
        function updateNPCList(npcs) {
            const list = document.getElementById('npcList');
            if(!npcs || npcs.length === 0) {
                list.innerHTML = '<div style="color: #888;">No guides in this region</div>';
                return;
            }
            
            list.innerHTML = npcs.map(npc => `
                <div class="npc-item" onclick="interactWithNPC('${npc.npc_id}')">
                    <strong>${npc.name}</strong><br>
                    <span class="sanskrit-text">${npc.sanskrit_name}</span><br>
                    <small>${npc.title}</small>
                </div>
            `).join('');
        }
        
        function updateQuestList(quests) {
            const list = document.getElementById('questList');
            if(!quests || quests.length === 0) {
                list.innerHTML = '<div style="color: #888;">No quests available</div>';
                return;
            }
            
            list.innerHTML = quests.map(quest => `
                <div class="quest-item" onclick="startQuest('${quest.quest_id}')">
                    <strong>${quest.title}</strong><br>
                    <small>${quest.description}</small><br>
                    <em>Reward: ${quest.experience_reward} XP</em>
                </div>
            `).join('');
        }
        
        function addChatMessage(sender, message) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function interactWithNPC(npcId) {
            if(ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'npc_interaction',
                    npc_id: npcId,
                    interaction_type: 'greeting'
                }));
            }
        }
        
        function startQuest(questId) {
            if(ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'quest_action',
                    action: 'start',
                    quest_id: questId
                }));
            }
        }
        
        // Chat input handling
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if(e.key === 'Enter' && this.value.trim()) {
                if(ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'chat',
                        message: this.value.trim()
                    }));
                }
                this.value = '';
            }
        });
        
        // Movement simulation (arrow keys)
        let playerPos = {x: 0, z: 0};
        document.addEventListener('keydown', function(e) {
            const moveDistance = 50;
            let moved = false;
            
            switch(e.key) {
                case 'ArrowUp':
                    playerPos.z += moveDistance;
                    moved = true;
                    break;
                case 'ArrowDown':
                    playerPos.z -= moveDistance;
                    moved = true;
                    break;
                case 'ArrowLeft':
                    playerPos.x -= moveDistance;
                    moved = true;
                    break;
                case 'ArrowRight':
                    playerPos.x += moveDistance;
                    moved = true;
                    break;
            }
            
            if(moved && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'movement',
                    x: playerPos.x,
                    y: 0,
                    z: playerPos.z
                }));
            }
        });
        
        // Connect to game on load
        window.onload = connectToGame;
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/admin/save")
async def manual_save():
    """Manual save endpoint"""
    game_server.save_game_data()
    return {"status": "saved", "timestamp": time.time()}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Start auto-save task"""
    asyncio.create_task(auto_save_task())
    print("🚀 Ancient Bharat server started successfully!")
    print("🌐 Game client available at: http://localhost:8000/client")
    print("📊 Server status at: http://localhost:8000/status")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    """Save data on shutdown"""
    game_server.save_game_data()
    print("💾 Final save completed!")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("🏛️ Echoes of the Horizon - Ancient Bharat")
    print("=" * 50)
    print("🎮 Complete 3D multiplayer game in a single Python file!")
    print("📦 Dependencies: fastapi, uvicorn, websockets (auto-installed)")
    print("🌐 Game client: http://localhost:8000/client")
    print("📊 Server status: http://localhost:8000/status")
    print("=" * 50)
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )