#!/usr/bin/env python3
"""
AI Agent System for Ancient Bharat NPCs
Beast Taming storyline based on "Classic of Mountains and Seas" adapted to Indian mythology
"""

import random
import time
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta


class BeastType(Enum):
    """Types of mythical beasts in Indian mythology"""
    GARUDA = "garuda"           # Divine eagle, mount of Vishnu
    NAGA = "naga"               # Serpent beings, guardians of treasures
    KINNARA = "kinnara"         # Half-human, half-horse musicians
    VANARA = "vanara"           # Monkey beings, allies of Rama
    RAKSHASA = "rakshasa"       # Shape-shifting demons
    APSARA = "apsara"           # Celestial dancers and water spirits
    GANDHARVA = "gandharva"     # Celestial musicians
    MAKARA = "makara"           # Crocodile-like water creatures
    SIMHA = "simha"             # Divine lions
    GAJA = "gaja"               # Elephants with divine powers


class BeastRarity(Enum):
    """Rarity levels of beasts"""
    COMMON = "common"
    UNCOMMON = "uncommon" 
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"


@dataclass
class MythicalBeast:
    """A mythical beast that can be tamed"""
    beast_id: str
    name: str
    beast_type: BeastType
    rarity: BeastRarity
    region: str
    description: str
    abilities: List[str]
    taming_difficulty: int  # 1-100
    required_level: int
    lore: str  # Story from Indian mythology
    temperament: str
    
    # Taming requirements
    required_items: List[str] = field(default_factory=list)
    required_knowledge: List[str] = field(default_factory=list)
    preferred_approach: str = ""


@dataclass
class PlayerBeastProgress:
    """Player's progress in beast taming"""
    player_id: str
    discovered_beasts: List[str] = field(default_factory=list)
    tamed_beasts: List[str] = field(default_factory=list)
    beast_knowledge: Dict[str, int] = field(default_factory=dict)  # knowledge levels
    taming_experience: int = 0
    current_region_explored: str = ""
    
    # Story progress
    mountains_seas_fragments: int = 0  # Fragments of the ancient text discovered
    ancient_taming_techniques: List[str] = field(default_factory=list)


class AIPersonalityTrait(Enum):
    """AI personality traits for dynamic responses"""
    SCHOLARLY = "scholarly"
    ADVENTUROUS = "adventurous"
    PROTECTIVE = "protective"
    MYSTICAL = "mystical"
    PRAGMATIC = "pragmatic"
    NURTURING = "nurturing"


@dataclass
class AIMemory:
    """AI agent memory system"""
    player_interactions: Dict[str, List[str]] = field(default_factory=dict)
    conversation_history: List[str] = field(default_factory=list)
    player_preferences: Dict[str, Any] = field(default_factory=dict)
    last_interaction_time: Optional[datetime] = None
    relationship_level: int = 0  # 0-100, how well they know the player
    topics_discussed: List[str] = field(default_factory=list)


class AIAgent:
    """Advanced AI agent for realistic NPC behavior"""
    
    def __init__(self, npc_id: str, name: str, personality_traits: List[AIPersonalityTrait],
                 beast_specialization: List[BeastType], knowledge_areas: List[str]):
        self.npc_id = npc_id
        self.name = name
        self.personality_traits = personality_traits
        self.beast_specialization = beast_specialization
        self.knowledge_areas = knowledge_areas
        self.memory = AIMemory()
        
        # Dynamic response templates
        self.response_templates = self._initialize_response_templates()
        self.beast_knowledge = self._initialize_beast_knowledge()
        
    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """Initialize dynamic response templates based on personality"""
        templates = {
            "greeting": [],
            "beast_discussion": [],
            "taming_advice": [],
            "lore_sharing": [],
            "farewell": []
        }
        
        # Customize templates based on personality traits
        if AIPersonalityTrait.SCHOLARLY in self.personality_traits:
            templates["greeting"].extend([
                "Ah, a seeker of knowledge! I've been studying the ancient texts...",
                "Welcome, student. The scriptures speak of great beasts that once roamed our lands...",
                "Namaste. I see the curiosity of a true scholar in your eyes."
            ])
            templates["beast_discussion"].extend([
                "According to the Puranas, this beast is mentioned in the {ancient_text}...",
                "The classical texts describe {beast_name} as {description}...",
                "I've found references to similar creatures in {source}..."
            ])
            
        if AIPersonalityTrait.ADVENTUROUS in self.personality_traits:
            templates["greeting"].extend([
                "Another adventurer! The wilds are calling, aren't they?",
                "I can see the spirit of exploration in you, friend!",
                "The forests hold many secrets for those brave enough to seek them."
            ])
            templates["taming_advice"].extend([
                "From my experience in the field, {beast_name} responds best to {approach}...",
                "I've tracked {beast_type} for years - here's what I've learned...",
                "The trick with {beast_name} is patience and {technique}..."
            ])
            
        return templates
    
    def _initialize_beast_knowledge(self) -> Dict[str, MythicalBeast]:
        """Initialize knowledge of mythical beasts"""
        beasts = {}
        
        # Garuda - Divine Eagle
        beasts["garuda_minor"] = MythicalBeast(
            beast_id="garuda_minor",
            name="Suparna",
            beast_type=BeastType.GARUDA,
            rarity=BeastRarity.RARE,
            region="Himalayan Peaks",
            description="A majestic eagle with golden feathers and divine wisdom",
            abilities=["Sky Travel", "Divine Sight", "Wind Control"],
            taming_difficulty=75,
            required_level=15,
            lore="Born from the union of Kashyapa and Vinata, these eagles carry the blood of Garuda himself. They serve as messengers between mortals and gods.",
            temperament="Proud but noble",
            required_items=["Sacred Soma", "Golden Feather"],
            required_knowledge=["Vedic Mantras", "Sky Navigation"],
            preferred_approach="Respectful offering and demonstration of worthiness"
        )
        
        # Naga - Serpent Being
        beasts["naga_guardian"] = MythicalBeast(
            beast_id="naga_guardian",
            name="Vasuki's Kin",
            beast_type=BeastType.NAGA,
            rarity=BeastRarity.EPIC,
            region="Sacred Ponds",
            description="An ancient serpent with jeweled scales and deep wisdom",
            abilities=["Treasure Location", "Water Control", "Poison Immunity"],
            taming_difficulty=80,
            required_level=20,
            lore="Descendants of the great Naga kings, these serpents guard ancient treasures and sacred knowledge hidden beneath the waters.",
            temperament="Wise but testing",
            required_items=["Precious Gems", "Sacred Water"],
            required_knowledge=["Naga History", "Underwater Breathing"],
            preferred_approach="Demonstration of wisdom and respect for water"
        )
        
        # Add more beasts based on specialization
        return beasts
    
    def generate_response(self, player_input: str, context: Dict[str, Any]) -> str:
        """Generate dynamic AI response based on input and context"""
        # Update memory
        self._update_memory(player_input, context)
        
        # Analyze input for topics
        topics = self._analyze_input_topics(player_input)
        
        # Generate contextual response
        response = self._create_contextual_response(topics, context)
        
        # Add personality touches
        response = self._add_personality_touches(response)
        
        return response
    
    def _update_memory(self, player_input: str, context: Dict[str, Any]):
        """Update AI memory with new interaction"""
        player_id = context.get("player_id", "unknown")
        
        if player_id not in self.memory.player_interactions:
            self.memory.player_interactions[player_id] = []
        
        self.memory.player_interactions[player_id].append(player_input)
        self.memory.conversation_history.append(f"Player: {player_input}")
        self.memory.last_interaction_time = datetime.now()
        
        # Increase relationship based on interaction quality
        if any(word in player_input.lower() for word in ["please", "thank", "help", "learn"]):
            self.memory.relationship_level = min(100, self.memory.relationship_level + 1)
    
    def _analyze_input_topics(self, player_input: str) -> List[str]:
        """Analyze player input to identify topics"""
        topics = []
        input_lower = player_input.lower()
        
        # Beast-related topics
        for beast_type in BeastType:
            if beast_type.value in input_lower:
                topics.append(f"beast_{beast_type.value}")
        
        # General topics
        topic_keywords = {
            "taming": ["tame", "taming", "train", "bond"],
            "lore": ["story", "legend", "myth", "history", "ancient"],
            "location": ["where", "find", "locate", "search"],
            "advice": ["help", "how", "guide", "teach", "learn"],
            "greeting": ["hello", "hi", "namaste", "greetings"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _create_contextual_response(self, topics: List[str], context: Dict[str, Any]) -> str:
        """Create response based on identified topics and context"""
        player_level = context.get("player_level", 1)
        player_beasts = context.get("player_beasts", [])
        
        responses = []
        
        # Handle different topics
        if "greeting" in topics:
            if self.memory.relationship_level < 20:
                responses.append(random.choice(self.response_templates["greeting"]))
            else:
                responses.append(f"Welcome back, friend! I remember our previous discussions about {random.choice(self.memory.topics_discussed) if self.memory.topics_discussed else 'the ancient ways'}.")
        
        if any(topic.startswith("beast_") for topic in topics):
            beast_type = next((topic.split("_")[1] for topic in topics if topic.startswith("beast_")), None)
            if beast_type and beast_type in [bt.value for bt in self.beast_specialization]:
                responses.append(self._generate_beast_response(beast_type, player_level))
        
        if "taming" in topics:
            responses.append(self._generate_taming_advice(player_level, player_beasts))
        
        if "lore" in topics:
            responses.append(self._generate_lore_response())
        
        # Default response if no specific topics identified
        if not responses:
            responses.append("I sense great potential in you, young seeker. What knowledge do you seek about the mystical beasts of our land?")
        
        return " ".join(responses)
    
    def _generate_beast_response(self, beast_type: str, player_level: int) -> str:
        """Generate response about specific beast type"""
        responses = [
            f"Ah, the {beast_type}! These magnificent beings are truly special.",
            f"I have studied the {beast_type} for many years. They are fascinating creatures.",
            f"The {beast_type} hold a special place in our ancient traditions."
        ]
        
        if player_level < 10:
            responses.append(f"However, approaching a {beast_type} requires great preparation. Build your skills first.")
        else:
            responses.append(f"You seem ready to learn more about the {beast_type}. Shall I share what I know?")
        
        return random.choice(responses[:2]) + " " + responses[-1]
    
    def _generate_taming_advice(self, player_level: int, player_beasts: List[str]) -> str:
        """Generate advice about beast taming"""
        if player_level < 5:
            return "Beast taming is an ancient art that requires patience, wisdom, and respect. Start by studying the creatures' nature and building your spiritual strength."
        elif len(player_beasts) == 0:
            return "For your first taming attempt, I suggest starting with a gentle creature. Observe their habits, learn their preferences, and approach with offerings they value."
        else:
            return "I see you've already formed bonds with some creatures. Each beast is unique - what works for one may not work for another. Trust your instincts and the wisdom you've gained."
    
    def _generate_lore_response(self) -> str:
        """Generate response about ancient lore"""
        lore_snippets = [
            "The ancient texts speak of a time when humans and beasts lived in harmony, sharing wisdom and power.",
            "In the Classic of Mountains and Seas, adapted to our Indian traditions, we learn of creatures beyond imagination.",
            "The Puranas tell us that each beast carries a fragment of divine consciousness - this is why taming is truly a spiritual journey.",
            "Long ago, great sages could commune with all creatures. This knowledge was recorded in texts that are now scattered like leaves in the wind."
        ]
        return random.choice(lore_snippets)
    
    def _add_personality_touches(self, response: str) -> str:
        """Add personality-specific touches to response"""
        if AIPersonalityTrait.SCHOLARLY in self.personality_traits:
            # Add scholarly phrases
            scholarly_touches = [
                "As the scriptures say, ",
                "According to ancient wisdom, ",
                "The texts remind us that ",
                "In my studies, I've found that "
            ]
            if random.random() < 0.3:  # 30% chance to add scholarly touch
                touch = random.choice(scholarly_touches)
                response = touch + response.lower()
        
        if AIPersonalityTrait.MYSTICAL in self.personality_traits:
            # Add mystical elements
            mystical_endings = [
                " ...as the cosmic winds whisper.",
                " The stars align to guide your path.",
                " Trust in the ancient energies that surround us.",
                " May the divine essence guide your journey."
            ]
            if random.random() < 0.2:  # 20% chance
                response += random.choice(mystical_endings)
        
        return response


# Create AI agents for each NPC
def create_arunima_ai_agent() -> AIAgent:
    """Create AI agent for Arunima - The Veda Scholar"""
    return AIAgent(
        npc_id="arunima",
        name="Arunima",
        personality_traits=[AIPersonalityTrait.SCHOLARLY, AIPersonalityTrait.MYSTICAL],
        beast_specialization=[BeastType.GARUDA, BeastType.APSARA, BeastType.GANDHARVA],
        knowledge_areas=["Vedic Texts", "Ancient Scriptures", "Divine Beasts", "Sacred Rituals"]
    )


def create_devraj_ai_agent() -> AIAgent:
    """Create AI agent for Devraj - The Forest Ranger"""
    return AIAgent(
        npc_id="devraj",
        name="Devraj",
        personality_traits=[AIPersonalityTrait.ADVENTUROUS, AIPersonalityTrait.PRAGMATIC],
        beast_specialization=[BeastType.VANARA, BeastType.SIMHA, BeastType.GAJA],
        knowledge_areas=["Beast Tracking", "Wilderness Survival", "Forest Creatures", "Practical Taming"]
    )


def create_rukmini_ai_agent() -> AIAgent:
    """Create AI agent for Rukmini - The Village Elder"""
    return AIAgent(
        npc_id="rukmini",
        name="Rukmini",
        personality_traits=[AIPersonalityTrait.NURTURING, AIPersonalityTrait.PROTECTIVE],
        beast_specialization=[BeastType.NAGA, BeastType.MAKARA, BeastType.KINNARA],
        knowledge_areas=["Village Traditions", "Protective Spirits", "Elder Wisdom", "Family Bonds"]
    )


# Beast Taming Story Integration
class BeastTamingStoryManager:
    """Manages the overarching beast taming storyline"""
    
    def __init__(self):
        self.story_fragments = self._initialize_story_fragments()
        self.player_progress = {}
    
    def _initialize_story_fragments(self) -> Dict[str, str]:
        """Initialize story fragments from the Mountains and Seas classic, adapted to India"""
        return {
            "prologue": """
            Long ago, in the golden age of Ancient Bharat, there existed a sacred text known as the 
            'Pashupati Shastra' - the Classic of Beasts and Sacred Lands. This ancient manuscript 
            contained the wisdom of taming and bonding with the mythical creatures that roamed our 
            subcontinent. When the great deluge came, the text was scattered across the seven sacred 
            regions of Bharat, its pages becoming one with the land itself.
            """,
            
            "first_fragment": """
            In the Himalayan peaks, where Garuda once rested, lies the first fragment. It speaks of 
            the Sky Tamers - those who could bond with celestial birds and traverse the heavens. 
            The fragment reveals that respect and demonstration of worthiness are key to earning 
            the trust of divine flying creatures.
            """,
            
            "second_fragment": """
            Deep in the sacred ponds and rivers, protected by the Naga guardians, the second fragment 
            rests. It tells of the Water Whisperers - humans who could speak with serpent beings and 
            learn the locations of hidden treasures. Wisdom and respect for the aquatic realm are 
            essential for these bonds.
            """,
            
            "ancient_prophecy": """
            When one gathers all seven fragments and masters the bonds with beasts from each sacred 
            region, they shall become the Pashupati - the Lord of Beasts - capable of restoring 
            the ancient harmony between human and creature. This is the path that lies before you, 
            brave seeker.
            """
        }
    
    def get_story_fragment(self, fragment_id: str, player_progress: PlayerBeastProgress) -> str:
        """Get story fragment based on player progress"""
        if fragment_id in self.story_fragments:
            return self.story_fragments[fragment_id]
        return "The ancient memories remain hidden..."
    
    def check_story_advancement(self, player_progress: PlayerBeastProgress) -> Optional[str]:
        """Check if player has advanced enough to unlock new story content"""
        if player_progress.mountains_seas_fragments == 0 and len(player_progress.tamed_beasts) >= 1:
            player_progress.mountains_seas_fragments = 1
            return "first_fragment"
        elif player_progress.mountains_seas_fragments == 1 and player_progress.taming_experience >= 100:
            player_progress.mountains_seas_fragments = 2
            return "second_fragment"
        return None


# Global instances
arunima_ai = create_arunima_ai_agent()
devraj_ai = create_devraj_ai_agent()
rukmini_ai = create_rukmini_ai_agent()
story_manager = BeastTamingStoryManager()

# Test functionality
def test_ai_system():
    """Test the AI agent system"""
    print("🤖 Testing AI Agent System")
    print("=" * 50)
    
    # Test Arunima's response
    context = {"player_id": "test_player", "player_level": 5, "player_beasts": []}
    response = arunima_ai.generate_response("Tell me about Garuda", context)
    print(f"Arunima: {response}")
    print()
    
    # Test Devraj's response
    response = devraj_ai.generate_response("How do I tame forest beasts?", context)
    print(f"Devraj: {response}")
    print()
    
    # Test Rukmini's response
    response = rukmini_ai.generate_response("What ancient wisdom can you share?", context)
    print(f"Rukmini: {response}")
    print()
    
    print("✅ AI Agent system initialized successfully!")


if __name__ == "__main__":
    test_ai_system()