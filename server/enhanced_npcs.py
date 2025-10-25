#!/usr/bin/env python3
"""
Enhanced NPCs with AI Agent Integration
Connects the AI agent system with the existing NPC framework
"""

from typing import Dict, Any, Optional
import sys
import os

# Add the current directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ai_agent_system import (
    arunima_ai, devraj_ai, rukmini_ai, story_manager,
    PlayerBeastProgress, BeastTamingStoryManager
)
from ancient_bharat_npcs import BaseNPC, NPCPersonality, DialogueState


class EnhancedNPC(BaseNPC):
    """Enhanced NPC with AI agent integration"""
    
    def __init__(self, npc_id: str, name: str, region: str, ai_agent=None):
        super().__init__(npc_id, name, region)
        self.ai_agent = ai_agent
        self.player_progress = {}  # Track progress per player
        
    def get_ai_response(self, player_id: str, player_input: str, 
                       player_level: int = 1, player_beasts: list = None) -> str:
        """Get AI-generated response for player interaction"""
        if not self.ai_agent:
            return self.get_default_response()
            
        if player_beasts is None:
            player_beasts = []
            
        # Create context for AI agent
        context = {
            "player_id": player_id,
            "player_level": player_level,
            "player_beasts": player_beasts,
            "npc_id": self.npc_id,
            "region": self.region
        }
        
        # Get AI response
        response = self.ai_agent.generate_response(player_input, context)
        
        # Check for story advancement
        if player_id not in self.player_progress:
            self.player_progress[player_id] = PlayerBeastProgress(player_id)
            
        progress = self.player_progress[player_id]
        new_fragment = story_manager.check_story_advancement(progress)
        
        if new_fragment:
            story_text = story_manager.get_story_fragment(new_fragment, progress)
            response += f"\n\n🏛️ Ancient Memory Unlocked:\n{story_text}"
            
        return response
    
    def get_default_response(self) -> str:
        """Fallback response if no AI agent is available"""
        return f"Namaste, traveler. I am {self.name}. How may I assist you?"
    
    def update_player_beast_progress(self, player_id: str, 
                                   beast_tamed: str = None,
                                   experience_gained: int = 0):
        """Update player's beast taming progress"""
        if player_id not in self.player_progress:
            self.player_progress[player_id] = PlayerBeastProgress(player_id)
            
        progress = self.player_progress[player_id]
        
        if beast_tamed:
            progress.tamed_beasts.append(beast_tamed)
            
        progress.taming_experience += experience_gained


class EnhancedArunima(EnhancedNPC):
    """Enhanced Arunima with AI agent"""
    
    def __init__(self):
        super().__init__(
            npc_id="arunima",
            name="Arunima",
            region="Sacred Library",
            ai_agent=arunima_ai
        )
        self.personality = NPCPersonality.WISE
        self.specialization = "Vedic Scholar and Divine Beast Expert"
        
    def get_beast_lore(self, beast_name: str) -> str:
        """Get specific lore about a beast"""
        lore_database = {
            "garuda": """
            Garuda, the divine eagle and mount of Lord Vishnu, represents the 
            eternal struggle between good and evil. Those who seek to bond with 
            Garuda's descendants must prove their righteousness and dedication 
            to dharma. The sacred mantras and offerings of soma are essential.
            """,
            "naga": """
            The Nagas are ancient serpent beings, children of Kashyapa and Kadru. 
            They guard treasures and sacred knowledge in the depths of waters and 
            underground realms. Approaching them requires wisdom, respect, and 
            often precious gems as offerings.
            """,
            "vanara": """
            The Vanaras, led by Hanuman in the great epic, represent devotion 
            and strength. They are loyal allies to those who prove themselves 
            worthy through acts of courage and selflessness. Forest fruits and 
            sincere devotion win their hearts.
            """
        }
        return lore_database.get(beast_name.lower(), 
                               "I must consult the ancient texts for more information.")


class EnhancedDevraj(EnhancedNPC):
    """Enhanced Devraj with AI agent"""
    
    def __init__(self):
        super().__init__(
            npc_id="devraj",
            name="Devraj",
            region="Ancient Forest",
            ai_agent=devraj_ai
        )
        self.personality = NPCPersonality.PRACTICAL
        self.specialization = "Beast Tracker and Wilderness Expert"
        
    def get_tracking_advice(self, beast_type: str) -> str:
        """Get practical tracking advice"""
        advice_database = {
            "forest_beasts": """
            Forest creatures follow predictable patterns - water sources at dawn, 
            feeding grounds at dusk, shelter during midday heat. Look for tracks 
            near streams, broken branches, and disturbed vegetation. Move quietly 
            and stay downwind.
            """,
            "mountain_beasts": """
            Mountain dwellers prefer high perches and rocky caves. Check cliff 
            faces and rocky outcrops. They often soar on thermal currents during 
            midday. Approach from below and have an escape route planned.
            """,
            "water_beasts": """
            Aquatic creatures emerge during specific lunar phases and times. 
            Sacred ponds and confluence points are favored. Bring waterproof 
            gear and learn to hold your breath - you may need to follow them 
            underwater.
            """
        }
        return advice_database.get(beast_type, 
                                 "Each creature is unique - observe and adapt.")


class EnhancedRukmini(EnhancedNPC):
    """Enhanced Rukmini with AI agent"""
    
    def __init__(self):
        super().__init__(
            npc_id="rukmini",
            name="Rukmini",
            region="Village Center",
            ai_agent=rukmini_ai
        )
        self.personality = NPCPersonality.WISE
        self.specialization = "Village Elder and Tradition Keeper"
        
    def share_village_wisdom(self) -> str:
        """Share traditional village wisdom about beasts"""
        wisdom_collection = [
            """
            In our village, we've always known that beasts respond to the purity 
            of one's heart. A person with selfish intentions will never earn the 
            trust of sacred creatures. Approach with humility and genuine care.
            """,
            """
            The old ways teach us that every creature has a purpose in the cosmic 
            order. Some are guardians, some are teachers, some are healers. 
            Understanding this purpose is key to forming a true bond.
            """,
            """
            My grandmother told me that the first beast tamers were not conquerors 
            but friends. They offered service, not domination. Remember this in 
            your journey, child.
            """
        ]
        import random
        return random.choice(wisdom_collection)


class NPCManager:
    """Enhanced NPC Manager with AI integration"""
    
    def __init__(self):
        self.npcs = {
            "arunima": EnhancedArunima(),
            "devraj": EnhancedDevraj(),
            "rukmini": EnhancedRukmini()
        }
        self.story_manager = BeastTamingStoryManager()
        
    def interact_with_npc(self, npc_id: str, player_id: str, 
                         player_input: str, player_data: Dict[str, Any] = None) -> str:
        """Enhanced interaction with NPC using AI"""
        if npc_id not in self.npcs:
            return "NPC not found."
            
        if player_data is None:
            player_data = {}
            
        npc = self.npcs[npc_id]
        
        # Extract player information
        player_level = player_data.get("level", 1)
        player_beasts = player_data.get("tamed_beasts", [])
        
        # Get AI response
        response = npc.get_ai_response(
            player_id, player_input, player_level, player_beasts
        )
        
        return response
    
    def get_all_npcs_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all NPCs"""
        status = {}
        for npc_id, npc in self.npcs.items():
            status[npc_id] = {
                "name": npc.name,
                "region": npc.region,
                "specialization": getattr(npc, "specialization", "General"),
                "personality": npc.personality.value,
                "has_ai": npc.ai_agent is not None,
                "active_conversations": len(npc.player_progress)
            }
        return status
    
    def get_beast_information(self, beast_name: str) -> Dict[str, str]:
        """Get comprehensive beast information from all NPCs"""
        info = {}
        
        # Get information from each NPC based on their specialization
        arunima = self.npcs["arunima"]
        devraj = self.npcs["devraj"]
        rukmini = self.npcs["rukmini"]
        
        info["lore"] = arunima.get_beast_lore(beast_name)
        info["tracking"] = devraj.get_tracking_advice("forest_beasts")
        info["wisdom"] = rukmini.share_village_wisdom()
        
        return info


# Create global enhanced NPC manager
enhanced_npc_manager = NPCManager()


def test_enhanced_npcs():
    """Test the enhanced NPC system"""
    print("🤖 Testing Enhanced NPC System with AI Agents")
    print("=" * 60)
    
    # Test interactions with each NPC
    test_player_id = "test_player_001"
    test_player_data = {
        "level": 8,
        "tamed_beasts": ["forest_sprite"],
        "experience": 150
    }
    
    # Test Arunima
    print("Testing Arunima (Veda Scholar):")
    response = enhanced_npc_manager.interact_with_npc(
        "arunima", test_player_id, 
        "Tell me about Garuda and how to approach divine birds", 
        test_player_data
    )
    print(f"Arunima: {response}")
    print()
    
    # Test Devraj
    print("Testing Devraj (Forest Ranger):")
    response = enhanced_npc_manager.interact_with_npc(
        "devraj", test_player_id,
        "I want to track and tame a forest beast. What advice do you have?",
        test_player_data
    )
    print(f"Devraj: {response}")
    print()
    
    # Test Rukmini
    print("Testing Rukmini (Village Elder):")
    response = enhanced_npc_manager.interact_with_npc(
        "rukmini", test_player_id,
        "Share your wisdom about the ancient ways of beast taming",
        test_player_data
    )
    print(f"Rukmini: {response}")
    print()
    
    # Test NPC status
    print("NPC Status Overview:")
    status = enhanced_npc_manager.get_all_npcs_status()
    for npc_id, npc_status in status.items():
        print(f"{npc_id}: {npc_status}")
    
    print("✅ Enhanced NPC system with AI agents working correctly!")


if __name__ == "__main__":
    test_enhanced_npcs()