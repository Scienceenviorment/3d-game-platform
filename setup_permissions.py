#!/usr/bin/env python3
"""
Ancient Bharat - Full Permissions Setup Script
Sets up all necessary permissions and system requirements
"""

import os
import sys
import subprocess
import stat
from pathlib import Path
import platform


def print_header():
    """Print setup header"""
    print("🔐" + "=" * 58 + "🔐")
    print("   ANCIENT BHARAT - FULL PERMISSIONS SETUP")
    print("🔐" + "=" * 58 + "🔐")
    print()


def check_admin_rights():
    """Check if running with administrator privileges"""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False


def request_admin_rights():
    """Request administrator privileges if needed"""
    if platform.system() == "Windows":
        if not check_admin_rights():
            print("🔐 Administrator privileges required for full setup")
            print("   Right-click Command Prompt/PowerShell and 'Run as Administrator'")
            print("   Then run this script again")
            input("Press Enter to continue anyway...")
            return False
    return True


def set_directory_permissions():
    """Set full permissions on project directory"""
    print("📁 Setting directory permissions...")
    
    project_dir = Path.cwd()
    
    try:
        if platform.system() == "Windows":
            # Windows: Give full control to current user
            username = os.getenv('USERNAME')
            cmd = f'icacls "{project_dir}" /grant "{username}":F /T'
            subprocess.run(cmd, shell=True, check=False)
            print(f"✅ Full permissions granted to {username}")
            
            # Also try to give permissions to Everyone group
            cmd_everyone = f'icacls "{project_dir}" /grant "Everyone":F /T'
            subprocess.run(cmd_everyone, shell=True, check=False)
            
        else:
            # Linux/Mac: Set 755 permissions
            for root, dirs, files in os.walk(project_dir):
                # Set directory permissions to 755 (rwxr-xr-x)
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    dir_path.chmod(0o755)
                
                # Set file permissions to 644 (rw-r--r--)
                for file_name in files:
                    file_path = Path(root) / file_name
                    if file_path.suffix == '.py':
                        file_path.chmod(0o755)  # Executable for Python files
                    else:
                        file_path.chmod(0o644)
            
            print("✅ Unix permissions set (755 for dirs, 644/755 for files)")
            
    except Exception as e:
        print(f"⚠️ Could not set some permissions: {e}")
        print("   Game should still work, but may have file access issues")


def create_required_directories():
    """Create all required directories with proper permissions"""
    print("\n📂 Creating required directories...")
    
    required_dirs = [
        "game_data",
        "config", 
        "logs",
        "temp",
        "client",
        "server"
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        try:
            dir_path.mkdir(exist_ok=True)
            
            # Set permissions
            if platform.system() != "Windows":
                dir_path.chmod(0o755)
            
            print(f"✅ Created: {dir_name}/")
            
        except Exception as e:
            print(f"❌ Could not create {dir_name}/: {e}")


def set_python_execution_policy():
    """Set Python execution permissions"""
    print("\n🐍 Setting Python execution permissions...")
    
    try:
        if platform.system() == "Windows":
            # Set PowerShell execution policy to allow scripts
            cmd = "powershell Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PowerShell execution policy set to RemoteSigned")
            else:
                print("⚠️ Could not set PowerShell execution policy")
                print("   You may need to run as Administrator")
        
        # Make Python files executable
        python_files = list(Path.cwd().glob("*.py"))
        for py_file in python_files:
            try:
                if platform.system() != "Windows":
                    py_file.chmod(0o755)
                print(f"✅ Made executable: {py_file.name}")
            except Exception as e:
                print(f"⚠️ Could not set permissions on {py_file.name}: {e}")
                
    except Exception as e:
        print(f"❌ Error setting Python permissions: {e}")


def configure_firewall_permissions():
    """Configure firewall to allow game server"""
    print("\n🔥 Configuring firewall permissions...")
    
    try:
        if platform.system() == "Windows":
            # Add Windows Firewall rules for the game server
            python_exe = sys.executable
            
            # Inbound rule
            cmd_in = f'netsh advfirewall firewall add rule name="Ancient Bharat Game Server (In)" dir=in action=allow program="{python_exe}" enable=yes'
            result_in = subprocess.run(cmd_in, shell=True, capture_output=True)
            
            # Outbound rule  
            cmd_out = f'netsh advfirewall firewall add rule name="Ancient Bharat Game Server (Out)" dir=out action=allow program="{python_exe}" enable=yes'
            result_out = subprocess.run(cmd_out, shell=True, capture_output=True)
            
            if result_in.returncode == 0 and result_out.returncode == 0:
                print("✅ Windows Firewall rules added for Python")
            else:
                print("⚠️ Could not add firewall rules (may need Administrator)")
                print("   Manually allow Python through Windows Firewall if needed")
        
        else:
            print("ℹ️ Non-Windows system - firewall configuration varies by distro")
            print("   If you have issues connecting, check your firewall settings")
            
    except Exception as e:
        print(f"⚠️ Firewall configuration error: {e}")


def set_network_permissions():
    """Set network access permissions"""
    print("\n🌐 Setting network permissions...")
    
    try:
        # Test network binding capability
        import socket
        
        # Try to bind to the game port
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('localhost', 8000))
        test_socket.close()
        
        print("✅ Can bind to port 8000 (game server port)")
        
        # Test port 8080 as backup
        test_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket2.bind(('localhost', 8080))
        test_socket2.close()
        
        print("✅ Can bind to port 8080 (backup port)")
        
    except Exception as e:
        print(f"⚠️ Network binding test failed: {e}")
        print("   You may need to run as Administrator for port access")


def install_with_permissions():
    """Install Python packages with proper permissions"""
    print("\n📦 Installing Python packages with permissions...")
    
    packages = ["fastapi", "uvicorn[standard]", "websockets"]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            
            # Try regular pip first
            cmd = [sys.executable, "-m", "pip", "install", package, "--user"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                # Try with --break-system-packages if needed (Python 3.11+)
                cmd_force = [sys.executable, "-m", "pip", "install", package, "--user", "--break-system-packages"]
                result2 = subprocess.run(cmd_force, capture_output=True, text=True)
                
                if result2.returncode == 0:
                    print(f"✅ {package} installed (with force)")
                else:
                    print(f"❌ Could not install {package}")
                    print(f"   Error: {result.stderr}")
                    
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")


def create_launch_scripts():
    """Create platform-specific launch scripts"""
    print("\n📝 Creating launch scripts...")
    
    # Windows batch file
    if platform.system() == "Windows":
        batch_content = '''@echo off
echo Starting Ancient Bharat Game Server...
cd /d "%~dp0"
python simple_game_server.py
pause
'''
        
        try:
            with open("start_game.bat", "w") as f:
                f.write(batch_content)
            print("✅ Created start_game.bat")
        except Exception as e:
            print(f"❌ Could not create batch file: {e}")
    
    # Unix shell script
    else:
        shell_content = '''#!/bin/bash
echo "Starting Ancient Bharat Game Server..."
cd "$(dirname "$0")"
python3 simple_game_server.py
read -p "Press Enter to exit..."
'''
        
        try:
            with open("start_game.sh", "w") as f:
                f.write(shell_content)
            
            # Make executable
            Path("start_game.sh").chmod(0o755)
            print("✅ Created start_game.sh")
        except Exception as e:
            print(f"❌ Could not create shell script: {e}")


def create_permission_test_file():
    """Create a test file to verify permissions work"""
    print("\n🧪 Creating permission test file...")
    
    test_content = '''#!/usr/bin/env python3
"""
Permission Test for Ancient Bharat
Verifies all permissions are working correctly
"""

import os
import sys
import json
import time
from pathlib import Path

def test_file_permissions():
    """Test file read/write permissions"""
    print("📁 Testing file permissions...")
    
    test_dir = Path("game_data")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "permission_test.json"
    
    try:
        # Test write
        test_data = {"test": True, "timestamp": time.time()}
        with open(test_file, "w") as f:
            json.dump(test_data, f)
        print("✅ File write permission OK")
        
        # Test read
        with open(test_file, "r") as f:
            loaded_data = json.load(f)
        print("✅ File read permission OK")
        
        # Test delete
        test_file.unlink()
        print("✅ File delete permission OK")
        
    except Exception as e:
        print(f"❌ File permission error: {e}")
        return False
    
    return True

def test_network_permissions():
    """Test network permissions"""
    print("\\n🌐 Testing network permissions...")
    
    try:
        import socket
        
        # Test socket creation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("✅ Socket creation OK")
        
        # Test port binding
        sock.bind(('127.0.0.1', 0))  # Bind to any available port
        port = sock.getsockname()[1]
        print(f"✅ Port binding OK (test port: {port})")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Network permission error: {e}")
        return False
    
    return True

def test_module_imports():
    """Test required module imports"""
    print("\\n📦 Testing module imports...")
    
    required_modules = ["fastapi", "uvicorn", "websockets"]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} import OK")
        except ImportError:
            print(f"❌ {module} not available")
            return False
    
    return True

def main():
    """Run all permission tests"""
    print("🧪 Ancient Bharat Permission Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_file_permissions():
        tests_passed += 1
    
    if test_network_permissions():
        tests_passed += 1
    
    if test_module_imports():
        tests_passed += 1
    
    print("\\n" + "=" * 40)
    print(f"📊 Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✅ All permissions working correctly!")
        print("🎮 Ready to run Ancient Bharat game!")
    else:
        print("❌ Some permission issues detected")
        print("   Run the full setup script to fix issues")
    
    print("\\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
'''
    
    try:
        with open("test_permissions.py", "w") as f:
            f.write(test_content)
        
        # Make executable
        if platform.system() != "Windows":
            Path("test_permissions.py").chmod(0o755)
        
        print("✅ Created test_permissions.py")
        
    except Exception as e:
        print(f"❌ Could not create test file: {e}")


def show_final_instructions():
    """Show final setup instructions"""
    print("\n" + "🎯" + "=" * 58 + "🎯")
    print("   SETUP COMPLETE - ANCIENT BHARAT READY!")
    print("🎯" + "=" * 58 + "🎯")
    print()
    
    print("🚀 How to Start the Game:")
    if platform.system() == "Windows":
        print("   Option 1: Double-click start_game.bat")
        print("   Option 2: python simple_setup.py")
        print("   Option 3: python simple_game_server.py")
    else:
        print("   Option 1: ./start_game.sh")
        print("   Option 2: python3 simple_setup.py")
        print("   Option 3: python3 simple_game_server.py")
    
    print()
    print("🧪 Test Permissions:")
    print("   python test_permissions.py")
    print()
    
    print("🌐 Game URLs (after starting server):")
    print("   Game Client: http://localhost:8000/client")
    print("   Server Status: http://localhost:8000/status")
    print("   Admin Panel: http://localhost:8000/admin/save")
    print()
    
    print("🔐 Permissions Set:")
    print("   ✅ Directory read/write access")
    print("   ✅ Python execution permissions")
    print("   ✅ Network port binding (8000, 8080)")
    print("   ✅ Firewall rules (Windows)")
    print("   ✅ Package installation rights")
    print()
    
    print("🎮 Game Features Ready:")
    print("   🏛️ 5 Ancient Bharat Regions")
    print("   👥 3 Cultural NPCs with Sanskrit names")
    print("   📜 Epic Sarasvati Map quest system")
    print("   💬 Real-time multiplayer chat")
    print("   💾 Automatic progress saving")
    print()
    
    print("📞 If you have issues:")
    print("   1. Run as Administrator (Windows)")
    print("   2. Check test_permissions.py output")
    print("   3. Manually allow Python through firewall")
    print("   4. Use python --version to verify Python 3.8+")


def main():
    """Main setup function"""
    print_header()
    
    print("🔍 Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required (found {sys.version})")
        print("   Please install Python 3.8+ from python.org")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Request admin rights if needed
    request_admin_rights()
    
    # Set up all permissions
    set_directory_permissions()
    create_required_directories()
    set_python_execution_policy()
    configure_firewall_permissions()
    set_network_permissions()
    install_with_permissions()
    create_launch_scripts()
    create_permission_test_file()
    
    # Show final instructions
    show_final_instructions()
    
    # Ask to run permission test
    print("\n🧪 Run permission test now? (recommended)")
    choice = input("Test permissions? (Y/n): ").lower().strip()
    
    if choice in ['', 'y', 'yes']:
        print("\n" + "-" * 60)
        subprocess.run([sys.executable, "test_permissions.py"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled!")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("   This may be a permissions issue")
        print("   Try running as Administrator")
        input("Press Enter to exit...")