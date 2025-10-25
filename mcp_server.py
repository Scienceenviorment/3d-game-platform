#!/usr/bin/env python3
"""
3D Game Platform MCP Server
===========================

Model Context Protocol server for the AI-powered 3D game platform.
Provides access to game state, 3D models, procedural generation, and AI systems.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
)

# Game imports
sys.path.append(str(Path(__file__).parent))
from server.ai_3d_model_agent import AI3DModelAgent
from server.procedural_generator import ProceduralGenerator
from server.karma_system import KarmaSystem
from server.class_system import ClassSystem

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GamePlatformMCPServer:
    """MCP Server for 3D Game Platform"""
    
    def __init__(self):
        self.server = Server("3d-game-platform")
        self.game_root = Path(__file__).parent
        self.ai_agent = None
        self.procedural_gen = None
        self.karma_system = None
        self.class_system = None
        
        self._setup_tools()
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize game systems"""
        try:
            # Initialize systems that don't require file system access during import
            self.procedural_gen = ProceduralGenerator()
            logger.info("Procedural generator initialized successfully")
            
            # Initialize AI agent with local mode for MCP server
            os.environ['LOCAL_MODE'] = '1'  # Signal to use local paths
            self.ai_agent = AI3DModelAgent()
            logger.info("AI 3D model agent initialized successfully")
            
            # Initialize other systems
            self.karma_system = KarmaSystem()
            self.class_system = ClassSystem()
            logger.info("Game systems initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize game systems: {e}")
            # Continue without AI agent if initialization fails
            self.ai_agent = None
    
    def _setup_tools(self):
        """Setup MCP tools for game interaction"""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available MCP tools"""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_game_status",
                        description="Get overall game platform status and statistics",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    ),
                    Tool(
                        name="get_player_data",
                        description="Retrieve player data and progress",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "player_id": {
                                    "type": "string",
                                    "description": "Player ID to retrieve data for"
                                }
                            },
                            "required": ["player_id"]
                        }
                    ),
                    Tool(
                        name="list_3d_models",
                        description="List available 3D models with metadata",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "category": {
                                    "type": "string",
                                    "enum": ["beasts", "weapons", "environments", "divine_entities", "props"],
                                    "description": "Category of 3D models to list"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Maximum number of models to return",
                                    "default": 10
                                }
                            },
                            "required": []
                        }
                    ),
                    Tool(
                        name="generate_procedural_content",
                        description="Generate new procedural game content",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "content_type": {
                                    "type": "string",
                                    "enum": ["beast", "weapon", "divine_entity", "quest"],
                                    "description": "Type of content to generate"
                                },
                                "count": {
                                    "type": "integer",
                                    "description": "Number of items to generate",
                                    "default": 1,
                                    "minimum": 1,
                                    "maximum": 10
                                }
                            },
                            "required": ["content_type"]
                        }
                    ),
                    Tool(
                        name="create_3d_model",
                        description="Generate a new 3D model using AI services",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Description of the 3D model to create"
                                },
                                "service": {
                                    "type": "string",
                                    "enum": ["luma", "meshy", "kaedim", "scenario"],
                                    "description": "AI service to use for generation"
                                },
                                "category": {
                                    "type": "string",
                                    "enum": ["beast", "weapon", "environment", "divine_entity", "prop"],
                                    "description": "Category for the 3D model"
                                }
                            },
                            "required": ["description", "category"]
                        }
                    ),
                    Tool(
                        name="get_karma_status",
                        description="Get karma system status and player karma",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "player_id": {
                                    "type": "string",
                                    "description": "Player ID to check karma for"
                                }
                            },
                            "required": []
                        }
                    ),
                    Tool(
                        name="get_world_state",
                        description="Get current world state and active events",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> CallToolResult:
            """Handle tool calls"""
            try:
                if name == "get_game_status":
                    return await self._get_game_status()
                elif name == "get_player_data":
                    return await self._get_player_data(arguments.get("player_id"))
                elif name == "list_3d_models":
                    return await self._list_3d_models(
                        arguments.get("category"),
                        arguments.get("limit", 10)
                    )
                elif name == "generate_procedural_content":
                    return await self._generate_procedural_content(
                        arguments.get("content_type"),
                        arguments.get("count", 1)
                    )
                elif name == "create_3d_model":
                    return await self._create_3d_model(
                        arguments.get("description"),
                        arguments.get("service"),
                        arguments.get("category")
                    )
                elif name == "get_karma_status":
                    return await self._get_karma_status(arguments.get("player_id"))
                elif name == "get_world_state":
                    return await self._get_world_state()
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Unknown tool: {name}"
                        )],
                        isError=True
                    )
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )
    
    async def _get_game_status(self) -> CallToolResult:
        """Get overall game platform status"""
        try:
            # Count 3D models
            models_dir = self.game_root / "game_data" / "3d_models"
            model_count = 0
            if models_dir.exists():
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        model_count += len(list(category_dir.glob("*.glb")))
            
            # Check player data
            player_data_file = self.game_root / "game_data" / "player_data.json"
            player_count = 0
            if player_data_file.exists():
                with open(player_data_file, 'r') as f:
                    data = json.load(f)
                    player_count = len(data.get("players", []))
            
            status = {
                "platform": "3D Game Platform",
                "version": "1.0.0",
                "status": "running",
                "statistics": {
                    "total_3d_models": model_count,
                    "total_players": player_count,
                    "ai_services": ["luma", "meshy", "kaedim", "scenario"],
                    "procedural_combinations": "102,384+",
                    "github_repository": "https://github.com/Scienceenviorment/3d-game-platform"
                },
                "systems": {
                    "ai_3d_generation": "active",
                    "procedural_generation": "active",
                    "karma_system": "active",
                    "class_system": "active"
                }
            }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(status, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to get game status: {e}")
    
    async def _get_player_data(self, player_id: str) -> CallToolResult:
        """Get player data"""
        try:
            player_file = self.game_root / "game_data" / f"player_{player_id}.json"
            if player_file.exists():
                with open(player_file, 'r') as f:
                    player_data = json.load(f)
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=json.dumps(player_data, indent=2)
                    )]
                )
            else:
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Player {player_id} not found"
                    )]
                )
        except Exception as e:
            raise Exception(f"Failed to get player data: {e}")
    
    async def _list_3d_models(self, category: Optional[str], limit: int) -> CallToolResult:
        """List 3D models"""
        try:
            models_dir = self.game_root / "game_data" / "3d_models"
            models = []
            
            if category:
                category_dir = models_dir / category
                if category_dir.exists():
                    for model_file in category_dir.glob("*.glb"):
                        models.append({
                            "name": model_file.name,
                            "category": category,
                            "path": str(model_file.relative_to(self.game_root)),
                            "size": model_file.stat().st_size
                        })
            else:
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        for model_file in category_dir.glob("*.glb"):
                            models.append({
                                "name": model_file.name,
                                "category": category_dir.name,
                                "path": str(model_file.relative_to(self.game_root)),
                                "size": model_file.stat().st_size
                            })
            
            # Limit results
            models = models[:limit]
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"models": models, "count": len(models)}, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to list 3D models: {e}")
    
    async def _generate_procedural_content(self, content_type: str, count: int) -> CallToolResult:
        """Generate procedural content"""
        try:
            if not self.procedural_gen:
                raise Exception("Procedural generator not initialized")
            
            results = []
            for _ in range(count):
                if content_type == "beast":
                    result = self.procedural_gen.generate_beast()
                elif content_type == "weapon":
                    result = self.procedural_gen.generate_weapon()
                elif content_type == "divine_entity":
                    result = self.procedural_gen.generate_divine_entity()
                else:
                    raise Exception(f"Unknown content type: {content_type}")
                
                results.append(result.__dict__)
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"generated_content": results}, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to generate procedural content: {e}")
    
    async def _create_3d_model(self, description: str, service: Optional[str], category: str) -> CallToolResult:
        """Create 3D model using AI"""
        try:
            if not self.ai_agent:
                raise Exception("AI 3D model agent not initialized")
            
            # Generate model
            model_data = await self.ai_agent.generate_3d_model(
                description=description,
                category=category,
                service=service or "auto"
            )
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(model_data, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to create 3D model: {e}")
    
    async def _get_karma_status(self, player_id: Optional[str]) -> CallToolResult:
        """Get karma status"""
        try:
            if player_id:
                # Get specific player karma
                karma_data = {"player_id": player_id, "karma": "Not implemented yet"}
            else:
                # Get overall karma system status
                karma_data = {
                    "system": "active",
                    "total_events": 0,
                    "average_karma": 0
                }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(karma_data, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to get karma status: {e}")
    
    async def _get_world_state(self) -> CallToolResult:
        """Get world state"""
        try:
            world_state_file = self.game_root / "game_data" / "world_state.json"
            if world_state_file.exists():
                with open(world_state_file, 'r') as f:
                    world_state = json.load(f)
            else:
                world_state = {
                    "time": "day",
                    "season": "spring",
                    "active_events": [],
                    "weather": "clear"
                }
            
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(world_state, indent=2)
                )]
            )
        except Exception as e:
            raise Exception(f"Failed to get world state: {e}")

async def main():
    """Run the MCP server"""
    print("🚀 Starting 3D Game Platform MCP Server...")
    print("📂 Working directory:", os.getcwd())
    
    try:
        server_instance = GamePlatformMCPServer()
        print("✅ MCP Server instance created successfully!")
        
        # Run the server
        print("🌐 Starting MCP server on stdio...")
        async with stdio_server() as (read_stream, write_stream):
            print("📡 MCP Server is running and ready for connections!")
            await server_instance.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="3d-game-platform",
                    server_version="1.0.0"
                )
            )
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())