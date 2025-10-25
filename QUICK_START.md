# Echoes of the Horizon - Quick Start Guide

## 🎮 Getting Started

### 1. Prerequisites
- Python 3.8+ installed on your system
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for package installation
- **Administrator privileges (recommended for full permissions)**

### 2. Full Permission Setup (Recommended)

**Windows (Run as Administrator):**
```batch
# Option 1: Double-click setup_permissions.bat
setup_permissions.bat

# Option 2: PowerShell (Run as Administrator)
PowerShell -ExecutionPolicy Bypass -File setup_permissions.ps1

# Option 3: Python permission setup
python setup_permissions.py
```

**Linux/Mac:**
```bash
# Run with sudo for full permissions
sudo python3 setup_permissions.py

# Or run without sudo (limited permissions)
python3 setup_permissions.py
```

### 3. Quick Installation (Basic Setup)
```bash
# Navigate to the game directory
cd 3d-game-platform

# Run the game launcher (it will install dependencies automatically)
python launch_game.py
```

### 3. Starting the Game
The launcher will:
- ✅ Check your Python version
- ✅ Install required packages (fastapi, uvicorn, websockets)
- ✅ Verify all game files are present
- 🚀 Start the server

### 4. Playing the Game
1. **Start Server**: Run `python launch_game.py` and press 'y'
2. **Open Client**: Open `client/index.html` in your web browser
3. **Enter Name**: Type your character name
4. **Start Exploring**: Begin your journey in Ancient Bharat!

## 🌍 Game Controls

### Movement
- **W, A, S, D** or **Arrow Keys**: Move around
- **Mouse**: Look around
- **Space**: Jump (if implemented)
- **Shift**: Sprint (if implemented)

### Interaction
- **Click NPCs**: Start conversations
- **Chat Box**: Type messages to other players
- **Quest Panel**: Track your current objectives
- **Inventory**: View collected items and progress

## 🗺️ Starting Your Journey

### Your First Steps
1. **Spawn Location**: You begin in Ocean Frontier, the coastal starting region
2. **Meet NPCs**: Look for Devraj the Ranger near the coastline
3. **Explore Regions**: Travel to different areas to unlock new content
4. **Collect Fragments**: Search for Sarasvati Map pieces in ancient sites

### Essential NPCs to Find
- **🏹 Devraj**: Ranger in Ocean Frontier - teaches survival skills
- **🕉️ Arunima**: Veda Scholar in Indrapura City - main quest giver
- **🏺 Rukmini**: Village Elder in Indrapura City - cultural quests

## 🎯 Quest System

### Main Quest: The Sarasvati Map
- **Goal**: Find 7 ancient map fragments scattered across all regions
- **Reward**: Massive experience and story completion
- **Difficulty**: Progressive from easy to legendary

### Side Quests
- **Village Building**: Help reconstruct traditional structures
- **Wilderness Training**: Learn survival from experienced rangers  
- **Cultural Discovery**: Translate ancient Sanskrit inscriptions
- **Daily Tasks**: Repeatable activities for steady progress

## 📊 Monitoring Your Server

### Web Endpoints (while server is running)
- **Server Status**: http://localhost:8000/status
- **Connected Players**: http://localhost:8000/players  
- **World Statistics**: http://localhost:8000/world/stats
- **Admin Save**: http://localhost:8000/admin/save (POST request)

### Server Console
Watch the server console for:
- Player connections and disconnections
- Quest completions and progress
- Auto-save notifications
- Error messages and debugging info

## 🛠️ Configuration Options

### Server Settings
Edit `server/config/server_config.json`:
```json
{
    "host": "0.0.0.0",
    "port": 8000,
    "max_players": 100,
    "auto_save_interval": 300
}
```

### World Generation  
Edit `server/config/world_config.json`:
```json
{
    "terrain_seed": 12345,
    "max_elevation": 100.0,
    "weather_change_interval": 1800
}
```

### Quest Configuration
Edit `server/config/quest_config.json`:
```json
{
    "sarasvati_fragments_total": 7,
    "fragment_reward_xp": 1000,
    "side_quest_reward_xp": 250
}
```

## 🚨 Troubleshooting

### Permission Issues

**"Access Denied" or "Permission Denied" errors**
```bash
# Windows: Run as Administrator
# Right-click Command Prompt/PowerShell -> "Run as Administrator"
python setup_permissions.py

# Linux/Mac: Use sudo
sudo python3 setup_permissions.py
```

**"Port already in use" errors**
```bash
# Check what's using port 8000
netstat -an | findstr :8000  # Windows  
lsof -i :8000                # Mac/Linux

# Kill process using the port (Windows)
taskkill /PID <process_id> /F

# Kill process using the port (Linux/Mac)
sudo kill -9 <process_id>
```

### Common Issues

**"Module not found" errors**
```bash
# Install missing packages manually
pip install fastapi uvicorn websockets

# If that fails, try:
pip install --user fastapi uvicorn websockets

# Python 3.11+ may need:
pip install --user --break-system-packages fastapi uvicorn websockets
```

**Server won't start**
```bash
# Check if port 8000 is available
netstat -an | findstr :8000  # Windows
lsof -i :8000                # Mac/Linux

# Try alternative port (edit simple_game_server.py)
# Change port=8000 to port=8080
```

**Firewall blocking connections**
```bash
# Windows: Allow Python through firewall
# Go to Windows Defender Firewall -> Allow an app
# Add python.exe to allowed apps

# Or run the permission setup:
python setup_permissions.py
```

**Can't connect to server**
- Ensure server is running (check console output)
- Try refreshing the browser page
- Check browser console for WebSocket errors (F12)
- Disable browser extensions that might block WebSockets
- Try incognito/private browsing mode

**Game runs slowly**
- Close other browser tabs
- Check server console for performance warnings
- Reduce world generation settings if needed
- Restart the server periodically

### Getting Help

1. **Check Server Logs**: Look at console output for error messages
2. **Browser Console**: Press F12 and check for JavaScript errors
3. **Network Issues**: Ensure WebSocket connections aren't blocked
4. **File Permissions**: Make sure Python can read/write game files

## 🎨 Customization

### Adding Your Own Content

**New NPCs**: Edit `server/ancient_bharat_npcs.py`
- Add new NPC classes inheriting from BaseNPC
- Define personality, schedule, and dialogue

**Custom Quests**: Edit `server/ancient_bharat_quests.py`  
- Create new Quest objects with objectives
- Add to quest system initialization

**World Objects**: Edit `server/ancient_bharat_world.py`
- Define new cultural objects with Sanskrit names
- Add to biome-specific generation lists

### Client Customization
**UI Styling**: Edit `client/index.html`
- Modify CSS for different color schemes
- Add new UI elements and panels
- Customize chat and quest displays

## 🌟 Advanced Features

### Multiplayer Testing
1. Open multiple browser windows/tabs
2. Each needs a unique player name
3. Test chat, movement, and quest sharing
4. Monitor server console for multi-player interactions

### Data Persistence
- Player progress automatically saved every 5 minutes
- Manual save: Visit http://localhost:8000/admin/save
- Data stored in `server/game_data/` directory
- Configuration in `server/config/` directory

### Performance Monitoring
- Watch server console for memory usage
- Monitor world generation statistics
- Check player connection stability
- Review auto-save completion messages

## 🎉 Have Fun!

You're now ready to explore the mystical world of Ancient Bharat! 

**Discover ancient wisdom, complete epic quests, and share the adventure with friends in this unique cultural gaming experience.**

*"सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः"*  
*"May all beings be happy, may all beings be free from illness"*

---

**Need help?** Check the full README_complete.md for detailed technical information!