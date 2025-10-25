#!/usr/bin/env python3
"""
Enhanced MCP Server for 3D Game Platform
========================================

A comprehensive Model Context Protocol server for the AI-powered 3D game platform.
Provides advanced access to game state, 3D models, procedural generation, and AI systems.

Features:
- Game status monitoring
- 3D model management
- Player data access
- Procedural content generation
- AI model creation interface
- Real-time game statistics
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# MCP imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Simple3DGameMCPServer:
    """Simple MCP Server for 3D Game Platform"""
    
    def __init__(self):
        self.server = Server("3d-game-platform")
        self.game_root = Path(__file__).parent
        print(f"🎮 Game root directory: {self.game_root}")
        
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup MCP tools for game interaction"""
        
        @self.server.list_tools()
        async def list_tools():
            """List available MCP tools"""
            return [
                Tool(
                    name="get_game_status",
                    description="Get overall game platform status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="list_3d_models",
                    description="List available 3D models",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Category of models to list"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_player_count",
                    description="Get number of players in the system",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="generate_content",
                    description="Generate procedural game content",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "content_type": {
                                "type": "string",
                                "enum": ["beast", "weapon", "divine_entity"],
                                "description": "Type of content to generate"
                            },
                            "count": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5,
                                "default": 1,
                                "description": "Number of items to generate"
                            }
                        },
                        "required": ["content_type"]
                    }
                ),
                Tool(
                    name="get_system_stats",
                    description="Get detailed system statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="search_models",
                    description="Search 3D models by name or properties",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for model names"
                            },
                            "category": {
                                "type": "string", 
                                "description": "Filter by category"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Optional[Dict[str, Any]]):
            """Handle tool calls"""
            try:
                if name == "get_game_status":
                    return await self._get_game_status()
                elif name == "list_3d_models":
                    return await self._list_3d_models(arguments.get("category") if arguments else None)
                elif name == "get_player_count":
                    return await self._get_player_count()
                elif name == "generate_content":
                    return await self._generate_content(arguments or {})
                elif name == "get_system_stats":
                    return await self._get_system_stats()
                elif name == "search_models":
                    return await self._search_models(arguments or {})
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _get_game_status(self):
        """Get overall game platform status"""
        try:
            # Count 3D models
            models_dir = self.game_root / "game_data" / "3d_models"
            model_count = 0
            if models_dir.exists():
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        model_count += len(list(category_dir.glob("*.glb")))
            
            status = {
                "platform": "3D Game Platform",
                "version": "1.0.0",
                "status": "running",
                "total_3d_models": model_count,
                "ai_services": ["luma", "meshy", "kaedim", "scenario"],
                "github_repository": "https://github.com/Scienceenviorment/3d-game-platform"
            }
            
            return [TextContent(type="text", text=json.dumps(status, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to get game status: {e}")
    
    async def _list_3d_models(self, category: Optional[str]):
        """List 3D models"""
        try:
            models_dir = self.game_root / "game_data" / "3d_models"
            models = []
            
            if category and (models_dir / category).exists():
                category_dir = models_dir / category
                for model_file in category_dir.glob("*.glb"):
                    models.append({
                        "name": model_file.name,
                        "category": category,
                        "size": model_file.stat().st_size
                    })
            elif models_dir.exists():
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        for model_file in category_dir.glob("*.glb"):
                            models.append({
                                "name": model_file.name,
                                "category": category_dir.name,
                                "size": model_file.stat().st_size
                            })
            
            result = {"models": models[:10], "count": len(models)}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to list 3D models: {e}")
    
    async def _get_player_count(self):
        """Get player count"""
        try:
            player_files = list(self.game_root.glob("game_data/player_*.json"))
            count = len(player_files)
            
            result = {"player_count": count, "active_players": count}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to get player count: {e}")
    
    async def _generate_content(self, arguments: Dict[str, Any]):
        """Generate procedural content"""
        try:
            content_type = arguments.get("content_type")
            count = arguments.get("count", 1)
            
            # Simulate procedural generation
            generated_items = []
            for i in range(count):
                if content_type == "beast":
                    item = {
                        "id": f"beast_{i+1:03d}",
                        "name": f"Mystical {content_type.title()} {i+1}",
                        "type": content_type,
                        "stats": {"health": 100, "attack": 50, "defense": 30},
                        "generated_at": datetime.now().isoformat()
                    }
                elif content_type == "weapon":
                    item = {
                        "id": f"weapon_{i+1:03d}",
                        "name": f"Legendary {content_type.title()} {i+1}",
                        "type": content_type,
                        "stats": {"damage": 75, "durability": 100, "rarity": "epic"},
                        "generated_at": datetime.now().isoformat()
                    }
                elif content_type == "divine_entity":
                    item = {
                        "id": f"divine_{i+1:03d}",
                        "name": f"Sacred {content_type.replace('_', ' ').title()} {i+1}",
                        "type": content_type,
                        "stats": {"power": 150, "wisdom": 100, "blessing": "high"},
                        "generated_at": datetime.now().isoformat()
                    }
                else:
                    item = {"error": f"Unknown content type: {content_type}"}
                
                generated_items.append(item)
            
            result = {
                "generated_content": generated_items,
                "count": len(generated_items),
                "content_type": content_type
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to generate content: {e}")
    
    async def _get_system_stats(self):
        """Get detailed system statistics"""
        try:
            models_dir = self.game_root / "game_data" / "3d_models"
            
            # Count models by category
            model_stats = {}
            total_models = 0
            total_size = 0
            
            if models_dir.exists():
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        models = list(category_dir.glob("*.glb"))
                        category_count = len(models)
                        category_size = sum(m.stat().st_size for m in models)
                        
                        model_stats[category_dir.name] = {
                            "count": category_count,
                            "size_bytes": category_size,
                            "size_mb": round(category_size / (1024*1024), 2)
                        }
                        total_models += category_count
                        total_size += category_size
            
            # Get player files
            player_files = list(self.game_root.glob("game_data/player_*.json"))
            
            stats = {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "total_3d_models": total_models,
                    "total_size_mb": round(total_size / (1024*1024), 2),
                    "active_players": len(player_files),
                    "categories": len(model_stats)
                },
                "models_by_category": model_stats,
                "platform_info": {
                    "version": "1.0.0",
                    "mcp_server": "enhanced",
                    "features": ["procedural_generation", "ai_3d_models", "karma_system"]
                }
            }
            
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to get system stats: {e}")
    
    async def _search_models(self, arguments: Dict[str, Any]):
        """Search 3D models by query"""
        try:
            query = arguments.get("query", "").lower()
            category_filter = arguments.get("category")
            
            models_dir = self.game_root / "game_data" / "3d_models"
            matching_models = []
            
            if models_dir.exists():
                for category_dir in models_dir.iterdir():
                    if category_dir.is_dir() and category_dir.name != "cache":
                        # Skip if category filter specified and doesn't match
                        if category_filter and category_dir.name != category_filter:
                            continue
                            
                        for model_file in category_dir.glob("*.glb"):
                            # Search in filename
                            if query in model_file.name.lower():
                                matching_models.append({
                                    "name": model_file.name,
                                    "category": category_dir.name,
                                    "size": model_file.stat().st_size,
                                    "path": str(model_file.relative_to(self.game_root))
                                })
            
            result = {
                "query": query,
                "category_filter": category_filter,
                "matches": matching_models[:20],  # Limit results
                "total_matches": len(matching_models)
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            raise Exception(f"Failed to search models: {e}")

async def main():
    """Run the simple MCP server"""
    print("🚀 Starting Simple 3D Game Platform MCP Server...")
    
    try:
        server_instance = Simple3DGameMCPServer()
        print("✅ Simple MCP Server instance created successfully!")
        
        # Run the server using stdio
        import sys
        from mcp.server.stdio import stdio_server
        
        print("📡 Simple MCP Server is running and ready!")
        async with stdio_server() as (read_stream, write_stream):
            from mcp.server.models import InitializationOptions
            from mcp.types import ServerCapabilities
            
            capabilities = ServerCapabilities(
                tools={}
            )
            
            await server_instance.server.run(
                read_stream, 
                write_stream,
                InitializationOptions(
                    server_name="3d-game-platform",
                    server_version="1.0.0",
                    capabilities=capabilities
                )
            )
            
    except Exception as e:
        print(f"❌ Error starting simple MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎮 Starting Simple MCP Server...")
    asyncio.run(main())