#!/usr/bin/env python3
"""
Simple Setup Script for Echoes of the Horizon
One-command installation and launcher
No Git, no complexity, just pure Ancient Bharat adventure!
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path


def print_header():
    """Print game header"""
    print("🏛️" + "=" * 58 + "🏛️")
    print("   ECHOES OF THE HORIZON - ANCIENT BHARAT SETUP")  
    print("🏛️" + "=" * 58 + "🏛️")
    print()


def check_python():
    """Check Python version"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   Current: {sys.version}")
        print("   Please install Python 3.8+ from python.org")
        return False
    
    major, minor = sys.version_info[:2]
    print(f"✅ Python {major}.{minor} detected")
    return True


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing game dependencies...")
    
    required = ["fastapi", "uvicorn[standard]", "websockets"]
    
    for package in required:
        print(f"   Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ])
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
            return False
    
    print("✅ All dependencies installed!")
    return True


def check_game_files():
    """Check if game server file exists"""
    print("\n🎮 Checking game files...")
    
    server_file = Path("simple_game_server.py")
    
    if server_file.exists():
        print("✅ Game server found")
        return True
    else:
        print("❌ simple_game_server.py not found")
        print("   Please ensure the game file is in this directory")
        return False


def start_server():
    """Start the game server"""
    print("\n🚀 Starting Echoes of the Horizon server...")
    print("   Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        # Start server
        subprocess.run([sys.executable, "simple_game_server.py"])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        print("Thanks for playing Echoes of the Horizon!")
        
    except FileNotFoundError:
        print("❌ Could not start server")
        print("   Make sure simple_game_server.py exists")


def open_game_client():
    """Open game client in browser"""
    print("🌐 Opening game client...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        webbrowser.open("http://localhost:8000/client")
        print("✅ Game client opened in browser")
    except:
        print("⚠️ Could not auto-open browser")
        print("   Manually visit: http://localhost:8000/client")


def show_info():
    """Show game information"""
    print("\n" + "=" * 60)
    print("🎮 ANCIENT BHARAT ADVENTURE AWAITS!")
    print("=" * 60)
    print("🌐 Game Client: http://localhost:8000/client")
    print("📊 Server Status: http://localhost:8000/status")
    print("🔧 Admin Save: http://localhost:8000/admin/save")
    print()
    print("🗺️ Five Mystical Regions to explore:")
    print("   🏜️ Dust Plains - Ancient desert ruins")
    print("   🏔️ Himalayan Peaks - Sacred mountains")
    print("   🏛️ Indrapura City - Cultural center")
    print("   🌲 Narmada Forest - Mystical woodlands")
    print("   🌊 Ocean Frontier - Starting coastline")
    print()
    print("👥 Meet the Wise NPCs:")
    print("   🕉️ Arunima - Veda Scholar")
    print("   🏹 Devraj - Forest Ranger") 
    print("   🏺 Rukmini - Village Elder")
    print()
    print("📜 Epic Quests:")
    print("   🗺️ Find the lost Sarasvati Map fragments")
    print("   🌿 Learn wilderness survival skills")
    print("   🏘️ Help preserve ancient traditions")
    print("=" * 60)


def main():
    """Main setup function"""
    print_header()
    
    # System checks
    if not check_python():
        input("Press Enter to exit...")
        return
    
    if not install_dependencies():
        input("Press Enter to exit...")
        return
    
    if not check_game_files():
        input("Press Enter to exit...")
        return
    
    # Show game info
    show_info()
    
    # Ask to start
    print("\n🎯 Ready to begin your Ancient Bharat adventure?")
    choice = input("Start server? (Y/n): ").lower().strip()
    
    if choice in ['', 'y', 'yes']:
        # Start server in background and open client
        print("\n🚀 Starting your journey...")
        
        # Option to open browser automatically
        auto_open = input("Open game client automatically? (Y/n): ").lower().strip()
        if auto_open in ['', 'y', 'yes']:
            # Start server in a way that allows browser to open
            import threading
            
            def start_server_thread():
                start_server()
            
            server_thread = threading.Thread(target=start_server_thread)
            server_thread.daemon = True
            server_thread.start()
            
            # Open browser
            open_game_client()
            
            # Keep main thread alive
            try:
                print("\n🎮 Game running! Check your browser.")
                print("   Press Ctrl+C to stop the server")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Shutting down...")
        else:
            start_server()
    
    else:
        print("\n👋 Setup complete! Run this script again to start.")
        print("Or manually run: python simple_game_server.py")


def install_mode():
    """Install-only mode"""
    print_header()
    print("📦 INSTALLATION MODE")
    print()
    
    if not check_python():
        return False
        
    return install_dependencies()


def quick_start():
    """Quick start mode (skip checks)"""
    print_header()
    print("⚡ QUICK START MODE")
    print()
    
    show_info()
    
    print("\n🚀 Starting server...")
    start_server()


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['install', 'i']:
            # Install dependencies only
            if install_mode():
                print("\n✅ Installation complete!")
            else:
                print("\n❌ Installation failed!")
                
        elif arg in ['start', 's', 'run']:
            # Quick start (skip setup)
            quick_start()
            
        elif arg in ['help', 'h', '--help']:
            # Show help
            print("Echoes of the Horizon Setup")
            print()
            print("Usage:")
            print("  python simple_setup.py         # Full setup and start")
            print("  python simple_setup.py install # Install dependencies only")  
            print("  python simple_setup.py start   # Quick start (skip setup)")
            print("  python simple_setup.py help    # Show this help")
            print()
            
        else:
            print(f"Unknown command: {arg}")
            print("Use 'python simple_setup.py help' for usage info")
    
    else:
        # Default: full setup
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n👋 Setup cancelled!")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again or check your Python installation")
            input("Press Enter to exit...")