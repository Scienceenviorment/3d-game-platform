#!/usr/bin/env python3
"""
AI Beast Taming System Demo
Demonstrates the enhanced NPC AI agents with beast taming storyline
"""

import asyncio
import json
import sys
import os

# Add server directory to path
server_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server')
sys.path.append(server_dir)

from enhanced_npcs import enhanced_npc_manager


def demo_ai_conversations():
    """Demonstrate AI-powered conversations with different NPCs"""
    print("🏛️ AI Beast Taming System - Interactive Demo")
    print("=" * 60)
    print("Experience realistic conversations with AI-powered NPCs!")
    print("Each NPC has memory, personality, and specialized knowledge.")
    print()
    
    # Demo player data
    player_id = "demo_player"
    player_data = {
        "level": 12,
        "experience": 300,
        "tamed_beasts": ["forest_sprite", "mountain_eagle"],
        "region": "Sacred Library"
    }
    
    print(f"Demo Player: Level {player_data['level']}, "
          f"Experience {player_data['experience']}, "
          f"Beasts: {', '.join(player_data['tamed_beasts'])}")
    print()
    
    # Conversation scenarios
    scenarios = [
        {
            "npc": "arunima",
            "title": "🏛️ Scholarly Wisdom from Arunima",
            "conversations": [
                "Namaste, Arunima. I seek knowledge about the divine Garuda.",
                "What ancient texts mention these celestial birds?",
                "How can I prove myself worthy to approach a Garuda?",
                "Thank you for sharing your wisdom with me."
            ]
        },
        {
            "npc": "devraj",
            "title": "🌲 Wilderness Expertise from Devraj",
            "conversations": [
                "Greetings, Devraj. I need advice on tracking forest beasts.",
                "I've heard about Vanaras in these forests. How do I find them?",
                "What supplies should I bring for a taming expedition?",
                "Your experience in the wild is invaluable, friend."
            ]
        },
        {
            "npc": "rukmini",
            "title": "🏘️ Village Wisdom from Rukmini",
            "conversations": [
                "Namaste, Elder Rukmini. I seek the wisdom of our ancestors.",
                "Tell me about the Nagas that guard our sacred waters.",
                "What traditions did past generations follow for beast bonding?",
                "Your guidance honors our village traditions."
            ]
        }
    ]
    
    for scenario in scenarios:
        print(scenario["title"])
        print("-" * len(scenario["title"]))
        
        for i, message in enumerate(scenario["conversations"], 1):
            print(f"\n{i}. Player: \"{message}\"")
            
            # Get AI response
            response = enhanced_npc_manager.interact_with_npc(
                scenario["npc"], player_id, message, player_data
            )
            
            npc_name = enhanced_npc_manager.npcs[scenario["npc"]].name
            print(f"   {npc_name}: {response}")
            
            # Update player data slightly for progression
            player_data["experience"] += 5
        
        print("\n" + "=" * 60 + "\n")


def demo_beast_information():
    """Demonstrate comprehensive beast information system"""
    print("🐲 Beast Information System Demo")
    print("=" * 40)
    print("Get specialized knowledge about mythical beasts from multiple NPCs:")
    print()
    
    beasts_to_demo = ["garuda", "naga", "vanara"]
    
    for beast in beasts_to_demo:
        print(f"🔍 Information about: {beast.upper()}")
        print("-" * 30)
        
        info = enhanced_npc_manager.get_beast_information(beast)
        
        print(f"📜 Scholarly Lore (Arunima):")
        print(f"   {info['lore'][:100]}...")
        print()
        
        print(f"🎯 Tracking Advice (Devraj):")
        print(f"   {info['tracking'][:100]}...")
        print()
        
        print(f"🏛️ Village Wisdom (Rukmini):")
        print(f"   {info['wisdom'][:100]}...")
        print()
        print("=" * 40 + "\n")


def demo_memory_system():
    """Demonstrate AI memory and relationship building"""
    print("🧠 AI Memory & Relationship System Demo")
    print("=" * 45)
    print("Watch how NPCs remember interactions and build relationships:")
    print()
    
    # Multiple interactions with the same NPC
    player_id = "memory_test_player"
    player_data = {"level": 5, "experience": 50, "tamed_beasts": []}
    
    conversations = [
        "Hello, I'm new to beast taming. Can you help me?",
        "I tried to approach a forest creature, but it ran away. What did I do wrong?",
        "Thank you for the advice! I successfully befriended a small forest sprite!",
        "I'm back! Do you have any advanced techniques to share?",
        "I remember you mentioned patience. That wisdom served me well."
    ]
    
    print("Conversation progression with Arunima:")
    print("-" * 40)
    
    for i, message in enumerate(conversations, 1):
        print(f"\nInteraction {i}:")
        print(f"Player: \"{message}\"")
        
        response = enhanced_npc_manager.interact_with_npc(
            "arunima", player_id, message, player_data
        )
        
        print(f"Arunima: {response}")
        
        # Simulate progression
        if i == 3:
            player_data["tamed_beasts"].append("forest_sprite")
            player_data["experience"] += 25
            player_data["level"] += 1
    
    print("\n" + "=" * 45 + "\n")


def demo_npc_status():
    """Demonstrate NPC status system"""
    print("📊 Enhanced NPC Status System")
    print("=" * 35)
    
    status = enhanced_npc_manager.get_all_npcs_status()
    
    for npc_id, npc_info in status.items():
        print(f"🏛️ {npc_info['name']} ({npc_id})")
        print(f"   📍 Region: {npc_info['region']}")
        print(f"   🎭 Personality: {npc_info['personality']}")
        print(f"   📚 Specialization: {npc_info['specialization']}")
        print(f"   🤖 AI Enhanced: {'✅' if npc_info['has_ai'] else '❌'}")
        print(f"   💬 Active Conversations: {npc_info['active_conversations']}")
        print()
    
    print("=" * 35 + "\n")


def main():
    """Run the complete AI Beast Taming System demo"""
    print("🎮 Welcome to the AI Beast Taming System Demo!")
    print("This demonstration showcases the enhanced NPCs with AI agents")
    print("based on the 'Classic of Mountains and Seas' adapted to Indian mythology.")
    print("\n" + "🕉️" * 20 + "\n")
    
    try:
        # Run all demonstrations
        demo_npc_status()
        demo_ai_conversations()
        demo_beast_information()
        demo_memory_system()
        
        print("🎊 Demo Complete!")
        print("Your Ancient Bharat game now features:")
        print("✅ AI-powered NPCs with memory and personality")
        print("✅ Beast taming storyline from Indian mythology")
        print("✅ Dynamic conversations that adapt to player progress")
        print("✅ Cultural authenticity with Sanskrit names and references")
        print("✅ Progressive difficulty and personalized guidance")
        print("\n🏛️ Start your enhanced server to experience the full system!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Make sure the enhanced NPC system is properly installed.")


if __name__ == "__main__":
    main()