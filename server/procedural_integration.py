"""
Procedural Generation Integration
Adds dynamic content generation to the game server
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from procedural_generator import ProceduralGenerator
import json
from typing import Dict, Any, List


class ProceduralContentManager:
    """Manages procedurally generated content for the game"""
    
    def __init__(self):
        self.generator = ProceduralGenerator()
        self.content_cache = {}
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the procedural content system"""
        try:
            print("🔮 Initializing Procedural Content Generator...")
            
            # Generate initial content
            initial_counts = self.generator.generate_bulk_content(
                job_classes=200,  # Generate 200 job classes
                weapons=300,      # Generate 300 weapons  
                beasts=250,       # Generate 250 beasts
                divine_entities=100  # Generate 100 divine entities
            )
            
            print(f"✅ Generated {initial_counts['job_classes']} job classes")
            print(f"✅ Generated {initial_counts['weapons']} weapons")
            print(f"✅ Generated {initial_counts['beasts']} beasts")
            print(f"✅ Generated {initial_counts['divine_entities']} divine entities")
            
            # Cache the content for quick access
            self._update_content_cache()
            
            self.is_initialized = True
            print("🌟 Procedural Generation System Ready!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize procedural generation: {e}")
            return False
    
    def _update_content_cache(self):
        """Update the content cache with current generated content"""
        self.content_cache = {
            'job_classes': list(self.generator.generated_job_classes.values()),
            'weapons': list(self.generator.generated_weapons.values()),
            'beasts': list(self.generator.generated_beasts.values()),
            'divine_entities': list(self.generator.generated_divine_entities.values())
        }
    
    def get_random_job_class(self) -> Dict[str, Any]:
        """Get a random generated job class"""
        if not self.content_cache.get('job_classes'):
            return None
        
        job_class = self.generator.generate_job_class()
        return {
            'id': job_class.class_id,
            'name': job_class.name,
            'role': job_class.role,
            'element': job_class.element,
            'theme': job_class.theme,
            'description': job_class.description,
            'rarity': job_class.rarity.value,
            'abilities': job_class.abilities,
            'stat_bonuses': job_class.stat_bonuses,
            'requirements': job_class.requirements
        }
    
    def get_random_weapon(self) -> Dict[str, Any]:
        """Get a random generated weapon"""
        weapon = self.generator.generate_weapon()
        return {
            'id': weapon.weapon_id,
            'name': weapon.name,
            'type': weapon.weapon_type,
            'material': weapon.material,
            'enchantment': weapon.enchantment,
            'description': weapon.description,
            'rarity': weapon.rarity.value,
            'damage_range': weapon.damage_range,
            'special_effects': weapon.special_effects,
            'requirements': weapon.requirements
        }
    
    def get_random_beast(self) -> Dict[str, Any]:
        """Get a random generated beast"""
        beast = self.generator.generate_beast()
        return {
            'id': beast.beast_id,
            'name': beast.name,
            'base_creature': beast.base_creature,
            'modifier': beast.modifier,
            'origin': beast.origin,
            'description': beast.description,
            'rarity': beast.rarity.value,
            'abilities': beast.abilities,
            'stats': beast.stats,
            'taming_difficulty': beast.taming_difficulty
        }
    
    def get_random_divine_entity(self) -> Dict[str, Any]:
        """Get a random generated divine entity"""
        entity = self.generator.generate_divine_entity()
        return {
            'id': entity.entity_id,
            'name': entity.name,
            'domain': entity.domain,
            'form': entity.form,
            'alignment': entity.alignment,
            'description': entity.description,
            'rarity': entity.rarity.value,
            'powers': entity.powers,
            'favor_requirements': entity.favor_requirements
        }
    
    def get_content_by_rarity(self, content_type: str, rarity: str) -> List[Dict[str, Any]]:
        """Get content of specific type and rarity"""
        try:
            from procedural_generator import ContentRarity
            rarity_enum = ContentRarity(rarity)
            content = self.generator.get_content_by_rarity(content_type, rarity_enum)
            
            # Convert to dict format
            result = []
            for item in content:
                if hasattr(item, '__dict__'):
                    item_dict = item.__dict__.copy()
                    if 'rarity' in item_dict:
                        item_dict['rarity'] = item_dict['rarity'].value
                    result.append(item_dict)
            
            return result
        except Exception as e:
            print(f"Error getting content by rarity: {e}")
            return []
    
    def generate_quest_content(self) -> Dict[str, Any]:
        """Generate content specifically for quests"""
        return {
            'reward_weapon': self.get_random_weapon(),
            'quest_beast': self.get_random_beast(),
            'patron_divine': self.get_random_divine_entity(),
            'unlock_class': self.get_random_job_class()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics"""
        stats = self.generator.get_statistics()
        
        # Add breakdown by rarity
        rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythical', 'divine']
        rarity_breakdown = {}
        
        for content_type in ['job_classes', 'weapons', 'beasts', 'divine_entities']:
            rarity_breakdown[content_type] = {}
            for rarity in rarities:
                count = len(self.get_content_by_rarity(content_type, rarity))
                rarity_breakdown[content_type][rarity] = count
        
        stats['rarity_breakdown'] = rarity_breakdown
        return stats
    
    def expand_content(self, multiplier: int = 2) -> Dict[str, int]:
        """Expand existing content by generating more"""
        current_stats = self.generator.get_statistics()
        
        new_counts = self.generator.generate_bulk_content(
            job_classes=current_stats['total_job_classes'] * multiplier,
            weapons=current_stats['total_weapons'] * multiplier,
            beasts=current_stats['total_beasts'] * multiplier,
            divine_entities=current_stats['total_divine_entities'] * multiplier
        )
        
        self._update_content_cache()
        return new_counts
    
    def get_content_for_player_level(self, player_level: int) -> Dict[str, List[Dict[str, Any]]]:
        """Get content appropriate for player level"""
        appropriate_content = {
            'job_classes': [],
            'weapons': [],
            'beasts': [],
            'divine_entities': []
        }
        
        # Filter content by level requirements
        for job_class in self.content_cache.get('job_classes', []):
            if hasattr(job_class, 'requirements') and job_class.requirements.get('min_level', 1) <= player_level:
                appropriate_content['job_classes'].append(job_class.__dict__ if hasattr(job_class, '__dict__') else job_class)
        
        # For weapons and beasts, use rarity as level gate
        level_rarity_map = {
            1: ['common'],
            10: ['common', 'uncommon'],
            25: ['common', 'uncommon', 'rare'],
            50: ['common', 'uncommon', 'rare', 'epic'],
            75: ['common', 'uncommon', 'rare', 'epic', 'legendary'],
            100: ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythical', 'divine']
        }
        
        allowed_rarities = ['common']
        for level_threshold in sorted(level_rarity_map.keys()):
            if player_level >= level_threshold:
                allowed_rarities = level_rarity_map[level_threshold]
        
        for weapon in self.content_cache.get('weapons', []):
            if hasattr(weapon, 'rarity') and weapon.rarity.value in allowed_rarities:
                appropriate_content['weapons'].append(weapon.__dict__ if hasattr(weapon, '__dict__') else weapon)
        
        return appropriate_content


# Global instance
procedural_manager = ProceduralContentManager()


def test_procedural_integration():
    """Test the procedural integration system"""
    print("=== TESTING PROCEDURAL INTEGRATION ===\n")
    
    # Initialize
    success = procedural_manager.initialize()
    print(f"Initialization: {'✅ Success' if success else '❌ Failed'}")
    
    if success:
        # Test random generation
        print("\n🎲 Testing Random Generation:")
        job_class = procedural_manager.get_random_job_class()
        print(f"Random Job Class: {job_class['name']}")
        
        weapon = procedural_manager.get_random_weapon()
        print(f"Random Weapon: {weapon['name']}")
        
        beast = procedural_manager.get_random_beast()
        print(f"Random Beast: {beast['name']}")
        
        divine = procedural_manager.get_random_divine_entity()
        print(f"Random Divine: {divine['name']}")
        
        # Test quest content
        print("\n⚔️ Testing Quest Content Generation:")
        quest_content = procedural_manager.generate_quest_content()
        print(f"Quest Reward: {quest_content['reward_weapon']['name']}")
        print(f"Quest Beast: {quest_content['quest_beast']['name']}")
        
        # Test statistics
        print("\n📊 Generation Statistics:")
        stats = procedural_manager.get_statistics()
        print(f"Total Content Generated: {stats['total_content']}")
        print(f"Job Classes: {stats['total_job_classes']}")
        print(f"Weapons: {stats['total_weapons']}")
        print(f"Beasts: {stats['total_beasts']}")
        print(f"Divine Entities: {stats['total_divine_entities']}")
        
        print("\n🌟 Procedural Integration Test Complete!")


if __name__ == "__main__":
    test_procedural_integration()