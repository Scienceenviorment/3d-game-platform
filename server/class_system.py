#!/usr/bin/env python3
"""
Job Classes and Profession System
Based on "Beast Taming: Classic of Mountains and Seas"
Includes specialized roles, progression paths, and unique abilities
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum


class JobClass(Enum):
    """Primary job classes available to players"""
    # Combat Classes
    BEAST_WARRIOR = "beast_warrior"         # Fights alongside tamed beasts
    DIVINE_PALADIN = "divine_paladin"       # Holy warrior blessed by gods
    SHADOW_ASSASSIN = "shadow_assassin"     # Stealth and dark arts
    ELEMENTAL_MAGE = "elemental_mage"       # Controls natural elements
    
    # Support Classes
    BEAST_TAMER = "beast_tamer"             # Specializes in taming creatures
    DIVINE_HEALER = "divine_healer"         # Healing and restoration
    SPIRIT_SHAMAN = "spirit_shaman"         # Communicates with spirits
    NATURE_DRUID = "nature_druid"           # Nature magic and transformation
    
    # Crafting Classes
    MASTER_ALCHEMIST = "master_alchemist"   # Advanced potion and transmutation
    DIVINE_SMITH = "divine_smith"           # Forges legendary weapons
    SAGE_SCHOLAR = "sage_scholar"           # Ancient knowledge and research
    MERCHANT_PRINCE = "merchant_prince"     # Trade and economics
    
    # Unique Classes
    FORBIDDEN_CULTIST = "forbidden_cultist" # Dangerous dark powers
    CELESTIAL_MONK = "celestial_monk"       # Martial arts and enlightenment
    BEAST_WHISPERER = "beast_whisperer"     # Deep beast communication
    RUNE_MASTER = "rune_master"             # Ancient symbols and magic


class Profession(Enum):
    """Secondary professions that complement job classes"""
    # Production
    HERBALIST = "herbalist"
    MINER = "miner"
    LUMBERJACK = "lumberjack"
    FARMER = "farmer"
    FISHERMAN = "fisherman"
    
    # Crafting
    BLACKSMITH = "blacksmith"
    TAILOR = "tailor"
    JEWELER = "jeweler"
    ENCHANTER = "enchanter"
    COOK = "cook"
    
    # Knowledge
    ARCHAEOLOGIST = "archaeologist"
    CARTOGRAPHER = "cartographer"
    LINGUIST = "linguist"
    BEAST_RESEARCHER = "beast_researcher"
    
    # Service
    GUIDE = "guide"
    TRADER = "trader"
    DIPLOMAT = "diplomat"
    SPY = "spy"


class AbilityType(Enum):
    """Types of abilities classes can learn"""
    PASSIVE = "passive"         # Always active
    ACTIVE = "active"           # Must be activated
    COMBAT = "combat"           # Used in battle
    UTILITY = "utility"         # Non-combat uses
    SOCIAL = "social"           # Interaction with NPCs
    CRAFTING = "crafting"       # Enhance crafting abilities
    BEAST = "beast"             # Related to beast taming


@dataclass
class ClassAbility:
    """An ability that job classes can learn"""
    ability_id: str
    name: str
    description: str
    ability_type: AbilityType
    
    # Learning requirements
    class_required: JobClass
    level_required: int
    prerequisite_abilities: List[str] = field(default_factory=list)
    
    # Costs and limitations
    mana_cost: int = 0
    stamina_cost: int = 0
    cooldown_seconds: int = 0
    uses_per_day: Optional[int] = None
    
    # Effects
    effects: List[str] = field(default_factory=list)
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    special_properties: List[str] = field(default_factory=list)
    
    # Mastery progression
    mastery_levels: int = 5
    mastery_bonuses: Dict[int, str] = field(default_factory=dict)  # level: bonus description
    
    # Unlocking method
    unlock_method: str = "Level Up"
    hidden_ability: bool = False


@dataclass
class JobProgression:
    """Progression path for a job class"""
    job_class: JobClass
    level: int = 1
    experience: int = 0
    
    # Abilities
    learned_abilities: List[str] = field(default_factory=list)
    ability_mastery: Dict[str, int] = field(default_factory=dict)  # ability_id: mastery_level
    
    # Specialization paths
    available_specializations: List[str] = field(default_factory=list)
    chosen_specialization: Optional[str] = None
    specialization_progress: int = 0
    
    # Class-specific resources
    class_resources: Dict[str, int] = field(default_factory=dict)
    
    # Achievements and titles
    class_achievements: List[str] = field(default_factory=list)
    earned_titles: List[str] = field(default_factory=list)


@dataclass
class ProfessionProgress:
    """Progress in a profession"""
    profession: Profession
    level: int = 1
    experience: int = 0
    
    # Profession benefits
    efficiency_bonuses: Dict[str, float] = field(default_factory=dict)
    resource_bonuses: Dict[str, float] = field(default_factory=dict)
    special_recipes: List[str] = field(default_factory=list)
    
    # Professional network
    known_contacts: List[str] = field(default_factory=list)  # NPC IDs
    reputation: int = 0  # 0-100
    
    # Tools and equipment
    professional_tools: List[str] = field(default_factory=list)
    workshop_level: int = 0


@dataclass
class PlayerClassProfile:
    """Complete class and profession profile for a player"""
    player_id: str
    
    # Primary job class
    primary_class: Optional[JobClass] = None
    class_progression: Optional[JobProgression] = None
    
    # Secondary class (unlocked later)
    secondary_class: Optional[JobClass] = None
    secondary_progression: Optional[JobProgression] = None
    
    # Professions (up to 2 active)
    active_professions: List[ProfessionProgress] = field(default_factory=list)
    
    # Overall stats
    total_class_level: int = 1
    skill_points_available: int = 0
    talent_points_available: int = 0
    
    # Class synergies
    class_synergy_bonuses: Dict[str, float] = field(default_factory=dict)
    
    # Special unlocks
    unlocked_hidden_classes: List[JobClass] = field(default_factory=list)
    unlocked_prestige_abilities: List[str] = field(default_factory=list)


class ClassSystem:
    """Manages job classes and profession system"""
    
    def __init__(self):
        self.class_abilities = self._initialize_abilities()
        self.class_paths = self._initialize_class_paths()
        self.profession_benefits = self._initialize_profession_benefits()
        self.player_profiles = {}
    
    def _initialize_abilities(self) -> Dict[str, ClassAbility]:
        """Initialize all class abilities"""
        abilities = {}
        
        # Beast Warrior Abilities
        abilities["beast_bond"] = ClassAbility(
            ability_id="beast_bond",
            name="Primal Beast Bond",
            description="Form a deeper connection with your beast companion",
            ability_type=AbilityType.PASSIVE,
            class_required=JobClass.BEAST_WARRIOR,
            level_required=1,
            effects=["Beast gains +20% health", "Share 50% of damage taken"],
            stat_bonuses={"beast_loyalty": 25},
            special_properties=["telepathic_communication", "shared_senses"],
            mastery_bonuses={
                1: "Beast gains +5% damage",
                3: "Share healing effects",
                5: "Beast can use one of your abilities"
            }
        )
        
        abilities["beast_charge"] = ClassAbility(
            ability_id="beast_charge",
            name="Coordinated Charge",
            description="You and your beast charge together for devastating damage",
            ability_type=AbilityType.COMBAT,
            class_required=JobClass.BEAST_WARRIOR,
            level_required=5,
            prerequisite_abilities=["beast_bond"],
            stamina_cost=30,
            cooldown_seconds=60,
            effects=["Combined charge attack", "Knockdown enemies", "Extra damage based on beast size"],
            mastery_bonuses={
                1: "Reduced cooldown",
                3: "Area damage on impact",
                5: "Can charge through enemies"
            }
        )
        
        # Divine Paladin Abilities
        abilities["divine_protection"] = ClassAbility(
            ability_id="divine_protection",
            name="Blessing of the Gods",
            description="Call upon divine protection for yourself and allies",
            ability_type=AbilityType.ACTIVE,
            class_required=JobClass.DIVINE_PALADIN,
            level_required=1,
            mana_cost=40,
            cooldown_seconds=300,
            effects=["Damage reduction 50%", "Immunity to fear/charm", "Party-wide blessing"],
            stat_bonuses={"divine_favor": 10},
            mastery_bonuses={
                1: "Longer duration",
                3: "Reflects damage to attackers",
                5: "Heals party over time"
            }
        )
        
        # Beast Tamer Abilities
        abilities["taming_mastery"] = ClassAbility(
            ability_id="taming_mastery",
            name="Master Beast Tamer",
            description="Extraordinary skill in communicating with and taming beasts",
            ability_type=AbilityType.PASSIVE,
            class_required=JobClass.BEAST_TAMER,
            level_required=1,
            effects=["50% faster taming", "Can tame higher level beasts", "Multiple beast slots"],
            special_properties=["beast_empathy", "danger_sense"],
            mastery_bonuses={
                1: "Can sense beast emotions",
                3: "Tame beasts without items sometimes",
                5: "Can tame legendary creatures"
            }
        )
        
        abilities["beast_whispering"] = ClassAbility(
            ability_id="beast_whispering",
            name="Voice of the Wild",
            description="Speak with any creature, gaining information and aid",
            ability_type=AbilityType.UTILITY,
            class_required=JobClass.BEAST_TAMER,
            level_required=10,
            prerequisite_abilities=["taming_mastery"],
            mana_cost=20,
            effects=["Communicate with any animal", "Learn about area dangers", "Request simple favors"],
            mastery_bonuses={
                1: "Speak with magical beasts",
                3: "Animals will warn of danger",
                5: "Can call wild animals for help"
            }
        )
        
        # Forbidden Cultist Abilities (Hidden/Dangerous)
        abilities["dark_pact"] = ClassAbility(
            ability_id="dark_pact",
            name="Pact with Shadows",
            description="Make a dangerous pact with dark entities for power",
            ability_type=AbilityType.PASSIVE,
            class_required=JobClass.FORBIDDEN_CULTIST,
            level_required=1,
            effects=["Gain shadow powers", "Increased damage at night", "Can see in darkness"],
            special_properties=["corruption_immunity", "fear_aura"],
            unlock_method="Dark Ritual",
            hidden_ability=True,
            mastery_bonuses={
                1: "Shadow minions",
                3: "Phase through walls briefly",
                5: "Transform into shadow form"
            }
        )
        
        # Sage Scholar Abilities
        abilities["ancient_knowledge"] = ClassAbility(
            ability_id="ancient_knowledge",
            name="Scholar of Ages",
            description="Deep knowledge of history, languages, and lore",
            ability_type=AbilityType.PASSIVE,
            class_required=JobClass.SAGE_SCHOLAR,
            level_required=1,
            effects=["Identify ancient items", "Read any language", "Know beast weaknesses"],
            stat_bonuses={"intelligence": 15, "wisdom": 15},
            special_properties=["perfect_memory", "pattern_recognition"],
            mastery_bonuses={
                1: "Predict weather and events",
                3: "Sense magical auras",
                5: "See brief glimpses of future"
            }
        )
        
        return abilities
    
    def _initialize_class_paths(self) -> Dict[JobClass, Dict[str, Any]]:
        """Initialize class progression paths and specializations"""
        paths = {}
        
        # Beast Warrior Path
        paths[JobClass.BEAST_WARRIOR] = {
            "description": "Masters of combat alongside beast companions",
            "primary_stats": ["strength", "constitution", "beast_affinity"],
            "specializations": {
                "alpha_pack_leader": "Lead multiple beasts in combat",
                "draconic_rider": "Specialize in dragon and flying mount bonds",
                "primal_berserker": "Merge temporarily with beast for power"
            },
            "prestige_unlock": "Tame a legendary beast and reach level 50",
            "unique_resources": ["beast_loyalty", "pack_unity"]
        }
        
        # Divine Paladin Path
        paths[JobClass.DIVINE_PALADIN] = {
            "description": "Holy warriors blessed by divine forces",
            "primary_stats": ["strength", "wisdom", "divine_favor"],
            "specializations": {
                "temple_guardian": "Protect sacred places and artifacts",
                "divine_judge": "Smite evil and enforce divine justice",
                "light_bringer": "Heal and purify corruption"
            },
            "prestige_unlock": "Complete a divine trial and maintain good karma",
            "unique_resources": ["divine_favor", "holy_power"]
        }
        
        # Beast Tamer Path
        paths[JobClass.BEAST_TAMER] = {
            "description": "Specialists in understanding and bonding with creatures",
            "primary_stats": ["charisma", "wisdom", "beast_empathy"],
            "specializations": {
                "legendary_tamer": "Focus on mythical and divine beasts",
                "swarm_master": "Control many smaller creatures",
                "beast_researcher": "Study and catalog creature abilities"
            },
            "prestige_unlock": "Tame beasts from all major categories",
            "unique_resources": ["beast_trust", "wild_reputation"]
        }
        
        # Forbidden Cultist Path (Hidden)
        paths[JobClass.FORBIDDEN_CULTIST] = {
            "description": "Wielders of dangerous dark powers",
            "primary_stats": ["intelligence", "charisma", "corruption"],
            "specializations": {
                "shadow_lord": "Master of darkness and stealth",
                "demon_binder": "Summon and control dark entities",
                "corruption_spreader": "Infect others with dark power"
            },
            "prestige_unlock": "Embrace complete corruption while retaining sanity",
            "unique_resources": ["dark_energy", "corruption_resistance"],
            "hidden_class": True
        }
        
        return paths
    
    def _initialize_profession_benefits(self) -> Dict[Profession, Dict[str, Any]]:
        """Initialize profession benefits and progression"""
        benefits = {}
        
        benefits[Profession.HERBALIST] = {
            "level_benefits": {
                1: {"gather_speed": 1.2, "herb_yield": 1.1},
                5: {"rare_herb_chance": 0.1, "herb_quality": 1.2},
                10: {"magical_herb_detection": True, "preservation_bonus": 1.5},
                15: {"herb_mutation_chance": 0.05, "legendary_herb_access": True}
            },
            "special_recipes": ["herbal_remedies", "growth_accelerators", "beast_attraction_potions"],
            "unique_tools": ["master_gathering_kit", "herb_preservation_box", "growth_analysis_lens"]
        }
        
        benefits[Profession.BEAST_RESEARCHER] = {
            "level_benefits": {
                1: {"beast_info_bonus": 1.5, "tracking_efficiency": 1.2},
                5: {"weakness_detection": True, "behavior_prediction": 1.3},
                10: {"beast_communication_bonus": 2.0, "rare_beast_locations": True},
                15: {"legendary_beast_knowledge": True, "perfect_beast_analysis": True}
            },
            "special_abilities": ["beast_encyclopedia", "behavior_analysis", "evolution_prediction"],
            "research_projects": ["beast_catalog", "taming_guide", "evolution_study"]
        }
        
        benefits[Profession.BLACKSMITH] = {
            "level_benefits": {
                1: {"crafting_speed": 1.2, "material_efficiency": 1.1},
                5: {"quality_bonus": 1.3, "rare_material_chance": 0.1},
                10: {"masterwork_chance": 0.2, "enchantment_compatibility": 1.5},
                15: {"legendary_crafting": True, "material_transmutation": True}
            },
            "signature_items": ["beast_armor", "divine_weapons", "elemental_tools"],
            "workshop_upgrades": ["divine_forge", "elemental_anvil", "master_quenching_pool"]
        }
        
        return benefits
    
    def choose_class(self, player_id: str, job_class: JobClass) -> Dict[str, Any]:
        """Player chooses their primary job class"""
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerClassProfile(player_id)
        
        profile = self.player_profiles[player_id]
        
        # Check if this is a hidden class that requires special unlock
        if job_class in self.class_paths and self.class_paths[job_class].get("hidden_class"):
            if job_class not in profile.unlocked_hidden_classes:
                return {"success": False, "reason": "Hidden class not unlocked"}
        
        # Set primary class
        profile.primary_class = job_class
        profile.class_progression = JobProgression(job_class)
        
        # Award starting abilities
        starting_abilities = self._get_starting_abilities(job_class)
        profile.class_progression.learned_abilities.extend(starting_abilities)
        
        # Set class resources
        class_info = self.class_paths.get(job_class, {})
        for resource in class_info.get("unique_resources", []):
            profile.class_progression.class_resources[resource] = 100
        
        return {
            "success": True,
            "class_chosen": job_class.value,
            "starting_abilities": starting_abilities,
            "specializations_available": list(class_info.get("specializations", {}).keys()),
            "primary_stats": class_info.get("primary_stats", [])
        }
    
    def learn_ability(self, player_id: str, ability_id: str) -> Dict[str, Any]:
        """Player attempts to learn a new ability"""
        if player_id not in self.player_profiles:
            return {"success": False, "reason": "No class profile found"}
        
        if ability_id not in self.class_abilities:
            return {"success": False, "reason": "Ability not found"}
        
        profile = self.player_profiles[player_id]
        ability = self.class_abilities[ability_id]
        
        # Check if player has the required class
        if (profile.primary_class != ability.class_required and 
            profile.secondary_class != ability.class_required):
            return {"success": False, "reason": f"Requires {ability.class_required.value} class"}
        
        # Get appropriate progression
        if profile.primary_class == ability.class_required:
            progression = profile.class_progression
        else:
            progression = profile.secondary_progression
        
        # Check level requirement
        if progression.level < ability.level_required:
            return {
                "success": False, 
                "reason": f"Requires class level {ability.level_required}"
            }
        
        # Check prerequisites
        for prereq in ability.prerequisite_abilities:
            if prereq not in progression.learned_abilities:
                return {"success": False, "reason": f"Missing prerequisite: {prereq}"}
        
        # Learn the ability
        progression.learned_abilities.append(ability_id)
        progression.ability_mastery[ability_id] = 1
        
        return {
            "success": True,
            "ability_learned": ability.name,
            "effects": ability.effects,
            "mastery_path": ability.mastery_bonuses
        }
    
    def _get_starting_abilities(self, job_class: JobClass) -> List[str]:
        """Get starting abilities for a class"""
        starting = []
        for ability_id, ability in self.class_abilities.items():
            if (ability.class_required == job_class and 
                ability.level_required == 1 and 
                not ability.prerequisite_abilities):
                starting.append(ability_id)
        return starting
    
    def add_profession(self, player_id: str, profession: Profession) -> Dict[str, Any]:
        """Add a profession to the player"""
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerClassProfile(player_id)
        
        profile = self.player_profiles[player_id]
        
        # Check if player already has max professions (2)
        if len(profile.active_professions) >= 2:
            return {"success": False, "reason": "Maximum 2 professions allowed"}
        
        # Check if already has this profession
        for prof in profile.active_professions:
            if prof.profession == profession:
                return {"success": False, "reason": "Already have this profession"}
        
        # Add profession
        new_profession = ProfessionProgress(profession)
        profile.active_professions.append(new_profession)
        
        # Apply starting benefits
        benefits = self.profession_benefits.get(profession, {})
        level_1_benefits = benefits.get("level_benefits", {}).get(1, {})
        
        for benefit, value in level_1_benefits.items():
            new_profession.efficiency_bonuses[benefit] = value
        
        return {
            "success": True,
            "profession_added": profession.value,
            "starting_benefits": level_1_benefits,
            "special_recipes": benefits.get("special_recipes", [])
        }
    
    def get_available_specializations(self, player_id: str) -> Dict[str, Any]:
        """Get available specializations for the player's class"""
        if player_id not in self.player_profiles:
            return {"specializations": []}
        
        profile = self.player_profiles[player_id]
        
        if not profile.primary_class or not profile.class_progression:
            return {"specializations": []}
        
        # Check if player is high enough level for specialization
        if profile.class_progression.level < 10:
            return {"message": "Specialization available at level 10"}
        
        class_info = self.class_paths.get(profile.primary_class, {})
        specializations = class_info.get("specializations", {})
        
        return {
            "available_specializations": {
                name: description for name, description in specializations.items()
            },
            "current_specialization": profile.class_progression.chosen_specialization,
            "min_level_required": 10
        }
    
    def choose_specialization(self, player_id: str, specialization_name: str) -> Dict[str, Any]:
        """Choose a specialization path"""
        if player_id not in self.player_profiles:
            return {"success": False, "reason": "No class profile"}
        
        profile = self.player_profiles[player_id]
        progression = profile.class_progression
        
        if progression.level < 10:
            return {"success": False, "reason": "Must be level 10+"}
        
        if progression.chosen_specialization:
            return {"success": False, "reason": "Already chose specialization"}
        
        class_info = self.class_paths.get(profile.primary_class, {})
        available = class_info.get("specializations", {})
        
        if specialization_name not in available:
            return {"success": False, "reason": "Invalid specialization"}
        
        # Choose specialization
        progression.chosen_specialization = specialization_name
        progression.specialization_progress = 0
        
        # Unlock specialization abilities
        spec_abilities = self._get_specialization_abilities(specialization_name)
        
        return {
            "success": True,
            "specialization_chosen": specialization_name,
            "description": available[specialization_name],
            "unlocked_abilities": spec_abilities
        }
    
    def _get_specialization_abilities(self, specialization_name: str) -> List[str]:
        """Get abilities unlocked by specialization"""
        # This would return specialization-specific abilities
        return [f"{specialization_name}_mastery", f"{specialization_name}_ultimate"]
    
    def get_player_class_summary(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive class information for player"""
        if player_id not in self.player_profiles:
            return {"message": "No class information found"}
        
        profile = self.player_profiles[player_id]
        
        summary = {
            "primary_class": profile.primary_class.value if profile.primary_class else None,
            "class_level": profile.class_progression.level if profile.class_progression else 0,
            "learned_abilities": len(profile.class_progression.learned_abilities) if profile.class_progression else 0,
            "specialization": profile.class_progression.chosen_specialization if profile.class_progression else None,
            "active_professions": [p.profession.value for p in profile.active_professions],
            "total_profession_levels": sum(p.level for p in profile.active_professions),
            "hidden_classes_unlocked": [c.value for c in profile.unlocked_hidden_classes],
            "titles_earned": profile.class_progression.earned_titles if profile.class_progression else []
        }
        
        return summary


# Global class system instance
class_system = ClassSystem()


def test_class_system():
    """Test the job class and profession system"""
    print("⚔️ Testing Job Classes and Profession System")
    print("=" * 60)
    
    # Test choosing a class
    print("🎯 Choosing Beast Warrior class...")
    class_result = class_system.choose_class("test_player", JobClass.BEAST_WARRIOR)
    
    if class_result["success"]:
        print(f"✅ Class chosen: {class_result['class_chosen']}")
        print(f"   Starting abilities: {class_result['starting_abilities']}")
        print(f"   Available specializations: {class_result['specializations_available']}")
    
    # Test learning an ability
    print("\n🧠 Learning Beast Bond ability...")
    ability_result = class_system.learn_ability("test_player", "beast_bond")
    
    if ability_result["success"]:
        print(f"✅ Learned: {ability_result['ability_learned']}")
        print(f"   Effects: {ability_result['effects']}")
    
    # Test adding profession
    print("\n🔨 Adding Beast Researcher profession...")
    prof_result = class_system.add_profession("test_player", Profession.BEAST_RESEARCHER)
    
    if prof_result["success"]:
        print(f"✅ Profession added: {prof_result['profession_added']}")
        print(f"   Starting benefits: {prof_result['starting_benefits']}")
    
    # Show available specializations
    print("\n⭐ Available Specializations:")
    spec_info = class_system.get_available_specializations("test_player")
    if "available_specializations" in spec_info:
        for name, desc in spec_info["available_specializations"].items():
            print(f"   {name}: {desc}")
    else:
        print(f"   {spec_info['message']}")
    
    # Final summary
    print("\n📊 Final Class Summary:")
    summary = class_system.get_player_class_summary("test_player")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Class system test completed!")


if __name__ == "__main__":
    test_class_system()