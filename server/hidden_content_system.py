#!/usr/bin/env python3
"""
Hidden Content and Secret Quest System
Mysterious areas, secret routes, and hidden quests that unlock based on player choices
Part of the "Beast Taming: Classic of Mountains and Seas" expansion
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum
from datetime import datetime


class SecretType(Enum):
    """Types of hidden content"""
    HIDDEN_QUEST = "hidden_quest"
    SECRET_AREA = "secret_area"
    MYSTERY_NPC = "mystery_npc"
    ANCIENT_RELIC = "ancient_relic"
    FORBIDDEN_KNOWLEDGE = "forbidden_knowledge"
    HIDDEN_CLASS = "hidden_class"
    SECRET_BEAST = "secret_beast"
    LEGENDARY_ITEM = "legendary_item"


class UnlockCondition(Enum):
    """How hidden content is unlocked"""
    KARMA_THRESHOLD = "karma_threshold"
    BEAST_COLLECTION = "beast_collection"
    ITEM_COMBINATION = "item_combination"
    LOCATION_SEQUENCE = "location_sequence"
    TIME_CONDITION = "time_condition"
    NPC_RELATIONSHIP = "npc_relationship"
    CHOICE_CONSEQUENCE = "choice_consequence"
    SKILL_MASTERY = "skill_mastery"
    DIVINE_FAVOR = "divine_favor"
    CORRUPTION_LEVEL = "corruption_level"


class SecretRarity(Enum):
    """Rarity of hidden content"""
    UNCOMMON = "uncommon"       # Found by careful exploration
    RARE = "rare"               # Requires specific knowledge
    EPIC = "epic"               # Multiple complex requirements
    LEGENDARY = "legendary"     # Extremely difficult to find
    MYTHICAL = "mythical"       # Nearly impossible, world-changing


@dataclass
class UnlockRequirement:
    """A requirement that must be met to unlock hidden content"""
    condition_type: UnlockCondition
    description: str
    
    # Specific parameters based on condition type
    value_required: Optional[Any] = None
    items_required: List[str] = field(default_factory=list)
    locations_required: List[str] = field(default_factory=list)
    npcs_required: List[str] = field(default_factory=list)
    
    # Timing
    time_sensitive: bool = False
    deadline: Optional[datetime] = None
    
    # Choice-based
    choices_required: List[str] = field(default_factory=list)
    
    # Progressive requirements
    cumulative: bool = False
    progress_needed: int = 1


@dataclass
class HiddenContent:
    """A piece of hidden content in the game"""
    content_id: str
    name: str
    description: str
    secret_type: SecretType
    rarity: SecretRarity
    
    # Unlock requirements
    unlock_requirements: List[UnlockRequirement] = field(default_factory=list)
    prerequisite_secrets: List[str] = field(default_factory=list)  # Other secrets needed first
    
    # Discovery method
    discovery_hints: List[str] = field(default_factory=list)
    false_leads: List[str] = field(default_factory=list)  # Red herrings
    
    # Rewards
    rewards: Dict[str, Any] = field(default_factory=dict)
    unlocks_content: List[str] = field(default_factory=list)  # What this unlocks
    
    # Story integration
    story_impact: str = ""
    world_changes: List[str] = field(default_factory=list)
    
    # Availability
    limited_time: bool = False
    max_discoverers: Optional[int] = None
    current_discoverers: int = 0
    
    # Location and access
    hidden_location: Optional[str] = None
    access_method: str = ""
    
    # Meta information
    creation_lore: str = ""     # How this secret came to exist
    developer_notes: str = ""   # For debugging and expansion


@dataclass
class SecretRoute:
    """A hidden path or route between locations"""
    route_id: str
    name: str
    description: str
    
    # Route endpoints
    start_location: str
    end_location: str
    waypoints: List[str] = field(default_factory=list)
    
    # Discovery and access
    unlock_requirements: List[UnlockRequirement] = field(default_factory=list)
    permanent_unlock: bool = True
    
    # Travel benefits
    travel_time_reduction: float = 0.5  # How much faster than normal routes
    special_encounters: List[str] = field(default_factory=list)
    hidden_resources: List[str] = field(default_factory=list)
    
    # Dangers and challenges
    hazards: List[str] = field(default_factory=list)
    guardians: List[str] = field(default_factory=list)  # Creatures that protect the route
    
    # Story elements
    historical_significance: str = ""
    route_lore: str = ""


@dataclass
class PlayerSecretProgress:
    """Tracks a player's progress with hidden content"""
    player_id: str
    
    # Discovered content
    discovered_secrets: Set[str] = field(default_factory=set)
    unlocked_routes: Set[str] = field(default_factory=set)
    active_mysteries: List[str] = field(default_factory=list)
    
    # Progress tracking
    secret_progress: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # secret_id: progress data
    clues_found: List[str] = field(default_factory=list)
    false_leads_followed: List[str] = field(default_factory=list)
    
    # Choice tracking for consequences
    major_choices_made: List[str] = field(default_factory=list)
    choice_consequences: Dict[str, List[str]] = field(default_factory=dict)
    
    # Discovery reputation
    secret_finder_level: int = 0  # Reputation as someone who finds secrets
    legendary_discoveries: int = 0
    
    # Current investigations
    active_investigations: Dict[str, datetime] = field(default_factory=dict)


class HiddenContentSystem:
    """Manages all hidden content, secret quests, and mysterious areas"""
    
    def __init__(self):
        self.hidden_content = self._initialize_hidden_content()
        self.secret_routes = self._initialize_secret_routes()
        self.player_progress = {}
        self.world_secrets_discovered = set()  # Global tracking
        
    def _initialize_hidden_content(self) -> Dict[str, HiddenContent]:
        """Initialize all hidden content in the game"""
        content = {}
        
        # Hidden Quest: The Lost Yaksha
        content["lost_yaksha_quest"] = HiddenContent(
            content_id="lost_yaksha_quest",
            name="The Lost Yaksha's Lament",
            description="A powerful yaksha (nature spirit) was banished and seeks redemption",
            secret_type=SecretType.HIDDEN_QUEST,
            rarity=SecretRarity.RARE,
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.BEAST_COLLECTION,
                    description="Must have tamed at least 3 forest spirits",
                    value_required=3,
                    items_required=["forest_spirit_1", "forest_spirit_2", "forest_spirit_3"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.LOCATION_SEQUENCE,
                    description="Visit the three ancient groves in correct order during full moon",
                    locations_required=["Grove of Echoes", "Whispering Glade", "Moonlit Sanctuary"],
                    time_sensitive=True
                )
            ],
            discovery_hints=[
                "Forest spirits speak of their lost brother in hushed tones",
                "Ancient trees bear scars from a great banishment",
                "The moon reveals paths hidden from the sun"
            ],
            rewards={
                "experience": 1000,
                "items": ["Yaksha's Blessing Amulet", "Nature's Harmony Scroll"],
                "abilities": ["Speak with Ancient Trees", "Forest Sanctuary"],
                "karma": 25
            },
            unlocks_content=["yaksha_alliance", "ancient_grove_mysteries"],
            story_impact="Redemption of the yaksha restores balance to the ancient forests",
            world_changes=["Forest spirits become more friendly", "New grove areas accessible"],
            hidden_location="Hidden Grove of Sorrow",
            access_method="Only accessible during quest progression",
            creation_lore="The yaksha was banished for trying to prevent deforestation centuries ago"
        )
        
        # Secret Area: Underwater Palace of the Naga King
        content["naga_underwater_palace"] = HiddenContent(
            content_id="naga_underwater_palace",
            name="Sunken Palace of Vasuki",
            description="The magnificent underwater palace of the Naga King, hidden beneath sacred lake",
            secret_type=SecretType.SECRET_AREA,
            rarity=SecretRarity.LEGENDARY,
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.ITEM_COMBINATION,
                    description="Combine the three sacred pearls at the lake's center",
                    items_required=["Pearl of Depths", "Pearl of Currents", "Pearl of Wisdom"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.NPC_RELATIONSHIP,
                    description="Gain the trust of a Naga guardian",
                    npcs_required=["Naga_Guardian_Shesha"],
                    value_required=80  # Relationship level
                )
            ],
            discovery_hints=[
                "Local fishermen speak of treasures beneath the sacred lake",
                "Naga scales found on the shoreline after storms",
                "Ancient carvings show serpent kings beneath the waters"
            ],
            false_leads=[
                "Many smaller lakes contain minor Naga dwellings",
                "Fake pearls are sometimes found that look similar"
            ],
            rewards={
                "area_access": "Underwater exploration area",
                "unique_beasts": ["Royal Naga", "Pearl Dragons", "Wisdom Serpents"],
                "treasures": ["Naga King's Crown", "Serpent Scale Armor", "Trident of Depths"],
                "knowledge": ["Ancient Naga History", "Underwater Architecture", "Serpent Magic"]
            },
            unlocks_content=["naga_political_questline", "underwater_exploration_skill"],
            world_changes=["Naga become potential allies", "Underwater travel unlocked"],
            access_method="Dive with special breathing charm at exact lake center"
        )
        
        # Forbidden Knowledge: The Rakshasa Transformation Ritual
        content["rakshasa_transformation"] = HiddenContent(
            content_id="rakshasa_transformation",
            name="The Forbidden Shapeshifter's Art",
            description="Ancient knowledge of how to permanently gain Rakshasa shapeshifting powers",
            secret_type=SecretType.FORBIDDEN_KNOWLEDGE,
            rarity=SecretRarity.MYTHICAL,
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.CORRUPTION_LEVEL,
                    description="Must have significant corruption but retain sanity",
                    value_required=50  # Corruption level 50+
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.CHOICE_CONSEQUENCE,
                    description="Must have made at least 3 morally ambiguous choices",
                    choices_required=["betrayed_ally", "used_forbidden_power", "sacrificed_innocent"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.SKILL_MASTERY,
                    description="Master level in deception and stealth",
                    value_required=80
                )
            ],
            discovery_hints=[
                "Whispers in the shadows speak of transformation beyond death",
                "Ancient Rakshasa texts hidden in forbidden libraries",
                "Those who walk the dark path sometimes find more than they sought"
            ],
            rewards={
                "permanent_abilities": ["Perfect Shapeshifting", "Demon Form", "Fear Aura"],
                "hidden_class_unlock": "Rakshasa Lord",
                "stat_changes": {"charisma": 20, "deception": 30, "corruption_resistance": 50}
            },
            unlocks_content=["demon_realm_access", "rakshasa_hierarchy_quests"],
            story_impact="Player becomes a being of legend, feared and powerful",
            world_changes=["NPCs react with fear or awe", "New demon-related content unlocks"],
            max_discoverers=1,  # Only one player per server can unlock this
            access_method="Found in personal nightmare realm during dark meditation"
        )
        
        # Secret Beast: The Phoenix of Rebirth
        content["phoenix_rebirth"] = HiddenContent(
            content_id="phoenix_rebirth",
            name="Garuda's Lost Cousin - The Eternal Phoenix",
            description="A legendary phoenix that died but can be reborn through a complex ritual",
            secret_type=SecretType.SECRET_BEAST,
            rarity=SecretRarity.LEGENDARY,
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.DIVINE_FAVOR,
                    description="Must have high favor with fire-related deities",
                    value_required=75,
                    npcs_required=["Agni_Fire_God"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.ITEM_COMBINATION,
                    description="Perform the Phoenix Rebirth Ritual",
                    items_required=["Phoenix Ashes", "Eternal Flame", "Tears of Joy", "Sacrificial Gold"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.TIME_CONDITION,
                    description="Must be performed during a solar eclipse",
                    time_sensitive=True
                )
            ],
            prerequisite_secrets=["discover_phoenix_legend", "find_ancient_pyre"],
            discovery_hints=[
                "Ancient texts speak of a bird that died protecting a village",
                "Firebirds in the area seem to gather at a particular mountain peak",
                "Local legends tell of a creature that sacrificed itself for mortals"
            ],
            rewards={
                "unique_beast": "Eternal Phoenix",
                "beast_abilities": ["Resurrection", "Healing Fire", "Immortal Flight"],
                "titles": ["Phoenix Friend", "Bringer of Rebirth"]
            },
            unlocks_content=["phoenix_evolution_quests", "fire_realm_access"],
            access_method="Perform ritual at the Sacred Pyre during solar eclipse"
        )
        
        # Hidden Class: Beast Sage
        content["beast_sage_class"] = HiddenContent(
            content_id="beast_sage_class",
            name="The Path of the Beast Sage",
            description="A legendary class that combines deep beast knowledge with divine wisdom",
            secret_type=SecretType.HIDDEN_CLASS,
            rarity=SecretRarity.EPIC,
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.BEAST_COLLECTION,
                    description="Must have tamed at least one beast from each major category",
                    value_required=8  # Number of categories
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.SKILL_MASTERY,
                    description="Master level in beast knowledge and wisdom",
                    value_required=75
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.NPC_RELATIONSHIP,
                    description="Recognized as a master by all three beast NPCs",
                    npcs_required=["Arunima", "Devraj", "Rukmini"],
                    value_required=90
                )
            ],
            discovery_hints=[
                "The wisest beast tamers speak of a higher calling",
                "Ancient tablets describe those who became one with all creatures",
                "Masters hint at a path beyond simple taming"
            ],
            rewards={
                "class_unlock": "Beast Sage",
                "unique_abilities": ["Universal Beast Speech", "Beast Evolution Guidance", "Harmony Aura"],
                "stat_bonuses": {"wisdom": 25, "beast_affinity": 50, "nature_connection": 30}
            },
            unlocks_content=["sage_council_access", "legendary_beast_quests"],
            story_impact="Player becomes a bridge between human and beast worlds"
        )
        
        return content
    
    def _initialize_secret_routes(self) -> Dict[str, SecretRoute]:
        """Initialize secret routes and hidden paths"""
        routes = {}
        
        # The Serpent's Path - Underground route through Naga territory
        routes["serpents_path"] = SecretRoute(
            route_id="serpents_path",
            name="The Serpent's Tunnel",
            description="Ancient underground passage used by Naga for secret travel",
            start_location="Sacred Lake Shore",
            end_location="Mountain Temple",
            waypoints=["Underground Cavern", "Naga Shrine", "Crystal Chambers"],
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.NPC_RELATIONSHIP,
                    description="Must be trusted by Naga guardians",
                    npcs_required=["Naga_Guardian"],
                    value_required=60
                )
            ],
            travel_time_reduction=0.7,  # 30% faster
            special_encounters=["Friendly Naga", "Underground Spirits", "Crystal Golems"],
            hidden_resources=["Underground Herbs", "Crystal Formations", "Sacred Water"],
            hazards=["Flooding tunnels", "Territorial Naga", "Crystal maze"],
            historical_significance="Built by ancient Naga civilization for secret diplomacy",
            route_lore="The path remembers those who travel it with respect"
        )
        
        # Sky Bridge - Aerial route for flying mounts
        routes["sky_bridge"] = SecretRoute(
            route_id="sky_bridge",
            name="The Garuda's Highway",
            description="Invisible wind currents that allow rapid aerial travel",
            start_location="Eagle's Peak",
            end_location="Cloud Temple",
            waypoints=["Wind Shrine", "Storm's Eye", "Thunder Roost"],
            unlock_requirements=[
                UnlockRequirement(
                    condition_type=UnlockCondition.BEAST_COLLECTION,
                    description="Must have bonded with a flying mount",
                    items_required=["flying_mount"]
                ),
                UnlockRequirement(
                    condition_type=UnlockCondition.SKILL_MASTERY,
                    description="Master aerial navigation",
                    value_required=50
                )
            ],
            travel_time_reduction=0.3,  # 70% faster
            special_encounters=["Sky Spirits", "Cloud Dragons", "Wind Elementals"],
            guardians=["Storm Eagles", "Thunder Birds"],
            historical_significance="Created by Garuda for divine messengers"
        )
        
        return routes
    
    def check_secret_unlock(self, player_id: str, secret_id: str, 
                           player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if a player can unlock a secret"""
        if secret_id not in self.hidden_content:
            return {"can_unlock": False, "reason": "Secret not found"}
        
        secret = self.hidden_content[secret_id]
        
        # Check if already discovered
        if player_id in self.player_progress:
            if secret_id in self.player_progress[player_id].discovered_secrets:
                return {"can_unlock": False, "reason": "Already discovered"}
        
        # Check max discoverers limit
        if secret.max_discoverers and secret.current_discoverers >= secret.max_discoverers:
            return {"can_unlock": False, "reason": "Discovery limit reached"}
        
        # Check prerequisites
        missing_requirements = []
        for requirement in secret.unlock_requirements:
            if not self._check_requirement(requirement, player_data):
                missing_requirements.append(requirement.description)
        
        if missing_requirements:
            return {
                "can_unlock": False,
                "reason": "Requirements not met",
                "missing": missing_requirements
            }
        
        # Check prerequisite secrets
        if player_id in self.player_progress:
            progress = self.player_progress[player_id]
            missing_secrets = []
            for prereq_secret in secret.prerequisite_secrets:
                if prereq_secret not in progress.discovered_secrets:
                    missing_secrets.append(prereq_secret)
            
            if missing_secrets:
                return {
                    "can_unlock": False,
                    "reason": "Prerequisite secrets required",
                    "missing_secrets": missing_secrets
                }
        
        return {"can_unlock": True}
    
    def _check_requirement(self, requirement: UnlockRequirement, 
                          player_data: Dict[str, Any]) -> bool:
        """Check if a specific requirement is met"""
        if requirement.condition_type == UnlockCondition.KARMA_THRESHOLD:
            return player_data.get("karma", 0) >= requirement.value_required
        
        elif requirement.condition_type == UnlockCondition.BEAST_COLLECTION:
            tamed_beasts = player_data.get("tamed_beasts", [])
            return len(tamed_beasts) >= requirement.value_required
        
        elif requirement.condition_type == UnlockCondition.ITEM_COMBINATION:
            inventory = player_data.get("inventory", [])
            return all(item in inventory for item in requirement.items_required)
        
        elif requirement.condition_type == UnlockCondition.SKILL_MASTERY:
            # Would check specific skill levels
            return player_data.get("max_skill_level", 0) >= requirement.value_required
        
        elif requirement.condition_type == UnlockCondition.CORRUPTION_LEVEL:
            return player_data.get("corruption", 0) >= requirement.value_required
        
        # Simplified checks for other conditions
        return True
    
    def unlock_secret(self, player_id: str, secret_id: str, 
                     player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to unlock a secret for a player"""
        unlock_check = self.check_secret_unlock(player_id, secret_id, player_data)
        
        if not unlock_check["can_unlock"]:
            return {"success": False, "reason": unlock_check["reason"]}
        
        secret = self.hidden_content[secret_id]
        
        # Initialize player progress if needed
        if player_id not in self.player_progress:
            self.player_progress[player_id] = PlayerSecretProgress(player_id)
        
        progress = self.player_progress[player_id]
        
        # Unlock the secret
        progress.discovered_secrets.add(secret_id)
        secret.current_discoverers += 1
        self.world_secrets_discovered.add(secret_id)
        
        # Award reputation
        rarity_bonus = {
            SecretRarity.UNCOMMON: 1,
            SecretRarity.RARE: 3,
            SecretRarity.EPIC: 5,
            SecretRarity.LEGENDARY: 10,
            SecretRarity.MYTHICAL: 20
        }
        progress.secret_finder_level += rarity_bonus.get(secret.rarity, 1)
        
        if secret.rarity in [SecretRarity.LEGENDARY, SecretRarity.MYTHICAL]:
            progress.legendary_discoveries += 1
        
        # Process unlocked content
        newly_unlocked = []
        for content_id in secret.unlocks_content:
            if content_id in self.hidden_content:
                unlock_check = self.check_secret_unlock(player_id, content_id, player_data)
                if unlock_check["can_unlock"]:
                    newly_unlocked.append(content_id)
        
        return {
            "success": True,
            "secret_unlocked": secret.name,
            "rarity": secret.rarity.value,
            "rewards": secret.rewards,
            "story_impact": secret.story_impact,
            "world_changes": secret.world_changes,
            "newly_unlocked_content": newly_unlocked,
            "reputation_gained": rarity_bonus.get(secret.rarity, 1)
        }
    
    def get_available_clues(self, player_id: str, location: str, 
                           player_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get clues available to the player at their current location"""
        clues = []
        
        for secret_id, secret in self.hidden_content.items():
            # Skip already discovered secrets
            if (player_id in self.player_progress and 
                secret_id in self.player_progress[player_id].discovered_secrets):
                continue
            
            # Check if player meets some but not all requirements
            requirements_met = 0
            total_requirements = len(secret.unlock_requirements)
            
            for requirement in secret.unlock_requirements:
                if self._check_requirement(requirement, player_data):
                    requirements_met += 1
            
            # Give hints if player is making progress
            if requirements_met > 0 and requirements_met < total_requirements:
                hint_level = requirements_met / total_requirements
                
                if hint_level >= 0.5:  # More than half requirements met
                    clue_text = random.choice(secret.discovery_hints)
                    clues.append({
                        "type": "discovery_hint",
                        "text": clue_text,
                        "secret_name": secret.name,
                        "progress": f"{requirements_met}/{total_requirements} requirements met"
                    })
                elif hint_level >= 0.25:  # Quarter requirements met
                    clue_text = f"You sense something mysterious about {location}..."
                    clues.append({
                        "type": "vague_hint",
                        "text": clue_text,
                        "progress": "Some progress made"
                    })
        
        # Add false leads occasionally
        if random.random() < 0.2:  # 20% chance
            false_leads = [
                "You notice strange markings, but they lead nowhere...",
                "Local rumors speak of treasures, but seem exaggerated...",
                "An old map shows something here, but it appears outdated..."
            ]
            clues.append({
                "type": "false_lead",
                "text": random.choice(false_leads)
            })
        
        return clues
    
    def get_player_secret_status(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive secret discovery status for a player"""
        if player_id not in self.player_progress:
            return {
                "secrets_discovered": 0,
                "reputation_level": 0,
                "legendary_discoveries": 0
            }
        
        progress = self.player_progress[player_id]
        
        # Calculate discovery rates by rarity
        rarity_counts = {}
        for secret_id in progress.discovered_secrets:
            if secret_id in self.hidden_content:
                rarity = self.hidden_content[secret_id].rarity
                rarity_counts[rarity.value] = rarity_counts.get(rarity.value, 0) + 1
        
        return {
            "total_secrets_discovered": len(progress.discovered_secrets),
            "secrets_by_rarity": rarity_counts,
            "secret_finder_reputation": progress.secret_finder_level,
            "legendary_discoveries": progress.legendary_discoveries,
            "active_investigations": len(progress.active_investigations),
            "routes_unlocked": len(progress.unlocked_routes),
            "major_choices_made": len(progress.major_choices_made),
            "world_impact": len([s for s in progress.discovered_secrets 
                               if self.hidden_content[s].world_changes])
        }


# Global hidden content system
hidden_content_system = HiddenContentSystem()


def test_hidden_content_system():
    """Test the hidden content system"""
    print("🔍 Testing Hidden Content and Secret Quest System")
    print("=" * 60)
    
    # Test player data
    test_player_data = {
        "level": 25,
        "karma": 40,
        "tamed_beasts": ["forest_spirit_1", "forest_spirit_2", "forest_spirit_3"],
        "inventory": ["Pearl of Depths", "Pearl of Currents"],
        "corruption": 30,
        "max_skill_level": 60
    }
    
    print("🎯 Checking secrets available to player...")
    
    # Check Lost Yaksha quest
    print("\n📜 Checking Lost Yaksha Quest:")
    yaksha_check = hidden_content_system.check_secret_unlock(
        "test_player", "lost_yaksha_quest", test_player_data
    )
    print(f"   Can unlock: {'✅' if yaksha_check['can_unlock'] else '❌'}")
    if not yaksha_check["can_unlock"]:
        print(f"   Reason: {yaksha_check['reason']}")
        if "missing" in yaksha_check:
            print(f"   Missing: {yaksha_check['missing']}")
    
    # Check Naga Palace
    print("\n🏰 Checking Naga Underwater Palace:")
    naga_check = hidden_content_system.check_secret_unlock(
        "test_player", "naga_underwater_palace", test_player_data
    )
    print(f"   Can unlock: {'✅' if naga_check['can_unlock'] else '❌'}")
    if not naga_check["can_unlock"]:
        print(f"   Reason: {naga_check['reason']}")
    
    # Try to unlock a secret
    print("\n🔓 Attempting to unlock Lost Yaksha quest...")
    unlock_result = hidden_content_system.unlock_secret(
        "test_player", "lost_yaksha_quest", test_player_data
    )
    
    if unlock_result["success"]:
        print(f"✅ Successfully unlocked: {unlock_result['secret_unlocked']}")
        print(f"   Rarity: {unlock_result['rarity']}")
        print(f"   Story Impact: {unlock_result['story_impact']}")
        print(f"   Rewards: {unlock_result['rewards']}")
    else:
        print(f"❌ Failed to unlock: {unlock_result['reason']}")
    
    # Get available clues
    print("\n🕵️ Getting clues at current location...")
    clues = hidden_content_system.get_available_clues(
        "test_player", "Forest Clearing", test_player_data
    )
    
    for i, clue in enumerate(clues):
        print(f"   Clue {i+1} ({clue['type']}): {clue['text']}")
    
    # Show final status
    print("\n📊 Final Secret Discovery Status:")
    status = hidden_content_system.get_player_secret_status("test_player")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Hidden content system test completed!")


if __name__ == "__main__":
    test_hidden_content_system()