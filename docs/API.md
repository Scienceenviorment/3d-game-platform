# API Documentation

## WebSocket Protocol

The game uses WebSocket communication for real-time multiplayer interaction.

### Connection Endpoint
```
ws://localhost:8000/ws
```

### Message Types

#### Client to Server Messages

**Connection Message**
```json
{
    "type": "connect",
    "player_id": "unique_player_id",
    "player_name": "Player Name"
}
```

**Movement Message**
```json
{
    "type": "move",
    "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    },
    "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    }
}
```

**Chat Message**
```json
{
    "type": "chat",
    "message": "Hello world!"
}
```

#### Server to Client Messages

**Welcome Message**
```json
{
    "type": "welcome",
    "player_id": "your_player_id",
    "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    }
}
```

**Player Joined**
```json
{
    "type": "player_joined",
    "player": {
        "id": "player_id",
        "name": "Player Name",
        "position": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        }
    }
}
```

**Player Left**
```json
{
    "type": "player_left",
    "player_id": "player_id"
}
```

**Player Moved**
```json
{
    "type": "player_moved",
    "player_id": "player_id",
    "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    },
    "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
    }
}
```

**Chat Message**
```json
{
    "type": "chat",
    "player_id": "sender_id",
    "player_name": "Sender Name",
    "message": "Chat message content"
}
```

## REST API Endpoints

### Server Info
```
GET /
```
Returns server information and player count.

### World Chunks
```
GET /world/chunk/{chunk_x}/{chunk_z}
```
Returns terrain and object data for a specific world chunk.

**Response:**
```json
{
    "x": 0,
    "z": 0,
    "terrain": [[height_values]],
    "objects": [
        {
            "type": "tree",
            "x": 5,
            "z": 8,
            "y": 0,
            "scale": 1.5
        }
    ]
}
```

## Data Structures

### Vector3
```json
{
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
}
```

### Player
```json
{
    "id": "unique_player_id",
    "name": "Player Name",
    "position": Vector3,
    "rotation": Vector3,
    "last_update": 1634567890.123
}
```

### World Object
```json
{
    "type": "tree|rock|bush",
    "x": 0,
    "z": 0,
    "y": 0,
    "scale": 1.0
}
```