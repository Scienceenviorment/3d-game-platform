#!/usr/bin/env python3
"""
Ancient Bharat Quest System
Comprehensive quest management using Python dataclasses and JSON
"""

import json
import time
import random
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Any
from enum import Enum


class QuestType(Enum):
    """Types of quests in Ancient Bharat"""
    MAIN = "main"                    # Primary storyline quests
    SIDE = "side"                    # Optional side quests
    DAILY = "daily"                  # Daily repeatable tasks
    CULTURAL = "cultural"            # Cultural exploration quests
    COLLECTION = "collection"        # Item gathering quests


class QuestStatus(Enum):
    """Quest completion status"""
    AVAILABLE = "available"          # Quest can be started
    ACTIVE = "active"                # Quest is in progress
    COMPLETED = "completed"          # Quest finished successfully
    FAILED = "failed"                # Quest failed
    LOCKED = "locked"                # Prerequisites not met


class QuestDifficulty(Enum):
    """Quest difficulty levels"""
    EASY = "easy"                    # Level 1-3
    MEDIUM = "medium"                # Level 4-7
    HARD = "hard"                    # Level 8-12
    LEGENDARY = "legendary"          # Level 13+


@dataclass
class QuestObjective:
    """Individual quest objective using Python dataclass"""
    objective_id: str                # Unique identifier
    description: str                 # What player needs to do
    target_type: str                 # "collect", "talk", "visit", "defeat"
    target_id: str                   # ID of target (item, npc, location)
    current_count: int = 0           # Progress towards target
    required_count: int = 1          # How many needed to complete
    completed: bool = False          # Objective completion status
    
    def update_progress(self, amount: int = 1) -> bool:
        """Update objective progress"""
        self.current_count += amount
        if self.current_count >= self.required_count:
            self.completed = True
        return self.completed
    
    def get_progress_text(self) -> str:
        """Get formatted progress text"""
        if self.target_type == "collect":
            return f"Collect {self.target_id}: {self.current_count}/{self.required_count}"
        elif self.target_type == "talk":
            return f"Speak with {self.target_id}: {'✓' if self.completed else '○'}"
        elif self.target_type == "visit":
            return f"Visit {self.target_id}: {'✓' if self.completed else '○'}"
        else:
            return f"{self.description}: {self.current_count}/{self.required_count}"


@dataclass
class QuestReward:
    """Quest reward structure"""
    experience: int = 0              # XP reward
    gold: int = 0                    # Currency reward
    items: List[str] = field(default_factory=list)  # Item rewards
    reputation: Dict[str, int] = field(default_factory=dict)  # NPC reputation
    special_unlock: Optional[str] = None  # Special content unlocked


@dataclass
class Quest:
    """Main quest data structure using Python dataclass"""
    quest_id: str                    # Unique quest identifier
    title: str                       # Quest display name
    description: str                 # Quest description
    giver_npc: str                   # NPC who gives this quest
    quest_type: QuestType            # Type of quest
    difficulty: QuestDifficulty      # Difficulty level
    
    # Quest requirements
    level_required: int = 1          # Minimum player level
    prerequisites: List[str] = field(default_factory=list)  # Required completed quests
    region_required: Optional[str] = None  # Required region
    
    # Quest progress
    objectives: List[QuestObjective] = field(default_factory=list)
    status: QuestStatus = QuestStatus.AVAILABLE
    started_at: Optional[float] = None    # Timestamp when started
    completed_at: Optional[float] = None  # Timestamp when completed
    
    # Quest rewards
    rewards: QuestReward = field(default_factory=QuestReward)
    
    # Quest narrative
    start_dialogue: str = ""         # What NPC says when giving quest
    progress_dialogue: str = ""      # What NPC says during progress
    completion_dialogue: str = ""    # What NPC says when completed
    
    def start_quest(self) -> bool:
        """Start the quest"""
        if self.status == QuestStatus.AVAILABLE:
            self.status = QuestStatus.ACTIVE
            self.started_at = time.time()
            return True
        return False
    
    def complete_quest(self) -> bool:
        """Complete the quest"""
        if self.status == QuestStatus.ACTIVE and self.all_objectives_completed():
            self.status = QuestStatus.COMPLETED
            self.completed_at = time.time()
            return True
        return False
    
    def all_objectives_completed(self) -> bool:
        """Check if all objectives are completed"""
        return all(obj.completed for obj in self.objectives)
    
    def get_progress_percentage(self) -> float:
        """Get overall quest progress as percentage"""
        if not self.objectives:
            return 0.0
        
        completed_objectives = sum(1 for obj in self.objectives if obj.completed)
        return (completed_objectives / len(self.objectives)) * 100.0
    
    def get_active_objectives(self) -> List[QuestObjective]:
        """Get list of incomplete objectives"""
        return [obj for obj in self.objectives if not obj.completed]
    
    def update_objective(self, objective_id: str, amount: int = 1) -> bool:
        """Update specific objective progress"""
        for objective in self.objectives:
            if objective.objective_id == objective_id:
                objective.update_progress(amount)
                
                # Check if quest is now complete
                if self.all_objectives_completed() and self.status == QuestStatus.ACTIVE:
                    self.complete_quest()
                    return True
        return False


class AncientBharatQuestSystem:
    """Main quest management system for Ancient Bharat"""
    
    def __init__(self):
        """Initialize quest system"""
        self.quests: Dict[str, Quest] = {}           # All available quests
        self.player_quests: Dict[str, Dict[str, Quest]] = {}  # Player quest progress
        self.daily_quests: Dict[str, List[Quest]] = {}  # Daily quest rotation
        
        # Initialize quest database
        self.initialize_main_quests()
        self.initialize_side_quests()
        self.initialize_daily_quests()
        self.initialize_cultural_quests()
    
    def initialize_main_quests(self):
        """Create main storyline quests"""
        
        # Main Quest 1: The Scholars Call
        scholars_call = Quest(
            quest_id="main_001_scholars_call",
            title="The Scholar's Call",
            description="Meet Arunima, the Veda Scholar, in Indrapura City to learn about the lost Sarasvati Map.",
            giver_npc="village_elder",
            quest_type=QuestType.MAIN,
            difficulty=QuestDifficulty.EASY,
            level_required=1,
            region_required="indrapura_city",
            start_dialogue="Young traveler, seek out Arunima in the great city. She possesses knowledge of ancient mysteries.",
            progress_dialogue="Have you spoken with Arunima yet? She awaits in the Temple of Knowledge.",
            completion_dialogue="Excellent! Now you understand the importance of the Sarasvati Map fragments."
        )
        
        # Add objectives
        scholars_call.objectives = [
            QuestObjective(
                objective_id="travel_to_city",
                description="Travel to Indrapura City",
                target_type="visit",
                target_id="indrapura_city"
            ),
            QuestObjective(
                objective_id="meet_arunima",
                description="Speak with Arunima, the Veda Scholar",
                target_type="talk",
                target_id="veda_scholar_arunima"
            )
        ]
        
        # Set rewards
        scholars_call.rewards = QuestReward(
            experience=100,
            gold=50,
            reputation={"veda_scholar_arunima": 10}
        )
        
        self.quests[scholars_call.quest_id] = scholars_call
        
        # Main Quest 2: First Fragment
        first_fragment = Quest(
            quest_id="main_002_first_fragment",
            title="Echoes in the Dust",
            description="Search the Dust Plains for the first Sarasvati Map fragment near ancient ruins.",
            giver_npc="veda_scholar_arunima",
            quest_type=QuestType.MAIN,
            difficulty=QuestDifficulty.MEDIUM,
            level_required=2,
            prerequisites=["main_001_scholars_call"],
            region_required="dust_plains",
            start_dialogue="The first fragment lies buried in the Dust Plains, where ancient kingdoms once flourished.",
            completion_dialogue="Remarkable! This fragment shows part of the sacred river's course. We need six more."
        )
        
        first_fragment.objectives = [
            QuestObjective(
                objective_id="explore_dust_plains",
                description="Explore the Dust Plains region",
                target_type="visit",
                target_id="dust_plains"
            ),
            QuestObjective(
                objective_id="find_ancient_ruins",
                description="Locate ancient ruins in the Dust Plains",
                target_type="visit",
                target_id="dust_plains_ruins"
            ),
            QuestObjective(
                objective_id="collect_fragment_1",
                description="Collect the first Sarasvati Map fragment",
                target_type="collect",
                target_id="sarasvati_fragment_1"
            )
        ]
        
        first_fragment.rewards = QuestReward(
            experience=250,
            gold=100,
            items=["ancient_scroll"],
            reputation={"veda_scholar_arunima": 15}
        )
        
        self.quests[first_fragment.quest_id] = first_fragment
        
        # Main Quest 3: The Forest's Secret
        forest_secret = Quest(
            quest_id="main_003_forest_secret",
            title="The Forest's Secret",
            description="Venture into Narmada Forest to find the second fragment hidden by forest spirits.",
            giver_npc="veda_scholar_arunima",
            quest_type=QuestType.MAIN,
            difficulty=QuestDifficulty.MEDIUM,
            level_required=4,
            prerequisites=["main_002_first_fragment"],
            region_required="narmada_forest",
            start_dialogue="The forest spirits guard the next fragment. Approach with respect and wisdom.",
            completion_dialogue="The spirits have accepted you. This fragment reveals more of the sacred geography."
        )
        
        forest_secret.objectives = [
            QuestObjective(
                objective_id="enter_narmada_forest",
                description="Enter the Narmada Forest",
                target_type="visit",
                target_id="narmada_forest"
            ),
            QuestObjective(
                objective_id="find_spirit_grove",
                description="Locate the Spirit Grove",
                target_type="visit",
                target_id="spirit_grove"
            ),
            QuestObjective(
                objective_id="commune_with_spirits",
                description="Perform ritual communion with forest spirits",
                target_type="talk",
                target_id="forest_spirits"
            ),
            QuestObjective(
                objective_id="collect_fragment_2",
                description="Collect the second Sarasvati Map fragment",
                target_type="collect",
                target_id="sarasvati_fragment_2"
            )
        ]
        
        forest_secret.rewards = QuestReward(
            experience=350,
            gold=150,
            items=["forest_blessing", "spirit_charm"],
            reputation={"forest_spirits": 20, "veda_scholar_arunima": 10}
        )
        
        self.quests[forest_secret.quest_id] = forest_secret
    
    def initialize_side_quests(self):
        """Create side quests for additional content"""
        
        # Side Quest: Village Reconstruction
        village_rebuild = Quest(
            quest_id="side_001_village_rebuild",
            title="Rebuilding the Past",
            description="Help Rukmini rebuild damaged structures in her village using traditional methods.",
            giver_npc="village_elder_rukmini",
            quest_type=QuestType.SIDE,
            difficulty=QuestDifficulty.EASY,
            level_required=2,
            region_required="indrapura_city",
            start_dialogue="Our village needs restoration. Will you help us rebuild using the old ways?",
            completion_dialogue="Thank you! Our village stands strong again, honoring our ancestors."
        )
        
        village_rebuild.objectives = [
            QuestObjective(
                objective_id="collect_traditional_materials",
                description="Collect traditional building materials",
                target_type="collect",
                target_id="building_materials",
                required_count=10
            ),
            QuestObjective(
                objective_id="repair_temple",
                description="Repair the village temple",
                target_type="visit",
                target_id="village_temple"
            ),
            QuestObjective(
                objective_id="restore_well",
                description="Restore the village well",
                target_type="visit",
                target_id="village_well"
            )
        ]
        
        village_rebuild.rewards = QuestReward(
            experience=200,
            gold=75,
            reputation={"village_elder_rukmini": 25},
            special_unlock="village_crafting_access"
        )
        
        self.quests[village_rebuild.quest_id] = village_rebuild
        
        # Side Quest: Ranger's Wisdom
        rangers_wisdom = Quest(
            quest_id="side_002_rangers_wisdom",
            title="Paths of the Ranger",
            description="Learn wilderness survival from Devraj, the experienced ranger.",
            giver_npc="ranger_devraj",
            quest_type=QuestType.SIDE,
            difficulty=QuestDifficulty.MEDIUM,
            level_required=3,
            start_dialogue="The wilderness teaches many lessons. Are you ready to learn?",
            completion_dialogue="You have learned well. The land will guide your steps."
        )
        
        rangers_wisdom.objectives = [
            QuestObjective(
                objective_id="track_animals",
                description="Successfully track 5 different animal species",
                target_type="collect",
                target_id="animal_tracks",
                required_count=5
            ),
            QuestObjective(
                objective_id="identify_plants",
                description="Identify 8 medicinal plants",
                target_type="collect",
                target_id="medicinal_plants",
                required_count=8
            ),
            QuestObjective(
                objective_id="navigate_wilderness",
                description="Navigate through unmarked wilderness areas",
                target_type="visit",
                target_id="wilderness_checkpoint"
            )
        ]
        
        rangers_wisdom.rewards = QuestReward(
            experience=300,
            items=["wilderness_guide", "tracking_tools", "herbal_pouch"],
            reputation={"ranger_devraj": 30},
            special_unlock="wilderness_navigation"
        )
        
        self.quests[rangers_wisdom.quest_id] = rangers_wisdom
    
    def initialize_daily_quests(self):
        """Create daily repeatable quests"""
        
        # Daily Quest: Sacred Offering
        sacred_offering = Quest(
            quest_id="daily_001_sacred_offering",
            title="Daily Sacred Offering",
            description="Collect flowers and offer them at the temple for blessings.",
            giver_npc="temple_priest",
            quest_type=QuestType.DAILY,
            difficulty=QuestDifficulty.EASY,
            level_required=1,
            start_dialogue="The gods appreciate daily offerings of fresh flowers.",
            completion_dialogue="Your devotion is noted. May the gods bless your journey."
        )
        
        sacred_offering.objectives = [
            QuestObjective(
                objective_id="collect_lotus_flowers",
                description="Collect lotus flowers",
                target_type="collect",
                target_id="lotus_flowers",
                required_count=5
            ),
            QuestObjective(
                objective_id="offer_at_temple",
                description="Make offering at temple altar",
                target_type="visit",
                target_id="temple_altar"
            )
        ]
        
        sacred_offering.rewards = QuestReward(
            experience=50,
            gold=25,
            items=["blessing_charm"]
        )
        
        self.quests[sacred_offering.quest_id] = sacred_offering
        
        # Daily Quest: Merchant's Delivery
        merchant_delivery = Quest(
            quest_id="daily_002_merchant_delivery",
            title="Merchant's Delivery",
            description="Deliver goods between regions for traveling merchants.",
            giver_npc="traveling_merchant",
            quest_type=QuestType.DAILY,
            difficulty=QuestDifficulty.MEDIUM,
            level_required=3,
            start_dialogue="I need someone reliable to deliver these goods. Will you help?",
            completion_dialogue="Excellent! Your reputation as a trustworthy courier grows."
        )
        
        merchant_delivery.objectives = [
            QuestObjective(
                objective_id="collect_goods",
                description="Collect merchant goods",
                target_type="collect",
                target_id="trade_goods"
            ),
            QuestObjective(
                objective_id="deliver_to_destination",
                description="Deliver goods to destination",
                target_type="visit",
                target_id="delivery_point"
            )
        ]
        
        merchant_delivery.rewards = QuestReward(
            experience=75,
            gold=50,
            reputation={"merchants_guild": 5}
        )
        
        self.quests[merchant_delivery.quest_id] = merchant_delivery
    
    def initialize_cultural_quests(self):
        """Create cultural exploration quests"""
        
        # Cultural Quest: Ancient Scripts
        ancient_scripts = Quest(
            quest_id="cultural_001_ancient_scripts",
            title="Deciphering Ancient Scripts",
            description="Find and translate ancient Sanskrit inscriptions throughout the world.",
            giver_npc="veda_scholar_arunima",
            quest_type=QuestType.CULTURAL,
            difficulty=QuestDifficulty.HARD,
            level_required=5,
            start_dialogue="Ancient wisdom is carved in stone across our land. Help me collect these teachings.",
            completion_dialogue="These inscriptions reveal profound wisdom from our ancestors."
        )
        
        ancient_scripts.objectives = [
            QuestObjective(
                objective_id="find_inscriptions",
                description="Find ancient Sanskrit inscriptions",
                target_type="collect",
                target_id="sanskrit_inscriptions",
                required_count=12
            ),
            QuestObjective(
                objective_id="translate_texts",
                description="Successfully translate the ancient texts",
                target_type="talk",
                target_id="translation_complete"
            )
        ]
        
        ancient_scripts.rewards = QuestReward(
            experience=500,
            gold=200,
            items=["scholar_robes", "translation_tools"],
            reputation={"veda_scholar_arunima": 50},
            special_unlock="ancient_language_mastery"
        )
        
        self.quests[ancient_scripts.quest_id] = ancient_scripts
    
    # Quest management methods
    def get_available_quests(self, player_id: str, player_level: int, current_region: str) -> List[Quest]:
        """Get quests available to player"""
        available = []
        
        for quest in self.quests.values():
            # Check if player meets requirements
            if (quest.level_required <= player_level and
                (not quest.region_required or quest.region_required == current_region) and
                self.check_prerequisites(player_id, quest.prerequisites)):
                
                # Check if quest is not already completed
                player_quest_data = self.get_player_quest_data(player_id)
                if quest.quest_id not in player_quest_data or player_quest_data[quest.quest_id].status != QuestStatus.COMPLETED:
                    available.append(quest)
        
        return available
    
    def start_quest(self, player_id: str, quest_id: str) -> bool:
        """Start a quest for player"""
        if quest_id not in self.quests:
            return False
        
        # Get or create player quest data
        if player_id not in self.player_quests:
            self.player_quests[player_id] = {}
        
        # Copy quest to player's quest log
        quest_copy = self.copy_quest(self.quests[quest_id])
        if quest_copy.start_quest():
            self.player_quests[player_id][quest_id] = quest_copy
            return True
        
        return False
    
    def update_quest_progress(self, player_id: str, quest_id: str, objective_id: str, amount: int = 1) -> bool:
        """Update quest objective progress"""
        if (player_id in self.player_quests and 
            quest_id in self.player_quests[player_id]):
            
            quest = self.player_quests[player_id][quest_id]
            return quest.update_objective(objective_id, amount)
        
        return False
    
    def get_player_quest_data(self, player_id: str) -> Dict[str, Quest]:
        """Get all quest data for player"""
        return self.player_quests.get(player_id, {})
    
    def get_active_quests(self, player_id: str) -> List[Quest]:
        """Get player's active quests"""
        player_quests = self.get_player_quest_data(player_id)
        return [quest for quest in player_quests.values() if quest.status == QuestStatus.ACTIVE]
    
    def get_completed_quests(self, player_id: str) -> List[Quest]:
        """Get player's completed quests"""
        player_quests = self.get_player_quest_data(player_id)
        return [quest for quest in player_quests.values() if quest.status == QuestStatus.COMPLETED]
    
    def check_prerequisites(self, player_id: str, prerequisites: List[str]) -> bool:
        """Check if player has completed prerequisite quests"""
        if not prerequisites:
            return True
        
        completed_quests = self.get_completed_quests(player_id)
        completed_quest_ids = {quest.quest_id for quest in completed_quests}
        
        return all(prereq in completed_quest_ids for prereq in prerequisites)
    
    def copy_quest(self, quest: Quest) -> Quest:
        """Create a copy of quest for player quest log"""
        # Convert to dict and back to create deep copy
        quest_dict = asdict(quest)
        return Quest(**quest_dict)
    
    def generate_daily_quests(self, player_id: str, date: str) -> List[Quest]:
        """Generate daily quests for player"""
        # Use date as seed for consistent daily quests
        random.seed(hash(f"{player_id}_{date}"))
        
        daily_quest_ids = [qid for qid, quest in self.quests.items() 
                          if quest.quest_type == QuestType.DAILY]
        
        # Select 2-3 random daily quests
        selected_quests = random.sample(daily_quest_ids, min(3, len(daily_quest_ids)))
        return [self.copy_quest(self.quests[qid]) for qid in selected_quests]
    
    def get_quest_statistics(self, player_id: str) -> Dict[str, Any]:
        """Get quest completion statistics"""
        player_quests = self.get_player_quest_data(player_id)
        
        stats = {
            "total_quests_available": len(self.quests),
            "quests_started": len(player_quests),
            "quests_active": len(self.get_active_quests(player_id)),
            "quests_completed": len(self.get_completed_quests(player_id)),
            "main_quest_progress": 0,
            "side_quest_completion": 0,
            "daily_quests_completed": 0
        }
        
        # Calculate detailed statistics
        for quest in player_quests.values():
            if quest.quest_type == QuestType.MAIN and quest.status == QuestStatus.COMPLETED:
                stats["main_quest_progress"] += 1
            elif quest.quest_type == QuestType.SIDE and quest.status == QuestStatus.COMPLETED:
                stats["side_quest_completion"] += 1
            elif quest.quest_type == QuestType.DAILY and quest.status == QuestStatus.COMPLETED:
                stats["daily_quests_completed"] += 1
        
        return stats


# Create global quest system instance
ancient_bharat_quests = AncientBharatQuestSystem()


# Utility functions for easy access
def get_quest_system() -> AncientBharatQuestSystem:
    """Get global quest system"""
    return ancient_bharat_quests


def start_player_quest(player_id: str, quest_id: str) -> bool:
    """Start quest for player"""
    return ancient_bharat_quests.start_quest(player_id, quest_id)


def update_player_quest(player_id: str, quest_id: str, objective_id: str, amount: int = 1) -> bool:
    """Update player quest progress"""
    return ancient_bharat_quests.update_quest_progress(player_id, quest_id, objective_id, amount)


# Example usage and testing
if __name__ == "__main__":
    print("🗺️ Ancient Bharat Quest System")
    print("=" * 50)
    
    quest_system = get_quest_system()
    
    # Test quest creation
    print("\n📋 Available Quests:")
    for quest_id, quest in quest_system.quests.items():
        print(f"  {quest.title} ({quest.quest_type.value})")
        print(f"    Level: {quest.level_required}, Difficulty: {quest.difficulty.value}")
        print(f"    Objectives: {len(quest.objectives)}")
    
    # Test player quest system
    print("\n👤 Testing Player Quest System:")
    test_player = "test_player_001"
    
    # Start main quest
    if quest_system.start_quest(test_player, "main_001_scholars_call"):
        print("  ✅ Started main quest: The Scholar's Call")
    
    # Update quest progress
    if quest_system.update_quest_progress(test_player, "main_001_scholars_call", "travel_to_city"):
        print("  📍 Completed objective: Travel to city")
    
    # Get active quests
    active = quest_system.get_active_quests(test_player)
    print(f"  📊 Active quests: {len(active)}")
    
    for quest in active:
        print(f"    {quest.title}: {quest.get_progress_percentage():.1f}% complete")
    
    # Get statistics
    stats = quest_system.get_quest_statistics(test_player)
    print(f"\n📈 Quest Statistics:")
    print(f"  Quests Started: {stats['quests_started']}")
    print(f"  Quests Active: {stats['quests_active']}")
    print(f"  Quests Completed: {stats['quests_completed']}")
    
    print("\n✅ Quest system test completed!")