#!/usr/bin/env python3
"""
Ancient Bharat NPCs - Key Characters
Python classes for game NPCs with dialogue and behavior systems
"""

import random
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


# NPC personality types using Python Enum
class NPCPersonality(Enum):
    """Different personality types for NPCs"""
    WISE = "wise"           # Speaks in riddles, offers wisdom
    FRIENDLY = "friendly"   # Helpful and welcoming
    MYSTERIOUS = "mysterious"  # Cryptic and secretive
    PRACTICAL = "practical"    # Direct and task-focused


# NPC dialogue states
class DialogueState(Enum):
    """Current dialogue state of NPC"""
    GREETING = "greeting"
    CONVERSATION = "conversation" 
    QUEST_OFFER = "quest_offer"
    FAREWELL = "farewell"


@dataclass
class DialogueLine:
    """A single line of NPC dialogue"""
    text: str
    personality: NPCPersonality
    state: DialogueState
    next_options: List[str] = None  # Possible player responses


# Base NPC class using Python inheritance
class BaseNPC:
    """Base class for all NPCs in Ancient Bharat"""
    
    def __init__(self, npc_id: str, name: str, region: str):
        """Initialize basic NPC properties"""
        self.npc_id = npc_id
        self.name = name
        self.region = region
        self.personality = NPCPersonality.FRIENDLY
        self.current_state = DialogueState.GREETING
        self.last_interaction = 0.0
        self.dialogue_lines = {}  # Will be populated by subclasses
        self.daily_schedule = {}  # When NPC appears/disappears
        self.reputation = 0       # Player's standing with this NPC
        
    def get_greeting(self) -> str:
        """Get appropriate greeting based on time and reputation"""
        current_time = time.time()
        hour = int((current_time % 86400) / 3600)  # Get hour of day
        
        # Time-based greetings
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Greetings"
        
        # Reputation-based greeting modifier
        if self.reputation > 50:
            respect = ", dear friend"
        elif self.reputation > 20:
            respect = ", traveler"
        elif self.reputation < -20:
            respect = ", stranger"
        else:
            respect = ""
        
        return f"{time_greeting}{respect}! I am {self.name}."
    
    def interact(self, player_message: str = None) -> dict:
        """Handle interaction with player"""
        self.last_interaction = time.time()
        
        # Get appropriate response
        response = self._generate_response(player_message)
        
        # Update dialogue state
        self._update_state()
        
        return {
            "npc_id": self.npc_id,
            "npc_name": self.name,
            "response": response,
            "personality": self.personality.value,
            "state": self.current_state.value
        }
    
    def _generate_response(self, player_message: str) -> str:
        """Generate appropriate response (to be overridden by subclasses)"""
        return self.get_greeting()
    
    def _update_state(self):
        """Update internal dialogue state"""
        # Simple state progression
        if self.current_state == DialogueState.GREETING:
            self.current_state = DialogueState.CONVERSATION
        elif self.current_state == DialogueState.CONVERSATION:
            # Randomly offer quests or farewell
            if random.random() < 0.3:
                self.current_state = DialogueState.QUEST_OFFER
            elif random.random() < 0.2:
                self.current_state = DialogueState.FAREWELL
    
    def is_available(self) -> bool:
        """Check if NPC is available based on schedule"""
        current_hour = int((time.time() % 86400) / 3600)
        if self.daily_schedule:
            return self.daily_schedule.get(current_hour, True)
        return True


# Veda Scholar Arunima - Wise teacher in Indrapura City
class VedaScholarArunima(BaseNPC):
    """Cryptic knowledge keeper who speaks in riddles"""
    
    def __init__(self):
        super().__init__(
            npc_id="arunima_veda_scholar",
            name="Veda Scholar Arunima",
            region="indrapura_city"
        )
        self.personality = NPCPersonality.WISE
        
        # Arunima's dialogue library
        self.riddles = [
            "The river that flows backwards holds the key to tomorrow's wisdom.",
            "What is found only when lost, and lost only when found?",
            "The tree that grows in winter bears fruit in the mind's summer.",
            "Seven steps north, three steps within - there wisdom dwells.",
            "The silent bell rings loudest for those who truly listen."
        ]
        
        self.wisdom_quotes = [
            "Knowledge is like water - it takes the shape of its container.",
            "The wise traveler carries questions, not just answers.",
            "In Ancient Bharat, every stone has a story to tell.",
            "The Sarasvati's wisdom flows through all who seek it.",
            "Time moves in circles here, not lines."
        ]
        
        # Daily schedule (appears mostly in morning and evening)
        self.daily_schedule = {
            6: True, 7: True, 8: True, 9: True, 10: True,    # Morning
            11: False, 12: False, 13: False, 14: False,       # Midday break
            15: True, 16: True, 17: True, 18: True,           # Afternoon
            19: True, 20: True, 21: True,                     # Evening
        }
    
    def _generate_response(self, player_message: str) -> str:
        """Generate wise, cryptic responses"""
        if self.current_state == DialogueState.GREETING:
            return (f"{self.get_greeting()} I spend my days unraveling the mysteries "
                   f"woven into the ancient texts. Perhaps you seek knowledge too?")
        
        elif self.current_state == DialogueState.CONVERSATION:
            if player_message and ("sarasvati" in player_message.lower() or 
                                  "map" in player_message.lower()):
                return ("Ah, the Sarasvati Map... " + random.choice([
                    "Its fragments are scattered like thoughts in a sleeping mind.",
                    "The river's knowledge flows to those pure of purpose.",
                    "Seven fragments, seven regions, seven truths to uncover.",
                    "The map shows not places, but the paths between worlds."
                ]))
            else:
                return random.choice(self.riddles)
        
        elif self.current_state == DialogueState.QUEST_OFFER:
            return ("The ancient library holds scrolls that few can read. " +
                   "Bring me three Sanskrit inscriptions from the ruins, " +
                   "and I shall share the location of a map fragment.")
        
        else:  # FAREWELL
            return ("May the wisdom of the ages guide your steps, traveler. " +
                   random.choice(self.wisdom_quotes))


# Ranger Devraj - Practical guide for wilderness survival
class RangerDevraj(BaseNPC):
    """Experienced wilderness guide and protector"""
    
    def __init__(self):
        super().__init__(
            npc_id="ranger_devraj",
            name="Ranger Devraj", 
            region="narmada_forest"
        )
        self.personality = NPCPersonality.PRACTICAL
        
        # Devraj's survival tips and local knowledge
        self.survival_tips = [
            "The banyan trees here are over 500 years old - they've seen many travelers.",
            "Never drink from still water in the forest. Find the running streams.",
            "The morning mist reveals paths that are hidden in bright sunlight.",
            "Wild elephants use this route at sunset - best to avoid the eastern path then.",
            "The sacred grove is guarded by more than just tradition, friend."
        ]
        
        self.warnings = [
            "Strange lights have been seen near the ancient trees lately.",
            "The village reports livestock going missing - something stalks the forest.",
            "Monsoon season approaches - the river will flood the lower paths soon.",
            "Bandits have been spotted on the trade routes to the north.",
            "The old hermit hasn't been seen for three days - most unusual."
        ]
        
        # Available throughout most of the day (forest patrol schedule)
        self.daily_schedule = {
            0: False, 1: False, 2: False, 3: False, 4: False,  # Sleeping
            5: True, 6: True, 7: True, 8: True, 9: True,       # Morning patrol
            10: True, 11: True, 12: True, 13: False,           # Midday rest
            14: True, 15: True, 16: True, 17: True,            # Afternoon patrol
            18: True, 19: True, 20: True, 21: False,           # Evening return
            22: False, 23: False                               # Night rest
        }
    
    def _generate_response(self, player_message: str) -> str:
        """Generate practical, helpful responses"""
        if self.current_state == DialogueState.GREETING:
            return (f"{self.get_greeting()} I patrol these woods to keep travelers safe. "
                   f"The forest can be dangerous for those who don't know her ways.")
        
        elif self.current_state == DialogueState.CONVERSATION:
            if player_message and any(word in player_message.lower() 
                                    for word in ["danger", "safe", "path", "route"]):
                return ("Listen well: " + random.choice(self.warnings))
            else:
                return random.choice(self.survival_tips)
        
        elif self.current_state == DialogueState.QUEST_OFFER:
            return ("I need someone brave to investigate the missing livestock. " +
                   "Check the caves near the sacred grove and report what you find. " +
                   "I'll mark the safe paths on your map in return.")
        
        else:  # FAREWELL
            return ("Stay safe out there, traveler. The forest has many secrets, " +
                   "but also many dangers. Trust your instincts.")


# Village Elder Rukmini - Community leader and quest giver
class VillageElderRukmini(BaseNPC):
    """Wise village elder who assigns community tasks"""
    
    def __init__(self):
        super().__init__(
            npc_id="elder_rukmini",
            name="Village Elder Rukmini",
            region="ocean_frontier"
        )
        self.personality = NPCPersonality.FRIENDLY
        
        # Village needs and community tasks
        self.village_tasks = [
            "Our fishing nets were damaged in the storm - we need new rope from the market.",
            "The lighthouse keeper is ill - someone must tend the beacon tonight.",
            "Children have been having nightmares about voices from the sea.",
            "The merchant caravan is three days overdue - they may need rescue.",
            "Our shrine needs fresh flowers - the marigolds bloom in the hills."
        ]
        
        self.community_stories = [
            "This village was founded by refugees from a great flood centuries ago.",
            "My grandmother spoke of times when the sea glowed with inner light.",
            "The old songs tell of a map that could heal the broken rivers.",
            "Travelers from all five regions once gathered here for the festival.",
            "The lighthouse was built on the foundation of an ancient temple."
        ]
        
        # Available during community hours
        self.daily_schedule = {
            5: False, 6: True, 7: True, 8: True, 9: True,      # Early morning
            10: True, 11: True, 12: True, 13: True, 14: True,  # Midday
            15: True, 16: True, 17: True, 18: True, 19: True,  # Evening
            20: False, 21: False, 22: False, 23: False,        # Night rest
            0: False, 1: False, 2: False, 3: False, 4: False
        }
    
    def _generate_response(self, player_message: str) -> str:
        """Generate community-focused, caring responses"""
        if self.current_state == DialogueState.GREETING:
            return (f"{self.get_greeting()} Welcome to our humble village! "
                   f"We don't see many travelers these days. How can we help you?")
        
        elif self.current_state == DialogueState.CONVERSATION:
            if player_message and any(word in player_message.lower() 
                                    for word in ["village", "help", "community", "people"]):
                return ("Our village faces many challenges: " + 
                       random.choice(self.village_tasks))
            else:
                return random.choice(self.community_stories)
        
        elif self.current_state == DialogueState.QUEST_OFFER:
            return ("If you're willing to help our community, I have tasks that " +
                   "need doing. " + random.choice(self.village_tasks) + 
                   " In return, I can share stories of the old maps.")
        
        else:  # FAREWELL
            return ("Thank you for visiting our village, traveler. " +
                   "May the winds carry you safely to your destination. " +
                   "You're always welcome here.")


# NPC Manager class for handling all NPCs
class NPCManager:
    """Manages all NPCs in Ancient Bharat"""
    
    def __init__(self):
        """Initialize all key NPCs"""
        self.npcs = {}  # Dict[str, BaseNPC]
        self._create_npcs()
    
    def _create_npcs(self):
        """Create and register all NPCs"""
        # Create the three key NPCs
        arunima = VedaScholarArunima()
        devraj = RangerDevraj() 
        rukmini = VillageElderRukmini()
        
        # Register them in the manager
        self.npcs[arunima.npc_id] = arunima
        self.npcs[devraj.npc_id] = devraj
        self.npcs[rukmini.npc_id] = rukmini
    
    def get_npcs_in_region(self, region: str) -> List[dict]:
        """Get all available NPCs in a specific region"""
        region_npcs = []
        
        for npc in self.npcs.values():
            if npc.region == region and npc.is_available():
                region_npcs.append({
                    "id": npc.npc_id,
                    "name": npc.name,
                    "personality": npc.personality.value,
                    "available": True
                })
        
        return region_npcs
    
    def interact_with_npc(self, npc_id: str, player_message: str = None) -> dict:
        """Handle interaction between player and NPC"""
        if npc_id not in self.npcs:
            return {
                "error": f"NPC {npc_id} not found",
                "available_npcs": list(self.npcs.keys())
            }
        
        npc = self.npcs[npc_id]
        
        if not npc.is_available():
            return {
                "error": f"{npc.name} is not available right now",
                "npc_id": npc_id,
                "npc_name": npc.name,
                "available": False
            }
        
        # Process the interaction
        response = npc.interact(player_message)
        response["available"] = True
        return response
    
    def get_all_npcs_status(self) -> dict:
        """Get status of all NPCs for debugging/admin"""
        status = {}
        
        for npc_id, npc in self.npcs.items():
            status[npc_id] = {
                "name": npc.name,
                "region": npc.region,
                "personality": npc.personality.value,
                "available": npc.is_available(),
                "last_interaction": npc.last_interaction,
                "current_state": npc.current_state.value,
                "reputation": npc.reputation
            }
        
        return status


# Create global NPC manager instance
npc_manager = NPCManager()


# Example usage and testing
if __name__ == "__main__":
    print("🎭 Ancient Bharat NPCs - Testing System")
    print("=" * 50)
    
    # Test each NPC
    npcs_to_test = [
        "arunima_veda_scholar",
        "ranger_devraj", 
        "elder_rukmini"
    ]
    
    for npc_id in npcs_to_test:
        print(f"\nTesting {npc_id}:")
        
        # Test greeting
        response = npc_manager.interact_with_npc(npc_id)
        print(f"Greeting: {response['response']}")
        
        # Test conversation
        response = npc_manager.interact_with_npc(npc_id, "Tell me about this place")
        print(f"Conversation: {response['response']}")
        
        # Test quest offer
        response = npc_manager.interact_with_npc(npc_id, "Can you help me?")
        print(f"Quest: {response['response']}")
        
        print("-" * 30)
    
    print("\n📊 All NPCs Status:")
    status = npc_manager.get_all_npcs_status()
    for npc_id, info in status.items():
        print(f"  {info['name']}: {info['region']} - {'Available' if info['available'] else 'Busy'}")