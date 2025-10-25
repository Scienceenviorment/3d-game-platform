#!/usr/bin/env python3
"""
Test the Procedural Generation Integration
Quick validation that the system works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from procedural_integration import procedural_manager


def test_procedural_system():
    """Test the procedural generation system"""
    print("=== TESTING PROCEDURAL GENERATION SYSTEM ===\n")
    
    # Initialize the system
    print("🔮 Initializing procedural generation...")
    success = procedural_manager.initialize()
    
    if not success:
        print("❌ Failed to initialize procedural generation system")
        return False
    
    print("✅ Procedural generation system initialized successfully!\n")
    
    # Test random content generation
    print("🎲 Testing random content generation...")
    
    # Generate job class
    job_class = procedural_manager.get_random_job_class()
    print(f"🏛️ Generated Job Class: {job_class['name']}")
    print(f"   Rarity: {job_class['rarity']}")
    print(f"   Description: {job_class['description'][:80]}...")
    
    # Generate weapon
    weapon = procedural_manager.get_random_weapon()
    print(f"\n⚔️ Generated Weapon: {weapon['name']}")
    print(f"   Damage: {weapon['damage_range'][0]}-{weapon['damage_range'][1]}")
    print(f"   Effects: {', '.join(weapon['special_effects'])}")
    
    # Generate beast
    beast = procedural_manager.get_random_beast()
    print(f"\n🐉 Generated Beast: {beast['name']}")
    print(f"   Taming Difficulty: {beast['taming_difficulty']}")
    print(f"   Abilities: {', '.join(beast['abilities'][:3])}")
    
    # Generate divine entity
    divine = procedural_manager.get_random_divine_entity()
    print(f"\n🌟 Generated Divine Entity: {divine['name']}")
    print(f"   Domain: {divine['domain']}")
    print(f"   Powers: {', '.join(divine['powers'][:2])}")
    
    # Test quest content bundle
    print(f"\n⚡ Testing quest content generation...")
    quest_content = procedural_manager.generate_quest_content()
    print(f"   Quest Reward: {quest_content['reward_weapon']['name']}")
    print(f"   Quest Beast: {quest_content['quest_beast']['name']}")
    print(f"   Patron Divine: {quest_content['patron_divine']['name']}")
    print(f"   Unlock Class: {quest_content['unlock_class']['name']}")
    
    # Test statistics
    print(f"\n📊 Generation statistics:")
    stats = procedural_manager.get_statistics()
    print(f"   Total Content: {stats['total_content']}")
    print(f"   Job Classes: {stats['total_job_classes']}")
    print(f"   Weapons: {stats['total_weapons']}")
    print(f"   Beasts: {stats['total_beasts']}")
    print(f"   Divine Entities: {stats['total_divine_entities']}")
    
    # Test potential combinations
    combinations = stats['potential_combinations']
    print(f"\n🔢 Potential combinations:")
    print(f"   Job Classes: {combinations['job_classes']:,}")
    print(f"   Weapons: {combinations['weapons']:,}")
    print(f"   Beasts: {combinations['beasts']:,}")
    print(f"   Divine Entities: {combinations['divine_entities']:,}")
    
    total_possible = (combinations['job_classes'] + combinations['weapons'] + 
                     combinations['beasts'] + combinations['divine_entities'])
    print(f"   Total Possible: {total_possible:,}")
    
    print(f"\n🌟 Procedural generation test completed successfully!")
    print(f"✨ The system can generate {total_possible:,} unique content pieces!")
    
    return True


if __name__ == "__main__":
    test_procedural_system()