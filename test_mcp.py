#!/usr/bin/env python3
"""
Simple MCP Server Test
======================
"""

import asyncio
import json
import os
from pathlib import Path

print("🚀 Starting MCP Server Test...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"📂 Contents: {os.listdir('.')}")

# Check if we can import MCP
try:
    from mcp.server import Server
    print("✅ MCP server module imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import MCP: {e}")
    exit(1)

# Check game files
game_files = [
    'server/ai_3d_model_agent.py',
    'server/procedural_generator.py', 
    'server/karma_system.py',
    'server/class_system.py'
]

print("\n🎮 Checking game files:")
for file in game_files:
    if Path(file).exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - NOT FOUND")

print("\n🎯 MCP Server components ready!")
print("📊 To start full server, run: python mcp_server.py")