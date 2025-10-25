# 🔐 Ancient Bharat - Complete Permission Guide

This guide ensures you have all necessary permissions to run the Ancient Bharat game without any issues.

## 🎯 Quick Start (Choose Your Method)

### Method 1: One-Click Windows Setup (Easiest)
1. **Right-click on `setup_permissions.bat`**
2. **Select "Run as administrator"**
3. **Follow the prompts**
4. **Done! Game ready to play**

### Method 2: PowerShell Setup (Advanced Windows)
1. **Right-click PowerShell** → **"Run as administrator"**
2. **Run:** `PowerShell -ExecutionPolicy Bypass -File setup_permissions.ps1`
3. **Follow the prompts**
4. **Game will auto-launch**

### Method 3: Python Setup (Cross-Platform)
```bash
# Windows (as Administrator)
python setup_permissions.py

# Linux/Mac (with sudo)
sudo python3 setup_permissions.py
```

### Method 4: Manual Setup (If automatic fails)
See the "Manual Permission Setup" section below.

## 🔍 What Permissions Are Needed?

### File System Permissions
- **Read/Write access** to game directory
- **Create directories** for game_data, config, logs
- **Execute permissions** on Python files
- **Temporary file access** for game state saving

### Network Permissions  
- **Bind to ports** 8000 and 8080 (game server)
- **Firewall exceptions** for Python.exe
- **WebSocket connections** for real-time multiplayer
- **Local network access** for browser connections

### System Permissions
- **Install Python packages** (FastAPI, uvicorn, websockets)
- **PowerShell execution policy** (Windows)
- **Process creation** for server startup
- **Registry access** (Windows, for some operations)

## 🛠️ Manual Permission Setup

If the automatic scripts don't work, follow these manual steps:

### Windows Manual Setup

#### 1. File Permissions
```cmd
# Open Command Prompt as Administrator
# Navigate to game directory
cd "C:\path\to\3d-game-platform"

# Grant full permissions to your user
icacls . /grant "%USERNAME%":F /T

# Grant permissions to Everyone (if needed)
icacls . /grant "Everyone":F /T
```

#### 2. Firewall Permissions
```cmd
# Add firewall rules (as Administrator)
netsh advfirewall firewall add rule name="Ancient Bharat (In)" dir=in action=allow program="%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" enable=yes

netsh advfirewall firewall add rule name="Ancient Bharat (Out)" dir=out action=allow program="%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" enable=yes
```

**Note:** Replace Python path with your actual Python installation path.

#### 3. PowerShell Execution Policy
```powershell
# In PowerShell (as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

#### 4. Install Packages
```cmd
# Install required packages
python -m pip install --user fastapi uvicorn[standard] websockets

# If that fails, try:
python -m pip install --user --break-system-packages fastapi uvicorn[standard] websockets
```

### Linux/Mac Manual Setup

#### 1. File Permissions
```bash
# Navigate to game directory
cd /path/to/3d-game-platform

# Set directory permissions
chmod -R 755 .

# Make Python files executable
chmod +x *.py
```

#### 2. Firewall/Port Access
```bash
# Ubuntu/Debian: Allow port 8000
sudo ufw allow 8000

# CentOS/RHEL: Allow port 8000
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# macOS: No additional firewall config usually needed
```

#### 3. Install Packages
```bash
# Install packages for current user
python3 -m pip install --user fastapi uvicorn[standard] websockets

# Or system-wide (with sudo)
sudo python3 -m pip install fastapi uvicorn[standard] websockets
```

## 🧪 Testing Your Permissions

### Run Permission Test
```bash
python test_permissions.py
```

This will test:
- ✅ File read/write permissions
- ✅ Network socket creation and binding
- ✅ Required module imports
- ✅ Directory creation capabilities

### Manual Tests

#### Test 1: File Permissions
```python
# Create a test file
import json
test_data = {"test": True}
with open("test_file.json", "w") as f:
    json.dump(test_data, f)

# If this works without error, file permissions are OK
```

#### Test 2: Network Permissions
```python
# Test port binding
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.close()
# If this works without error, network permissions are OK
```

#### Test 3: Package Installation
```python
# Test imports
import fastapi
import uvicorn
import websockets
print("All packages available!")
```

## 🚨 Common Permission Problems & Solutions

### Problem: "Access Denied" when creating files
**Solution:**
```bash
# Windows
icacls . /grant "%USERNAME%":F /T

# Linux/Mac
chmod -R 755 .
sudo chown -R $USER:$USER .
```

### Problem: "Port 8000 already in use"
**Solution:**
```bash
# Find what's using the port
netstat -an | findstr :8000  # Windows
lsof -i :8000               # Linux/Mac

# Kill the process
taskkill /PID <pid> /F      # Windows
sudo kill -9 <pid>          # Linux/Mac

# Or use alternative port (edit simple_game_server.py)
# Change: uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Problem: "Module not found" even after installation
**Solution:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install to user directory
python -m pip install --user <package>

# Force install (Python 3.11+)
python -m pip install --user --break-system-packages <package>

# Check installed packages
python -m pip list
```

### Problem: Firewall blocking connections
**Solution:**

**Windows:**
1. Windows Defender Firewall → Allow an app
2. Click "Change Settings" → "Allow another app"
3. Browse to your Python.exe
4. Check both "Private" and "Public" networks

**Linux:**
```bash
sudo ufw allow 8000
sudo ufw status
```

**Mac:**
```bash
# Usually no additional config needed
# If issues: System Preferences → Security & Privacy → Firewall
```

### Problem: PowerShell execution policy (Windows)
**Solution:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set to allow local scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for one session
PowerShell -ExecutionPolicy Bypass -File script.ps1
```

## 🎮 Verify Everything Works

### Final Test Sequence
1. **Run permission test:** `python test_permissions.py`
2. **Start game server:** `python simple_game_server.py`
3. **Check server responds:** Visit `http://localhost:8000/status`
4. **Open game client:** Visit `http://localhost:8000/client`
5. **Test multiplayer:** Open client in multiple browser tabs

### Success Indicators
- ✅ Server starts without errors
- ✅ Browser can connect to http://localhost:8000
- ✅ WebSocket connection established (check browser console F12)
- ✅ Can move around and chat in game
- ✅ Game data saves without errors

## 📞 Still Having Issues?

### Debug Information to Collect
1. **Operating System:** Windows/Linux/Mac version
2. **Python Version:** `python --version`
3. **Error Messages:** Full text of any error messages
4. **Permissions Test Results:** Output from `test_permissions.py`
5. **Port Status:** Output from `netstat -an | findstr :8000`
6. **Firewall Status:** Windows Defender or system firewall settings

### Alternative Solutions
1. **Use different port:** Edit `simple_game_server.py` to use port 8080 or 9000
2. **Run in virtual environment:** Create isolated Python environment
3. **Use portable Python:** Download portable Python distribution
4. **Container solution:** Run in Docker (advanced users)

## 🎯 Quick Reference Commands

### Windows
```cmd
# Full setup (as Administrator)
setup_permissions.bat

# Quick test
python test_permissions.py

# Start game
python simple_game_server.py
```

### Linux/Mac
```bash
# Full setup
sudo python3 setup_permissions.py

# Quick test  
python3 test_permissions.py

# Start game
python3 simple_game_server.py
```

---

**🎮 Once permissions are set up correctly, you'll have full access to the mystical world of Ancient Bharat!**

*Experience the wisdom of ages with complete system permissions.*