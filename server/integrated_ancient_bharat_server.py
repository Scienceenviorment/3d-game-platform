#!/usr/bin/env python3
"""
Echoes of the Horizon - Integrated Ancient Bharat Server
Complete multiplayer exploration game with NPCs, quests, and world generation
"""

# Standard Python library imports
import json
import time
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from enum import Enum

# Third-party imports (FastAPI for web server)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our Ancient Bharat game systems
from ancient_bharat_config import get_config, get_data_manager, save_game_state
from enhanced_npcs import enhanced_npc_manager
from ancient_bharat_quests import get_quest_system, start_player_quest, update_player_quest
from ancient_bharat_world import get_world_generator, get_nearby_objects, get_terrain_height

# Import new expansion systems
from power_system import PowerSystem
from crafting_system import CraftingSystem
from class_system import ClassSystem
from hidden_content_system import HiddenContentSystem
from blackhole_event_system import BlackholeEventSystem
from voice_chat_system import VoiceChatSystem
from karma_system import KarmaSystem, KarmaActionType
from procedural_integration import procedural_manager
from procedural_3d_integration import procedural_3d_manager


# Ancient Bharat regions using Python Enum
class Region(Enum):
    """The five mystical regions of Ancient Bharat"""
    DUST_PLAINS = "dust_plains"
    HIMALAYAN_PEAKS = "himalayan_peaks" 
    INDRAPURA_CITY = "indrapura_city"
    NARMADA_FOREST = "narmada_forest"
    OCEAN_FRONTIER = "ocean_frontier"


# Data structures using Python dataclasses
@dataclass
class Position:
    """3D position in the world"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Player:
    """Enhanced player information with quest and world integration"""
    player_id: str
    name: str
    position: Position
    current_region: Region = Region.OCEAN_FRONTIER
    websocket: Optional[WebSocket] = None
    last_active: float = 0.0
    
    # New integrated features
    level: int = 1
    experience: int = 0
    regions_visited: List[str] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.regions_visited is None:
            self.regions_visited = ["ocean_frontier"]


class IntegratedAncientBharatServer:
    """Enhanced server with full game system integration"""
    
    def __init__(self):
        """Initialize the integrated game server"""
        print("🏛️ Initializing Echoes of the Horizon - Ancient Bharat Server")
        
        # Get all game systems
        self.config = get_config()
        self.data_manager = get_data_manager()
        self.npc_manager = enhanced_npc_manager
        self.quest_system = get_quest_system()
        self.world_generator = get_world_generator()
        
        # Initialize new expansion systems
        self.power_system = PowerSystem()
        self.crafting_system = CraftingSystem()
        self.class_system = ClassSystem()
        self.hidden_content_system = HiddenContentSystem()
        self.blackhole_system = BlackholeEventSystem()
        self.voice_chat_system = VoiceChatSystem()
        self.karma_system = KarmaSystem()
        
        # Initialize procedural generation system
        print("🔮 Initializing Procedural Content Generation...")
        self.procedural_manager = procedural_manager
        if self.procedural_manager.initialize():
            print("🌟 Procedural Generation System Ready!")
        else:
            print("⚠️ Procedural Generation System failed to initialize")
        
        # Initialize AI 3D Model Generation system
        print("🎨 Initializing AI 3D Model Generation...")
        self.procedural_3d_manager = procedural_3d_manager
        # Load existing model database
        self.procedural_3d_manager.load_model_database()
        print("🤖 AI 3D Model Generation System Ready!")
        
        # Connected players using Python dictionary
        self.connected_players: Dict[str, Player] = {}
        
        # Chat history using Python list
        self.chat_history: List[Dict] = []
        
        print("✅ All game systems initialized successfully")
        print("🌌 Blackhole Event System ready - secret area awaits discovery!")
        print("🎲 Procedural Generation System ready - infinite content awaits!")
        print("🎨 AI 3D Model Generation ready - visual content creation enabled!")
    
    def get_region_from_position(self, x: float, z: float) -> Region:
        """Determine region based on player position"""
        # Use configuration-based region detection
        if self.config.is_in_region(x, z, "dust_plains"):
            return Region.DUST_PLAINS
        elif self.config.is_in_region(x, z, "ocean_frontier"):
            return Region.OCEAN_FRONTIER
        elif self.config.is_in_region(x, z, "himalayan_peaks"):
            return Region.HIMALAYAN_PEAKS
        elif self.config.is_in_region(x, z, "narmada_forest"):
            return Region.NARMADA_FOREST
        else:
            return Region.INDRAPURA_CITY
    
    async def connect_player(self, websocket: WebSocket, player_id: str, player_name: str):
        """Handle new player connection with full integration"""
        try:
            # Accept WebSocket connection
            await websocket.accept()
            
            # Load player data from persistent storage
            player_data = self.data_manager.get_player_progress(player_id)
            
            # Create player object with loaded data
            last_pos = player_data.get("last_position", {"x": 0, "y": 2, "z": 0})
            player = Player(
                player_id=player_id,
                name=player_data.get("name", player_name),
                position=Position(
                    x=last_pos["x"], 
                    y=last_pos["y"], 
                    z=last_pos["z"]
                ),
                websocket=websocket,
                last_active=time.time(),
                level=player_data.get("level", 1),
                experience=player_data.get("experience", 0),
                regions_visited=player_data.get("regions_visited", ["ocean_frontier"])
            )
            
            # Determine current region
            player.current_region = self.get_region_from_position(player.position.x, player.position.z)
            
            # Add to connected players
            self.connected_players[player_id] = player
            
            # Send welcome message with integrated data
            welcome_data = {
                "type": "player_joined",
                "player_id": player_id,
                "name": player.name,
                "position": asdict(player.position),
                "current_region": player.current_region.value,
                "level": player.level,
                "experience": player.experience,
                "regions_visited": player.regions_visited
            }
            
            # Send to joining player
            await websocket.send_text(json.dumps(welcome_data))
            
            # Notify other players
            await self.broadcast_to_others(player_id, welcome_data)
            
            # Send available NPCs in current region
            await self.send_nearby_npcs(player)
            
            # Send available quests
            await self.send_available_quests(player)
            
            # Send nearby world objects
            await self.send_nearby_world_objects(player)
            
            # Send chat history
            await self.send_chat_history(player)
            
            print(f"🎮 Player {player.name} ({player_id}) connected in {player.current_region.value}")
            
        except Exception as e:
            print(f"❌ Error connecting player {player_id}: {e}")
    
    async def disconnect_player(self, player_id: str):
        """Handle player disconnection with data saving"""
        if player_id in self.connected_players:
            player = self.connected_players[player_id]
            
            # Save player progress
            self.save_player_progress(player)
            
            # Remove from connected players
            del self.connected_players[player_id]
            
            # Notify other players
            disconnect_data = {
                "type": "player_left",
                "player_id": player_id,
                "name": player.name
            }
            await self.broadcast_to_all(disconnect_data)
            
            print(f"👋 Player {player.name} ({player_id}) disconnected")
    
    def save_player_progress(self, player: Player):
        """Save player progress to persistent storage"""
        player_data = {
            "name": player.name,
            "level": player.level,
            "experience": player.experience,
            "regions_visited": player.regions_visited,
            "last_position": asdict(player.position),
            "last_login": time.time()
        }
        self.data_manager.save_player_progress(player.player_id, player_data)
    
    async def handle_player_movement(self, player_id: str, movement_data: dict):
        """Handle player movement with region detection and world interaction"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        
        # Update player position
        player.position.x = movement_data.get("x", player.position.x)
        player.position.y = movement_data.get("y", player.position.y) 
        player.position.z = movement_data.get("z", player.position.z)
        player.last_active = time.time()
        
        # Check for region change
        new_region = self.get_region_from_position(player.position.x, player.position.z)
        
        if new_region != player.current_region:
            # Player entered new region
            old_region = player.current_region
            player.current_region = new_region
            
            # Add to visited regions if not already visited
            region_name = new_region.value
            if region_name not in player.regions_visited:
                player.regions_visited.append(region_name)
                player.experience += 100  # Exploration reward
            
            # Send region change notification
            region_change_data = {
                "type": "region_changed",
                "player_id": player_id,
                "old_region": old_region.value,
                "new_region": new_region.value,
                "position": asdict(player.position),
                "experience_gained": 100 if region_name not in player.regions_visited else 0
            }
            await player.websocket.send_text(json.dumps(region_change_data))
            
            # Update NPCs and quests for new region
            await self.send_nearby_npcs(player)
            await self.send_available_quests(player)
        
        # Check for nearby world objects
        nearby_objects = get_nearby_objects(player.position.x, player.position.z, 20.0)
        if nearby_objects:
            objects_data = {
                "type": "nearby_objects",
                "objects": [
                    {
                        "object_id": obj.object_id,
                        "name": obj.name,
                        "sanskrit_name": obj.sanskrit_name,
                        "type": obj.object_type.value,
                        "position": asdict(obj.position),
                        "interactable": obj.interactable,
                        "cultural_significance": obj.cultural_significance
                    }
                    for obj in nearby_objects
                ]
            }
            await player.websocket.send_text(json.dumps(objects_data))
        
        # Broadcast movement to other players
        movement_broadcast = {
            "type": "player_moved",
            "player_id": player_id,
            "position": asdict(player.position),
            "current_region": player.current_region.value
        }
        await self.broadcast_to_others(player_id, movement_broadcast)
    
    async def handle_chat_message(self, player_id: str, message_data: dict):
        """Handle chat messages with enhanced features"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        message = message_data.get("message", "").strip()
        
        if not message:
            return
        
        # Create chat message with timestamp
        chat_message = {
            "type": "chat_message",
            "player_id": player_id,
            "player_name": player.name,
            "message": message,
            "timestamp": time.time(),
            "region": player.current_region.value
        }
        
        # Add to chat history
        self.chat_history.append(chat_message)
        
        # Keep chat history limited
        if len(self.chat_history) > self.config.server_config.max_chat_history:
            self.chat_history.pop(0)
        
        # Broadcast to all players
        await self.broadcast_to_all(chat_message)
    
    async def handle_npc_interaction(self, player_id: str, interaction_data: dict):
        """Handle NPC interactions with AI agent integration"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        npc_id = interaction_data.get("npc_id")
        player_message = interaction_data.get("message", "Hello")
        
        if not npc_id:
            return
        
        # Prepare player data for AI agent
        player_data = {
            "level": player.level,
            "experience": player.experience,
            "tamed_beasts": getattr(player, "tamed_beasts", []),
            "region": player.region
        }
        
        # Get AI-powered NPC response
        npc_response = self.npc_manager.interact_with_npc(
            npc_id, player_id, player_message, player_data
        )
        
        if npc_response:
            # Record interaction in data manager
            interaction_record = {
                "helpful_response": True,
                "quest_completed": False,
                "player_message": player_message,
                "ai_response": True
            }
            self.data_manager.record_npc_interaction(player_id, npc_id, interaction_record)
            
            # Send NPC response
            response_data = {
                "type": "npc_interaction",
                "npc_id": npc_id,
                "response": npc_response,
                "timestamp": time.time(),
                "enhanced_ai": True
            }
            await player.websocket.send_text(json.dumps(response_data))
    
    async def handle_quest_action(self, player_id: str, quest_data: dict):
        """Handle quest-related actions"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        action = quest_data.get("action")
        quest_id = quest_data.get("quest_id")
        
        if action == "start" and quest_id:
            # Start quest
            if start_player_quest(player_id, quest_id):
                # Award experience for starting quest
                player.experience += 25
                
                response_data = {
                    "type": "quest_started",
                    "quest_id": quest_id,
                    "experience_gained": 25
                }
                await player.websocket.send_text(json.dumps(response_data))
        
        elif action == "update" and quest_id:
            # Update quest progress
            objective_id = quest_data.get("objective_id")
            amount = quest_data.get("amount", 1)
            
            if update_player_quest(player_id, quest_id, objective_id, amount):
                # Quest completed
                player.experience += 250
                
                response_data = {
                    "type": "quest_completed",
                    "quest_id": quest_id,
                    "experience_gained": 250
                }
                await player.websocket.send_text(json.dumps(response_data))
    
    async def send_nearby_npcs(self, player: Player):
        """Send available NPCs in player's region"""
        available_npcs = self.npc_manager.get_npcs_in_region(player.current_region.value)
        
        if available_npcs:
            npcs_data = {
                "type": "nearby_npcs",
                "npcs": [
                    {
                        "npc_id": npc.npc_id,
                        "name": npc.name,
                        "sanskrit_name": npc.sanskrit_name,
                        "title": npc.title,
                        "region": npc.current_region.value,
                        "personality": npc.personality_type.value,
                        "available": npc.is_available()
                    }
                    for npc in available_npcs
                ]
            }
            await player.websocket.send_text(json.dumps(npcs_data))
    
    async def send_available_quests(self, player: Player):
        """Send available quests for player"""
        available_quests = self.quest_system.get_available_quests(
            player.player_id, 
            player.level,
            player.current_region.value
        )
        
        if available_quests:
            quests_data = {
                "type": "available_quests",
                "quests": [
                    {
                        "quest_id": quest.quest_id,
                        "title": quest.title,
                        "description": quest.description,
                        "difficulty": quest.difficulty.value,
                        "type": quest.quest_type.value,
                        "level_required": quest.level_required,
                        "giver_npc": quest.giver_npc
                    }
                    for quest in available_quests
                ]
            }
            await player.websocket.send_text(json.dumps(quests_data))
    
    async def send_nearby_world_objects(self, player: Player):
        """Send nearby world objects"""
        nearby_objects = get_nearby_objects(player.position.x, player.position.z, 100.0)
        
        if nearby_objects:
            objects_data = {
                "type": "world_objects",
                "objects": [
                    {
                        "object_id": obj.object_id,
                        "name": obj.name,
                        "sanskrit_name": obj.sanskrit_name,
                        "type": obj.object_type.value,
                        "cultural_significance": obj.cultural_significance,
                        "interactable": obj.interactable,
                        "quest_related": obj.quest_related
                    }
                    for obj in nearby_objects[:20]  # Limit to 20 objects
                ]
            }
            await player.websocket.send_text(json.dumps(objects_data))
    
    async def send_chat_history(self, player: Player):
        """Send recent chat history to player"""
        if self.chat_history:
            history_data = {
                "type": "chat_history",
                "messages": self.chat_history[-20:]  # Last 20 messages
            }
            await player.websocket.send_text(json.dumps(history_data))
    
    async def broadcast_to_all(self, data: dict):
        """Broadcast message to all connected players"""
        message = json.dumps(data)
        disconnected_players = []
        
        for player_id, player in self.connected_players.items():
            try:
                await player.websocket.send_text(message)
            except:
                # Mark for disconnection
                disconnected_players.append(player_id)
        
        # Clean up disconnected players
        for player_id in disconnected_players:
            await self.disconnect_player(player_id)
    
    async def broadcast_to_others(self, sender_id: str, data: dict):
        """Broadcast message to all players except sender"""
        message = json.dumps(data)
        disconnected_players = []
        
        for player_id, player in self.connected_players.items():
            if player_id != sender_id:
                try:
                    await player.websocket.send_text(message)
                except:
                    disconnected_players.append(player_id)
        
        # Clean up disconnected players
        for player_id in disconnected_players:
            await self.disconnect_player(player_id)
    
    async def handle_websocket_message(self, websocket: WebSocket, player_id: str):
        """Main WebSocket message handler with full integration"""
        try:
            while True:
                # Receive message from client
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
                
                elif message_type == "voice_chat":
                    await self.handle_voice_chat(player_id, message)
                
                elif message_type == "karma_action":
                    await self.handle_karma_action(player_id, message)
                
                elif message_type == "npc_voice_interaction":
                    await self.handle_npc_voice_interaction(player_id, message)
                
                elif message_type == "procedural_content":
                    await self.handle_procedural_content_request(player_id, message)
                
                elif message_type == "3d_model_request":
                    await self.handle_3d_model_request(player_id, message)
                
                elif message_type == "world_interaction":
                    # Handle world object interactions
                    object_id = message.get("object_id")
                    # Add world interaction logic here
                
                else:
                    print(f"⚠️ Unknown message type: {message_type}")
        
        except WebSocketDisconnect:
            await self.disconnect_player(player_id)
        except Exception as e:
            print(f"❌ Error handling WebSocket message: {e}")
            await self.disconnect_player(player_id)
    
    async def handle_voice_chat(self, player_id: str, voice_data: dict):
        """Handle voice chat messages"""
        if player_id not in self.connected_players:
            return
        
        action = voice_data.get("action")
        
        if action == "join_channel":
            channel_id = voice_data.get("channel_id", "global")
            result = await self.voice_chat_system.join_voice_channel(player_id, channel_id)
            
            response_data = {
                "type": "voice_chat_response",
                "action": "join_result",
                "result": result
            }
            
        elif action == "send_voice":
            channel_id = voice_data.get("channel_id", "global")
            audio_data = voice_data.get("audio_data")
            sender_name = self.connected_players[player_id].name
            
            result = await self.voice_chat_system.send_voice_message(
                player_id, sender_name, audio_data, channel_id
            )
            
            if result.get("success"):
                # Broadcast to channel participants
                await self.broadcast_voice_message(result["message_data"], result["recipients"])
            
            response_data = {
                "type": "voice_chat_response", 
                "action": "send_result",
                "result": result
            }
        
        else:
            response_data = {
                "type": "voice_chat_error",
                "message": f"Unknown voice action: {action}"
            }
        
        await self.connected_players[player_id].websocket.send_text(json.dumps(response_data))
    
    async def handle_npc_voice_interaction(self, player_id: str, voice_data: dict):
        """Handle voice interactions with NPCs"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        npc_id = voice_data.get("npc_id")
        action = voice_data.get("action")
        
        if action == "send_speech":
            audio_data = voice_data.get("audio_data")
            
            # Convert speech to text
            speech_result = await self.voice_chat_system.process_speech_to_text(audio_data)
            
            if speech_result.get("success"):
                transcript = speech_result["transcript"]
                
                # Get NPC response using AI system
                npc_response = await self.npc_manager.get_enhanced_response(
                    npc_id, transcript, player_id
                )
                
                # Check karma alignment for NPC reaction
                karma_reaction = self.karma_system.get_npc_reaction_to_player(player_id, npc_id)
                
                # Modify NPC response based on karma
                if karma_reaction["alignment"] in ["evil", "dark_lord", "absolute_evil"]:
                    npc_response = f"*trembles* {npc_response} *steps back nervously*"
                elif karma_reaction["alignment"] in ["pure_saint", "virtuous"]:
                    npc_response = f"*bows respectfully* Blessed one, {npc_response}"
                
                # Convert NPC response to speech
                tts_result = await self.voice_chat_system.synthesize_npc_speech(npc_response, npc_id)
                
                response_data = {
                    "type": "npc_voice_response",
                    "transcript": transcript,
                    "npc_response": npc_response,
                    "npc_audio": tts_result.get("audio_data"),
                    "karma_reaction": karma_reaction
                }
            else:
                response_data = {
                    "type": "npc_voice_error",
                    "error": speech_result.get("error")
                }
        
        await player.websocket.send_text(json.dumps(response_data))
    
    async def handle_karma_action(self, player_id: str, karma_data: dict):
        """Handle karma-affecting actions"""
        if player_id not in self.connected_players:
            return
        
        action_type_str = karma_data.get("action_type")
        description = karma_data.get("description", "")
        witnesses = karma_data.get("witnesses", [])
        
        try:
            # Convert string to enum
            action_type = KarmaActionType(action_type_str)
            
            # Record karma action
            result = self.karma_system.record_karma_action(
                player_id, action_type, description, witnesses
            )
            
            # Send karma update to player
            response_data = {
                "type": "karma_update",
                "result": result,
                "karma_summary": self.karma_system.get_karma_summary(player_id)
            }
            
        except ValueError:
            response_data = {
                "type": "karma_error",
                "error": f"Invalid karma action type: {action_type_str}"
            }
        
        await self.connected_players[player_id].websocket.send_text(json.dumps(response_data))
    
    async def broadcast_voice_message(self, message_data: dict, recipients: list):
        """Broadcast voice message to recipients"""
        message = json.dumps(message_data)
        
        for recipient_id in recipients:
            if recipient_id in self.connected_players:
                try:
                    await self.connected_players[recipient_id].websocket.send_text(message)
                except:
                    pass
    
    async def handle_procedural_content_request(self, player_id: str, request_data: dict):
        """Handle requests for procedurally generated content"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        request_type = request_data.get("request_type")
        
        try:
            response_data = {"type": "procedural_content_response"}
            
            if request_type == "random_job_class":
                content = self.procedural_manager.get_random_job_class()
                response_data.update({
                    "content_type": "job_class",
                    "content": content
                })
            
            elif request_type == "random_weapon":
                content = self.procedural_manager.get_random_weapon()
                response_data.update({
                    "content_type": "weapon", 
                    "content": content
                })
            
            elif request_type == "random_beast":
                content = self.procedural_manager.get_random_beast()
                response_data.update({
                    "content_type": "beast",
                    "content": content
                })
            
            elif request_type == "random_divine":
                content = self.procedural_manager.get_random_divine_entity()
                response_data.update({
                    "content_type": "divine_entity",
                    "content": content
                })
            
            elif request_type == "quest_content":
                content = self.procedural_manager.generate_quest_content()
                response_data.update({
                    "content_type": "quest_bundle",
                    "content": content
                })
            
            elif request_type == "player_level_content":
                content = self.procedural_manager.get_content_for_player_level(player.level)
                response_data.update({
                    "content_type": "level_appropriate",
                    "content": content,
                    "player_level": player.level
                })
            
            elif request_type == "content_by_rarity":
                rarity = request_data.get("rarity", "common")
                content_type = request_data.get("content_category", "weapons")
                content = self.procedural_manager.get_content_by_rarity(content_type, rarity)
                response_data.update({
                    "content_type": f"{content_type}_by_rarity",
                    "content": content,
                    "rarity": rarity
                })
            
            elif request_type == "generation_stats":
                stats = self.procedural_manager.get_statistics()
                response_data.update({
                    "content_type": "statistics",
                    "content": stats
                })
            
            else:
                response_data = {
                    "type": "procedural_content_error",
                    "error": f"Unknown request type: {request_type}"
                }
        
        except Exception as e:
            response_data = {
                "type": "procedural_content_error", 
                "error": f"Failed to generate content: {str(e)}"
            }
        
        await player.websocket.send_text(json.dumps(response_data))
    
    async def handle_3d_model_request(self, player_id: str, request_data: dict):
        """Handle requests for 3D model generation"""
        if player_id not in self.connected_players:
            return
        
        player = self.connected_players[player_id]
        request_type = request_data.get("request_type")
        
        try:
            response_data = {"type": "3d_model_response"}
            
            if request_type == "generate_for_content":
                # Generate 3D model for specific content
                content_data = request_data.get("content_data", {})
                
                model_result = await self.procedural_3d_manager.generate_model_for_content(content_data)
                
                if model_result:
                    response_data.update({
                        "success": True,
                        "model_info": model_result
                    })
                else:
                    response_data.update({
                        "success": False,
                        "error": "Failed to generate 3D model"
                    })
            
            elif request_type == "get_model_for_content":
                # Get existing 3D model for content
                content_id = request_data.get("content_id")
                model_info = self.procedural_3d_manager.get_model_for_content(content_id)
                
                response_data.update({
                    "success": model_info is not None,
                    "model_info": model_info
                })
            
            elif request_type == "get_models_by_type":
                # Get all models of specific type
                content_type = request_data.get("content_type", "weapon")
                models = self.procedural_3d_manager.get_models_by_type(content_type)
                
                response_data.update({
                    "success": True,
                    "models": models,
                    "count": len(models)
                })
            
            elif request_type == "batch_generate":
                # Generate models for multiple items
                batch_result = await self.procedural_3d_manager.batch_generate_models_for_procedural_content()
                
                response_data.update({
                    "success": True,
                    "batch_result": batch_result
                })
            
            elif request_type == "preload_priority":
                # Preload priority models
                preload_result = await self.procedural_3d_manager.preload_priority_models()
                
                response_data.update({
                    "success": True,
                    "preload_result": preload_result
                })
            
            elif request_type == "3d_model_stats":
                # Get 3D model generation statistics
                stats = self.procedural_3d_manager.get_statistics()
                
                response_data.update({
                    "success": True,
                    "statistics": stats
                })
            
            else:
                response_data = {
                    "type": "3d_model_error",
                    "error": f"Unknown request type: {request_type}"
                }
        
        except Exception as e:
            response_data = {
                "type": "3d_model_error",
                "error": f"Failed to process 3D model request: {str(e)}"
            }
        
        await player.websocket.send_text(json.dumps(response_data))
    
    def get_server_status(self) -> dict:
        """Get comprehensive server status"""
        blackhole_status = self.blackhole_system.get_event_status()
        procedural_stats = self.procedural_manager.get_statistics()
        model_stats = self.procedural_3d_manager.get_statistics()
        
        return {
            "server_name": "Echoes of the Horizon - Ancient Bharat",
            "connected_players": len(self.connected_players),
            "max_players": self.config.server_config.max_players,
            "regions": [region.value for region in Region],
            "total_npcs": len(self.npc_manager.npcs),
            "total_quests": len(self.quest_system.quests),
            "world_chunks_generated": len(self.world_generator.chunks),
            "uptime": time.time() - server_start_time,
            "game_systems": {
                "npc_system": "active",
                "quest_system": "active", 
                "world_generation": "active",
                "data_persistence": "active",
                "power_system": "active",
                "crafting_system": "active",
                "class_system": "active",
                "hidden_content": "active",
                "blackhole_event": "ready" if not blackhole_status["blackhole_active"] else "ACTIVE",
                "procedural_generation": "active" if self.procedural_manager.is_initialized else "inactive",
                "ai_3d_models": "active"
            },
            "expansion_features": {
                "available_races": blackhole_status["races_available"],
                "total_job_classes": blackhole_status["total_job_classes"],
                "exclusive_classes_taken": blackhole_status["exclusive_classes_taken"],
                "secret_area_discovered": blackhole_status["secret_area_discovered"],
                "dimensional_collision": blackhole_status["blackhole_active"]
            },
            "procedural_content": {
                "total_generated": procedural_stats["total_content"],
                "job_classes": procedural_stats["total_job_classes"],
                "weapons": procedural_stats["total_weapons"],
                "beasts": procedural_stats["total_beasts"],
                "divine_entities": procedural_stats["total_divine_entities"],
                "potential_combinations": procedural_stats["potential_combinations"]
            },
            "ai_3d_models": {
                "total_models_generated": model_stats["completed_generations"],
                "models_cached": model_stats["cached_models"],
                "generation_success_rate": model_stats["success_rate"],
                "active_generations": model_stats["active_generations"],
                "ai_services_available": len(model_stats["ai_agent_stats"]["available_services"]) if "ai_agent_stats" in model_stats else 0
            }
        }


# Create global server instance
server_start_time = time.time()
game_server = IntegratedAncientBharatServer()

# Create FastAPI app
app = FastAPI(title="Echoes of the Horizon - Ancient Bharat Server")

# Add CORS middleware for browser compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for player connections"""
    # Extract player name from query parameters
    player_name = websocket.query_params.get("name", f"Player_{player_id[:8]}")
    
    # Connect player
    await game_server.connect_player(websocket, player_id, player_name)
    
    # Handle messages
    await game_server.handle_websocket_message(websocket, player_id)


@app.get("/")
async def root():
    """Root endpoint with server information"""
    return game_server.get_server_status()


@app.get("/status")
async def server_status():
    """Detailed server status endpoint"""
    return game_server.get_server_status()


@app.get("/players")
async def get_players():
    """Get list of connected players"""
    return {
        "players": [
            {
                "player_id": player.player_id,
                "name": player.name,
                "current_region": player.current_region.value,
                "level": player.level,
                "last_active": player.last_active
            }
            for player in game_server.connected_players.values()
        ]
    }


@app.get("/world/stats")
async def world_statistics():
    """Get world generation statistics"""
    return game_server.world_generator.get_world_statistics()


@app.get("/npcs/status")
async def npc_status():
    """Get enhanced NPC status with AI information"""
    return game_server.npc_manager.get_all_npcs_status()


@app.get("/beasts/{beast_name}")
async def beast_information(beast_name: str):
    """Get comprehensive beast information from AI NPCs"""
    return game_server.npc_manager.get_beast_information(beast_name)


@app.post("/admin/save")
async def save_game_data():
    """Admin endpoint to save all game data"""
    save_game_state()
    return {"status": "saved", "timestamp": time.time()}


# Auto-save task
async def auto_save_task():
    """Automatic periodic save of game data"""
    while True:
        await asyncio.sleep(game_server.config.server_config.auto_save_interval)
        
        try:
            # Save all player progress
            for player in game_server.connected_players.values():
                game_server.save_player_progress(player)
            
            # Save global game state
            save_game_state()
            
            print(f"💾 Auto-save completed at {time.ctime()}")
        
        except Exception as e:
            print(f"❌ Auto-save error: {e}")


@app.on_event("startup")
async def startup_event():
    """Server startup tasks"""
    print("🚀 Starting Echoes of the Horizon server...")
    
    # Start auto-save task
    asyncio.create_task(auto_save_task())
    
    print("✅ Server startup completed!")


@app.on_event("shutdown")
async def shutdown_event():
    """Server shutdown tasks"""
    print("🛑 Shutting down server...")
    
    # Save all player progress
    for player in game_server.connected_players.values():
        game_server.save_player_progress(player)
    
    # Save game state
    save_game_state()
    
    print("💾 Final save completed!")


# Run server
if __name__ == "__main__":
    config = get_config()
    
    print(f"🎮 Starting Echoes of the Horizon - Ancient Bharat Server")
    print(f"📡 Server: {config.get_server_address()}")
    print(f"🌐 WebSocket: {config.get_websocket_address()}")
    print("=" * 60)
    
    # Run with uvicorn
    uvicorn.run(
        app,
        host=config.server_config.host,
        port=config.server_config.port,
        log_level="info"
    )