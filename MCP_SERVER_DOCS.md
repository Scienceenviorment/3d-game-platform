# MCP Server Documentation for 3D Game Platform

## Overview

The Model Context Protocol (MCP) server provides a comprehensive interface to interact with the 3D Game Platform through standardized tools and APIs. This allows AI systems, development tools, and external applications to seamlessly integrate with the game platform.

## Features

### 🎮 Core Game Integration
- Real-time game status monitoring
- Player data management
- 3D model asset access
- Procedural content generation
- System statistics and analytics

### 🔧 Available MCP Tools

#### 1. `get_game_status`
**Description:** Get overall game platform status and statistics
**Parameters:** None
**Returns:** Platform information including model counts, player statistics, and system status

**Example Response:**
```json
{
  "platform": "3D Game Platform",
  "version": "1.0.0", 
  "status": "running",
  "total_3d_models": 327,
  "ai_services": ["luma", "meshy", "kaedim", "scenario"],
  "github_repository": "https://github.com/Scienceenviorment/3d-game-platform"
}
```

#### 2. `list_3d_models`
**Description:** List available 3D models with optional category filtering
**Parameters:**
- `category` (optional): Filter by model category (beasts, weapons, environments, etc.)

**Returns:** List of 3D models with metadata

**Example Response:**
```json
{
  "models": [
    {
      "name": "beast_001_luma.glb",
      "category": "beasts",
      "size": 2048576
    }
  ],
  "count": 327
}
```

#### 3. `get_player_count`
**Description:** Get number of active players in the system
**Parameters:** None
**Returns:** Player count and activity statistics

#### 4. `generate_content`
**Description:** Generate procedural game content using the platform's systems
**Parameters:**
- `content_type`: Type of content ("beast", "weapon", "divine_entity")
- `count` (optional): Number of items to generate (1-5, default: 1)

**Returns:** Generated content with stats and metadata

**Example Response:**
```json
{
  "generated_content": [
    {
      "id": "beast_001",
      "name": "Mystical Beast 1",
      "type": "beast",
      "stats": {"health": 100, "attack": 50, "defense": 30},
      "generated_at": "2025-10-26T01:00:00"
    }
  ],
  "count": 1,
  "content_type": "beast"
}
```

#### 5. `get_system_stats`
**Description:** Get detailed system statistics and performance metrics
**Parameters:** None
**Returns:** Comprehensive system statistics including model counts by category, file sizes, and platform info

**Example Response:**
```json
{
  "timestamp": "2025-10-26T01:00:00",
  "system": {
    "total_3d_models": 327,
    "total_size_mb": 150.5,
    "active_players": 3,
    "categories": 5
  },
  "models_by_category": {
    "beasts": {"count": 120, "size_bytes": 50331648, "size_mb": 48.0},
    "weapons": {"count": 80, "size_bytes": 33554432, "size_mb": 32.0}
  },
  "platform_info": {
    "version": "1.0.0",
    "mcp_server": "enhanced",
    "features": ["procedural_generation", "ai_3d_models", "karma_system"]
  }
}
```

#### 6. `search_models`
**Description:** Search 3D models by name or properties
**Parameters:**
- `query`: Search query for model names
- `category` (optional): Filter by specific category

**Returns:** Matching models with metadata

## Quick Start

### 1. Start the MCP Server
```bash
python simple_mcp_server.py
```

### 2. Connect MCP Client
The server runs on stdio and can be connected to by any MCP-compatible client.

### 3. Configuration
Update `mcp_config.json` for custom configurations:
```json
{
  "mcpServers": {
    "3d-game-platform": {
      "command": "python",
      "args": ["simple_mcp_server.py"],
      "env": {"PYTHONPATH": "."},
      "cwd": "path/to/3d-game-platform"
    }
  }
}
```

## Development

### Requirements
- Python 3.11+
- MCP SDK 1.19.0+
- Game platform dependencies (see `mcp_requirements.txt`)

### Installation
```bash
pip install -r mcp_requirements.txt
```

### Testing
Use the test script to verify MCP server functionality:
```bash
python test_mcp.py
```

## Integration Examples

### Using with Claude/AI Systems
The MCP server can be connected to AI systems like Claude Desktop to provide game context and tools for AI-assisted game development.

### Custom Tool Development
Extend the server by adding new tools to the `_setup_tools()` method:

```python
Tool(
    name="custom_tool",
    description="Your custom functionality",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
)
```

## Error Handling

The MCP server includes comprehensive error handling:
- Tool execution errors are captured and returned as error responses
- Connection issues are logged for debugging
- Invalid parameters trigger validation errors

## Performance

- **Startup Time:** ~2 seconds
- **Response Time:** <100ms for most operations
- **Memory Usage:** ~50MB baseline
- **Concurrent Connections:** Supports multiple MCP clients

## Troubleshooting

### Common Issues

1. **MCP Server Won't Start**
   - Check Python version (3.11+ required)
   - Verify all dependencies installed
   - Ensure proper working directory

2. **Tool Execution Errors**
   - Check game data directory exists
   - Verify file permissions
   - Review error logs for details

3. **Connection Issues**
   - Confirm MCP client configuration
   - Check stdio communication setup
   - Verify server is running

## Future Enhancements

Planned improvements:
- Real-time event streaming
- WebSocket support for live updates
- Advanced AI model creation tools
- Player action monitoring
- Custom game rule engine integration

## Support

For issues and questions:
- Check the GitHub repository: https://github.com/Scienceenviorment/3d-game-platform
- Review error logs for debugging information
- Test with `test_mcp.py` for basic functionality verification