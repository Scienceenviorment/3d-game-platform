#!/usr/bin/env python3
"""
Development server launcher for 3D Game Platform
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing server dependencies...")
    requirements_file = Path("server/requirements.txt")
    
    if requirements_file.exists():
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    else:
        print("❌ requirements.txt not found")
        return False

def start_game_server():
    """Start the game server"""
    print("🚀 Starting game server...")
    server_script = Path("server/main.py")
    
    if server_script.exists():
        try:
            # Change to server directory
            os.chdir("server")
            
            # Start the server
            process = subprocess.Popen([
                sys.executable, "main.py"
            ])
            
            print("✅ Game server started on http://localhost:8000")
            return process
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return None
    else:
        print("❌ Server script not found")
        return None

def start_client_server():
    """Start a simple HTTP server for the client"""
    print("🌐 Starting client server...")
    client_dir = Path("client")
    
    if client_dir.exists():
        try:
            os.chdir(str(client_dir.absolute()))
            
            # Start HTTP server
            process = subprocess.Popen([
                sys.executable, "-m", "http.server", "8080"
            ])
            
            print("✅ Client server started on http://localhost:8080")
            return process
        except Exception as e:
            print(f"❌ Failed to start client server: {e}")
            return None
    else:
        print("❌ Client directory not found")
        return None

def main():
    """Main development server launcher"""
    print("🎮 3D Game Platform - Development Server Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n💡 Try running: pip install -r server/requirements.txt")
        sys.exit(1)
    
    # Go back to project root
    os.chdir(Path(__file__).parent)
    
    # Start servers
    print("\n🚀 Starting servers...")
    
    game_server = start_game_server()
    if not game_server:
        sys.exit(1)
    
    # Give server a moment to start
    time.sleep(2)
    
    # Go back to project root for client server
    os.chdir(Path(__file__).parent)
    
    client_server = start_client_server()
    if not client_server:
        if game_server:
            game_server.terminate()
        sys.exit(1)
    
    # Wait a moment then open browser
    time.sleep(2)
    print("\n🌐 Opening game in browser...")
    webbrowser.open("http://localhost:8080")
    
    print("\n" + "=" * 50)
    print("🎮 Game Platform Running!")
    print("📊 Game Server: http://localhost:8000")
    print("🎯 Game Client: http://localhost:8080")
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("\n💡 Press Ctrl+C to stop all servers")
    print("=" * 50)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        
        if game_server:
            game_server.terminate()
            print("✅ Game server stopped")
        
        if client_server:
            client_server.terminate()
            print("✅ Client server stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()