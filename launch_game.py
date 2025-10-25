#!/usr/bin/env python3
"""
Echoes of the Horizon - Game Launcher
Simple Python script to start the complete Ancient Bharat server
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def print_banner():
    """Display game banner"""
    print("=" * 60)
    print("🏛️  ECHOES OF THE HORIZON - ANCIENT BHARAT  🏛️")
    print("    Complete 3D Multiplayer Exploration Game")
    print("=" * 60)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "websockets"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True


def check_game_files():
    """Check if all game files are present"""
    server_dir = Path("server")
    required_files = [
        "ancient_bharat_config.py",
        "ancient_bharat_npcs.py", 
        "ancient_bharat_quests.py",
        "ancient_bharat_world.py",
        "integrated_ancient_bharat_server.py"
    ]
    
    missing_files = []
    
    for filename in required_files:
        file_path = server_dir / filename
        if file_path.exists():
            print(f"✅ {filename}")
        else:
            missing_files.append(filename)
            print(f"❌ {filename} missing")
    
    if missing_files:
        print(f"\n❌ Missing game files: {', '.join(missing_files)}")
        print("   Please ensure all game files are in the server/ directory")
        return False
    
    return True


def start_server():
    """Start the integrated Ancient Bharat server"""
    server_dir = Path("server")
    server_file = server_dir / "integrated_ancient_bharat_server.py"
    
    print("\n🚀 Starting Echoes of the Horizon server...")
    print("   Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Change to server directory
        os.chdir(server_dir)
        
        # Start the server
        subprocess.run([sys.executable, "integrated_ancient_bharat_server.py"])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except FileNotFoundError:
        print(f"❌ Server file not found: {server_file}")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def show_connection_info():
    """Show how to connect to the game"""
    print("\n🌐 Connection Information:")
    print("   Server URL: http://localhost:8000")
    print("   Game Client: Open client/index.html in your browser")
    print("   WebSocket: ws://localhost:8000/ws/{player_id}")
    print("\n📊 Monitoring Endpoints:")
    print("   Status: http://localhost:8000/status")
    print("   Players: http://localhost:8000/players")
    print("   World Stats: http://localhost:8000/world/stats")


def main():
    """Main launcher function"""
    print_banner()
    
    print("\n🔍 System Check:")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check game files
    if not check_game_files():
        return
    
    print("\n✅ All systems ready!")
    
    # Show connection info
    show_connection_info()
    
    # Ask user if they want to start
    print("\n" + "=" * 60)
    response = input("🎮 Start Echoes of the Horizon server? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        start_server()
    else:
        print("👋 Launch cancelled. Run this script again when ready!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   Please check your installation and try again.")