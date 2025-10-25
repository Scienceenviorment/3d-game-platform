#!/usr/bin/env python3
"""
Echoes of the Horizon - Ancient Bharat Server
A Python-based multiplayer exploration game set in mythological India
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
    """Player information and state"""
    player_id: str
    name: str
    position: Position
    current_region: Region = Region.OCEAN_FRONTIER
    websocket: Optional[WebSocket] = None
    last_active: float = 0.0


# Main game server class
class AncientBharatServer:
    """Game server managing Ancient Bharat world and players"""
    
    def __init__(self):
        """Initialize the server with empty player list and region data"""
        # Use Python dictionaries for simple data storage
        self.players = {}  # Dict[str, Player]
        self.connections = []  # List[WebSocket]
        self.world_data = self._create_world_data()
    
    def _create_world_data(self) -> Dict[str, dict]:
        """Create the five regions of Ancient Bharat using Python dictionaries"""
        return {
            # Dust Plains - Western desert region
            Region.DUST_PLAINS.value: {
                "name": "The Dust Plains",
                "description": "Endless sands hide ancient secrets and forgotten ruins",
                "atmosphere_color": [0.9, 0.7, 0.4],  # Sandy brown
                "special_locations": ["Ancient Ruins", "Oasis of Memory", "Caravan Rest"],
                "terrain_type": "desert",
                "elevation": 0.5
            },
            
            # Himalayan Peaks - Northern mountains
            Region.HIMALAYAN_PEAKS.value: {
                "name": "Himalayan Peaks",
                "description": "Sacred mountains where sages meditate in eternal snow",
                "atmosphere_color": [0.8, 0.9, 1.0],  # Cool blue-white
                "special_locations": ["Mountain Monastery", "Prayer Flag Valley", "Ice Cave Shrine"],
                "terrain_type": "mountains",
                "elevation": 3.0
            },
            
            # Indrapura City - Central trade hub
            Region.INDRAPURA_CITY.value: {
                "name": "Indrapura City",
                "description": "Bustling metropolis where cultures meet and stories are born",
                "atmosphere_color": [1.0, 0.8, 0.5],  # Golden yellow
                "special_locations": ["Royal Palace", "Grand Bazaar", "Temple Complex"],
                "terrain_type": "urban",
                "elevation": 1.0
            },
            
            # Narmada Forest - Southern woodland
            Region.NARMADA_FOREST.value: {
                "name": "Narmada Forest",
                "description": "Dense jungle where ancient wisdom sleeps among banyan trees",
                "atmosphere_color": [0.2, 0.7, 0.2],  # Deep green
                "special_locations": ["Sacred Grove", "Hermit's Hut", "Ancient Banyan"],
                "terrain_type": "forest",
                "elevation": 1.5
            },
            
            # Ocean Frontier - Eastern coast (starting area)
            Region.OCEAN_FRONTIER.value: {
                "name": "Ocean Frontier", 
                "description": "Coastal haven where all great journeys begin",
                "atmosphere_color": [0.4, 0.7, 1.0],  # Ocean blue
                "special_locations": ["Lighthouse", "Fishing Village", "Shrine by the Sea"],
                "terrain_type": "coastal",
                "elevation": 0.2
            }
        }
    
    def get_region_from_position(self, pos: Position) -> Region:
        """
        Determine which region a position belongs to
        Using simple coordinate-based boundaries
        """
        x, z = pos.x, pos.z
        
        # Define region boundaries
        if x < -200:      # West = Desert
            return Region.DUST_PLAINS
        elif x > 200:     # East = Ocean
            return Region.OCEAN_FRONTIER
        elif z > 200:     # North = Mountains
            return Region.HIMALAYAN_PEAKS
        elif z < -100:    # South = Forest
            return Region.NARMADA_FOREST
        else:             # Center = City
            return Region.INDRAPURA_CITY
    
    async def add_player(self, websocket: WebSocket, player_id: str, player_name: str):
        """Add a new player to Ancient Bharat"""
        # Accept the WebSocket connection
        await websocket.accept()
        
        # Create new player starting at Ocean Frontier
        starting_pos = Position(250, 2, 0)  # Eastern coast
        new_player = Player(
            player_id=player_id,
            name=player_name,
            position=starting_pos,
            current_region=Region.OCEAN_FRONTIER,
            websocket=websocket,
            last_active=time.time()
        )
        
        # Store player in our dictionaries
        self.players[player_id] = new_player
        self.connections.append(websocket)
        
        # Send welcome message with region information
        region_data = self.world_data[new_player.current_region.value]
        welcome_message = {
            "type": "welcome",
            "player_id": player_id,
            "message": f"नमस्ते! Welcome to {region_data['name']}, {player_name}",
            "position": asdict(new_player.position),
            "region": {
                "name": region_data["name"],
                "description": region_data["description"],
                "color": region_data["atmosphere_color"]
            }
        }
        await self._send_to_player(player_id, welcome_message)
        
        # Notify other players about the new arrival
        join_notification = {
            "type": "player_joined",
            "player": {
                "id": new_player.player_id,
                "name": new_player.name,
                "position": asdict(new_player.position),
                "region": new_player.current_region.value
            }
        }
        await self._broadcast_to_others(player_id, join_notification)
        
        # Send information about existing players to the new player
        for existing_player in self.players.values():
            if existing_player.player_id != player_id:
                existing_info = {
                    "type": "player_joined",
                    "player": {
                        "id": existing_player.player_id,
                        "name": existing_player.name,
                        "position": asdict(existing_player.position),
                        "region": existing_player.current_region.value
                    }
                }
                await self._send_to_player(player_id, existing_info)
        
        print(f"🎭 {player_name} joined Ancient Bharat at {region_data['name']}")
    
    async def remove_player(self, player_id: str):
        """Remove a player from the game"""
        if player_id in self.players:
            player = self.players[player_id]
            
            # Remove from connections list
            if player.websocket in self.connections:
                self.connections.remove(player.websocket)
            
            # Remove from players dictionary
            player_name = player.name
            del self.players[player_id]
            
            # Notify remaining players
            departure_message = {
                "type": "player_left",
                "player_id": player_id,
                "message": f"{player_name} has left Ancient Bharat"
            }
            await self._broadcast_to_all(departure_message)
            
            print(f"👋 {player_name} left Ancient Bharat")
    
    async def handle_player_movement(self, player_id: str, movement_data: dict):
        """Process player movement and check for region changes"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        
        # Update position if provided
        if "position" in movement_data:
            pos_data = movement_data["position"]
            new_position = Position(pos_data["x"], pos_data["y"], pos_data["z"])
            player.position = new_position
            player.last_active = time.time()
            
            # Check if player moved to a different region
            new_region = self.get_region_from_position(new_position)
            if new_region != player.current_region:
                # Player entered a new region!
                old_region_data = self.world_data[player.current_region.value]
                new_region_data = self.world_data[new_region.value]
                player.current_region = new_region
                
                # Send region change notification
                region_change_message = {
                    "type": "region_changed",
                    "old_region": old_region_data["name"],
                    "new_region": {
                        "name": new_region_data["name"],
                        "description": new_region_data["description"],
                        "color": new_region_data["atmosphere_color"]
                    },
                    "message": f"You have entered {new_region_data['name']}. {new_region_data['description']}"
                }
                await self._send_to_player(player_id, region_change_message)
                
                print(f"🗺️ {player.name} entered {new_region_data['name']}")
        
        # Broadcast movement to other players
        movement_broadcast = {
            "type": "player_moved",
            "player_id": player_id,
            "position": asdict(player.position),
            "region": player.current_region.value
        }
        await self._broadcast_to_others(player_id, movement_broadcast)
    
    async def handle_chat_message(self, player_id: str, message: str):
        """Process chat message and broadcast with location context"""
        if player_id not in self.players:
            return
        
        player = self.players[player_id]
        region_data = self.world_data[player.current_region.value]
        
        # Create chat message with regional context
        chat_broadcast = {
            "type": "chat",
            "player_id": player_id,
            "player_name": player.name,
            "message": message,
            "region": region_data["name"],
            "timestamp": time.time()
        }
        await self._broadcast_to_all(chat_broadcast)
        
        print(f"💬 {player.name} in {region_data['name']}: {message}")
    
    async def _send_to_player(self, player_id: str, message: dict):
        """Send message to a specific player"""
        if player_id in self.players:
            player = self.players[player_id]
            if player.websocket:
                try:
                    message_json = json.dumps(message)
                    await player.websocket.send_text(message_json)
                except Exception:
                    # Connection failed, remove player
                    await self.remove_player(player_id)
    
    async def _broadcast_to_all(self, message: dict):
        """Send message to all connected players"""
        if not self.connections:
            return
        
        message_json = json.dumps(message)
        failed_connections = []
        
        # Try to send to each connection
        for connection in self.connections:
            try:
                await connection.send_text(message_json)
            except Exception:
                failed_connections.append(connection)
        
        # Clean up failed connections
        for failed_conn in failed_connections:
            if failed_conn in self.connections:
                self.connections.remove(failed_conn)
    
    async def _broadcast_to_others(self, exclude_player_id: str, message: dict):
        """Send message to all players except the specified one"""
        message_json = json.dumps(message)
        failed_players = []
        
        # Send to each player except the excluded one
        for pid, player in self.players.items():
            if pid != exclude_player_id and player.websocket:
                try:
                    await player.websocket.send_text(message_json)
                except Exception:
                    failed_players.append(pid)
        
        # Clean up failed players
        for failed_pid in failed_players:
            await self.remove_player(failed_pid)


# Create the game server instance
game_server = AncientBharatServer()

# Create FastAPI application
app = FastAPI(
    title="🏛️ Echoes of the Horizon",
    description="Ancient Bharat Multiplayer Game Server",
    version="1.0.0"
)

# Enable CORS for browser connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes
@app.get("/")
async def server_status():
    """Get server status and basic information"""
    return {
        "server_name": "🏛️ Echoes of the Horizon - Ancient Bharat",
        "status": "online",
        "travelers_online": len(game_server.players),
        "regions_available": len(game_server.world_data),
        "version": "1.0.0",
        "description": "Journey through the mystical lands of Ancient Bharat"
    }


@app.get("/regions")
async def get_regions():
    """Get information about all Ancient Bharat regions"""
    return {
        "regions": game_server.world_data,
        "total_regions": len(game_server.world_data)
    }


@app.get("/players")
async def get_online_players():
    """Get list of currently online players"""
    players_info = []
    for player in game_server.players.values():
        players_info.append({
            "id": player.player_id,
            "name": player.name,
            "region": player.current_region.value,
            "last_active": player.last_active
        })
    
    return {
        "players": players_info,
        "total_online": len(players_info)
    }


# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time gameplay"""
    player_id = None
    
    try:
        # Accept initial connection
        await websocket.accept()
        
        # Wait for connection message
        initial_data = await websocket.receive_text()
        initial_message = json.loads(initial_data)
        
        # Handle player connection
        if initial_message["type"] == "connect":
            player_id = initial_message["player_id"]
            player_name = initial_message.get("player_name", f"Traveler_{player_id[:8]}")
            
            # Add player to the game
            await game_server.add_player(websocket, player_id, player_name)
            
            # Listen for ongoing messages
            async for data in websocket.iter_text():
                try:
                    message = json.loads(data)
                    
                    # Handle different message types
                    if message["type"] == "move":
                        await game_server.handle_player_movement(player_id, message)
                    elif message["type"] == "chat":
                        await game_server.handle_chat_message(player_id, message["message"])
                    
                except json.JSONDecodeError:
                    # Ignore invalid JSON
                    continue
                except Exception as e:
                    print(f"❌ Error processing message from {player_id}: {e}")
    
    except WebSocketDisconnect:
        # Normal disconnection
        pass
    except Exception as e:
        print(f"❌ WebSocket error for player {player_id}: {e}")
    finally:
        # Clean up when connection ends
        if player_id:
            await game_server.remove_player(player_id)


# Main execution
if __name__ == "__main__":
    print("🏛️ Echoes of the Horizon - Ancient Bharat Server")
    print("🐍 Powered by Python and FastAPI")
    print("=" * 60)
    
    print("🗺️ Ancient Bharat regions ready for exploration:")
    for region_key, region_info in game_server.world_data.items():
        print(f"   🏞️ {region_info['name']}")
        print(f"      📖 {region_info['description']}")
        print()
    
    print("🚀 Starting server...")
    print("🌐 Server URL: http://localhost:8000")
    print("📡 WebSocket: ws://localhost:8000/ws") 
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    # Start the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
