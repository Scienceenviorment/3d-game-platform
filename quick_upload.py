#!/usr/bin/env python3
"""
Quick GitHub Repository Creator
==============================
"""

import subprocess
import os

def create_github_repo():
    """Create GitHub repository using GitHub CLI"""
    print("🚀 Creating GitHub Repository...")
    
    try:
        # Check if GitHub CLI is installed
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI not found. Please install it first:")
            print("   Visit: https://cli.github.com/")
            return False
        
        print("✅ GitHub CLI found")
        
        # Create repository
        cmd = [
            'gh', 'repo', 'create', '3d-game-platform',
            '--public',
            '--description', 'AI-powered 3D game platform with procedural generation and Ancient Bharat theme',
            '--confirm'
        ]
        
        print("📦 Creating repository...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Repository created successfully!")
            return True
        else:
            print(f"❌ Failed to create repository: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ GitHub CLI not installed")
        return False

def push_to_github():
    """Push all files to GitHub"""
    print("\n📤 Pushing to GitHub...")
    
    try:
        # Push to GitHub
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully uploaded to GitHub!")
            print("🌐 Repository URL: https://github.com/Scien12/3d-game-platform")
            return True
        else:
            print(f"❌ Upload failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def main():
    """Main upload process"""
    print("🎮 3D Game Platform - GitHub Upload")
    print("=" * 40)
    
    # Option 1: Try automated creation
    if create_github_repo():
        if push_to_github():
            print("\n🎉 Upload Complete!")
            return
    
    # Option 2: Manual instructions
    print("\n📝 Manual Setup Required")
    print("-" * 25)
    print("Please create the repository manually:")
    print("1. Go to https://github.com/new")
    print("2. Repository name: 3d-game-platform")
    print("3. Make it Public")
    print("4. Don't initialize with README")
    print("5. Click 'Create repository'")
    print("\nThen run: git push -u origin main")

if __name__ == "__main__":
    main()