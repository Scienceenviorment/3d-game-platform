#!/usr/bin/env python3
"""
Power System - Divine and Beast Powers with Costs
Based on "Beast Taming: Starting with the Classic of Mountains and Seas"
Powers come at a price - rituals, sacrifices, and consequences
"""

import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta


class PowerType(Enum):
    """Types of powers available to players"""
    DIVINE = "divine"           # Powers from gods
    BEAST = "beast"             # Powers from tamed beasts
    ELEMENTAL = "elemental"     # Control over elements
    SPIRITUAL = "spiritual"     # Soul and mind powers
    NATURE = "nature"           # Plant and animal communion
    ANCESTRAL = "ancestral"     # Powers from ancient bloodlines
    FORBIDDEN = "forbidden"     # Dangerous dark powers


class PowerSource(Enum):
    """Sources of power in the world"""
    # Indian Deities
    BRAHMA = "brahma"           # Creator god - creation powers
    VISHNU = "vishnu"           # Preserver god - protection powers
    SHIVA = "shiva"             # Destroyer god - transformation powers
    INDRA = "indra"             # Thunder god - lightning powers
    VARUNA = "varuna"           # Water god - ocean powers
    AGNI = "agni"               # Fire god - flame powers
    SURYA = "surya"             # Sun god - light powers
    CHANDRA = "chandra"         # Moon god - lunar powers
    
    # Mythical Beasts
    GARUDA_LORD = "garuda_lord"     # King of eagles - flight powers
    NAGA_KING = "naga_king"         # Serpent ruler - poison/wisdom
    HANUMAN = "hanuman"             # Monkey god - strength/devotion
    LAKSHMI = "lakshmi"             # Goddess - prosperity powers
    
    # Natural Forces
    FOREST_SPIRIT = "forest_spirit"
    MOUNTAIN_SOUL = "mountain_soul"
    RIVER_ESSENCE = "river_essence"
    STORM_HEART = "storm_heart"


@dataclass
class PowerCost:
    """The price that must be paid for power"""
    # Material costs
    required_items: List[str] = field(default_factory=list)
    gold_cost: int = 0
    experience_cost: int = 0
    
    # Spiritual costs
    karma_cost: int = 0          # Negative karma for forbidden powers
    life_force_cost: int = 0     # Permanent health reduction
    sanity_cost: int = 0         # Mental stability loss
    
    # Ritual requirements
    ritual_components: List[str] = field(default_factory=list)
    ritual_location: str = ""    # Specific location required
    ritual_time: str = ""        # Time of day/moon phase required
    witnesses_required: int = 0   # Number of NPCs needed
    
    # Ongoing costs
    daily_maintenance: Dict[str, int] = field(default_factory=dict)
    power_degradation_rate: float = 0.0  # How fast power fades without maintenance


@dataclass
class Power:
    """A divine or beast power that players can acquire"""
    power_id: str
    name: str
    description: str
    power_type: PowerType
    source: PowerSource
    level: int = 1              # Power level (1-10)
    max_level: int = 10
    
    # Power effects
    abilities: List[str] = field(default_factory=list)
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    special_effects: List[str] = field(default_factory=list)
    
    # Acquisition cost
    acquisition_cost: PowerCost = field(default_factory=PowerCost)
    
    # Upgrade costs (per level)
    upgrade_cost_multiplier: float = 1.5
    
    # Risks and side effects
    side_effects: List[str] = field(default_factory=list)
    corruption_risk: float = 0.0    # Chance of power corrupting the user
    
    # Lore and story
    origin_story: str = ""
    acquisition_method: str = ""    # How to obtain this power
    prerequisites: List[str] = field(default_factory=list)


@dataclass
class Ritual:
    """A ritual that must be performed to gain or maintain power"""
    ritual_id: str
    name: str
    description: str
    purpose: str                # What this ritual accomplishes
    
    # Requirements
    required_components: List[str] = field(default_factory=list)
    required_location: str = ""
    required_time: str = ""     # "dawn", "full_moon", "eclipse", etc.
    participant_count: int = 1  # How many people needed
    
    # Process
    duration_minutes: int = 30
    steps: List[str] = field(default_factory=list)
    difficulty: int = 1         # 1-10 complexity
    
    # Outcomes
    success_rate: float = 0.8   # Base success rate
    success_effects: List[str] = field(default_factory=list)
    failure_effects: List[str] = field(default_factory=list)
    
    # Costs and risks
    component_consumption: bool = True  # Are components used up?
    energy_cost: int = 20       # Player energy/stamina cost
    risk_level: int = 1         # How dangerous (1-10)


class PowerCorruption(Enum):
    """Types of corruption from forbidden powers"""
    MADNESS = "madness"         # Sanity loss
    PHYSICAL = "physical"       # Body transformation
    SPIRITUAL = "spiritual"     # Soul corruption
    SOCIAL = "social"           # NPCs fear/hate you
    ELEMENTAL = "elemental"     # Uncontrolled elemental effects


@dataclass
class PlayerPowerProfile:
    """Player's power progression and status"""
    player_id: str
    
    # Acquired powers
    active_powers: Dict[str, Power] = field(default_factory=dict)
    dormant_powers: Dict[str, Power] = field(default_factory=dict)  # Powers not currently usable
    
    # Power statistics
    total_power_level: int = 0
    divine_affinity: Dict[PowerSource, int] = field(default_factory=dict)
    corruption_level: int = 0   # 0-100, higher = more corrupted
    karma_balance: int = 0      # Positive = good karma, negative = bad
    
    # Power maintenance
    last_maintenance: Dict[str, datetime] = field(default_factory=dict)
    power_stability: Dict[str, float] = field(default_factory=dict)  # 0.0-1.0
    
    # Ritual history
    completed_rituals: List[str] = field(default_factory=list)
    failed_rituals: List[str] = field(default_factory=list)
    ritual_mastery: Dict[str, int] = field(default_factory=dict)  # How good at each ritual
    
    # Corruption effects
    active_corruptions: List[PowerCorruption] = field(default_factory=list)
    corruption_resistance: float = 1.0  # How well they resist corruption


class PowerSystem:
    """Manages the divine and beast power system"""
    
    def __init__(self):
        self.available_powers = self._initialize_powers()
        self.available_rituals = self._initialize_rituals()
        self.player_profiles = {}
    
    def _initialize_powers(self) -> Dict[str, Power]:
        """Initialize all available powers in the game"""
        powers = {}
        
        # Divine Powers - Shiva's Transformation
        powers["third_eye"] = Power(
            power_id="third_eye",
            name="Third Eye of Shiva",
            description="The divine eye that sees truth and can destroy illusions",
            power_type=PowerType.DIVINE,
            source=PowerSource.SHIVA,
            abilities=["See through illusions", "Detect hidden enemies", "Spiritual sight"],
            stat_bonuses={"wisdom": 15, "perception": 20},
            special_effects=["Can see invisible creatures", "Immune to mind control"],
            acquisition_cost=PowerCost(
                required_items=["Sacred Ash", "Rudraksha Beads", "Himalayan Crystal"],
                experience_cost=500,
                karma_cost=10,  # Good karma required
                ritual_components=["Sacred Fire", "Meditation Mat", "Incense"],
                ritual_location="Mountain Peak Temple",
                ritual_time="New Moon Night",
                witnesses_required=1,  # Need a guru
                daily_maintenance={"meditation_minutes": 60}
            ),
            side_effects=["Headaches when overused", "See disturbing truths"],
            corruption_risk=0.1,
            origin_story="Lord Shiva opened his third eye to see beyond maya (illusion)",
            acquisition_method="Complete the Trial of Truth ritual at a mountain temple",
            prerequisites=["Level 15", "Good Karma", "Meditation Skill"]
        )
        
        # Beast Power - Garuda's Flight
        powers["garuda_wings"] = Power(
            power_id="garuda_wings",
            name="Wings of Garuda",
            description="Manifest ethereal wings like the great eagle Garuda",
            power_type=PowerType.BEAST,
            source=PowerSource.GARUDA_LORD,
            abilities=["Flight", "Wind control", "Sky navigation"],
            stat_bonuses={"agility": 25, "speed": 30},
            special_effects=["Can fly for 30 minutes", "Immune to fall damage"],
            acquisition_cost=PowerCost(
                required_items=["Golden Feather", "Eagle's Talon", "Wind Crystal"],
                experience_cost=300,
                life_force_cost=5,  # Permanent HP reduction
                ritual_components=["Sacred Perch", "Sky Offerings"],
                ritual_location="Highest Mountain Peak",
                ritual_time="Dawn",
                daily_maintenance={"flight_training_minutes": 30}
            ),
            side_effects=["Exhaustion after flight", "Fear of enclosed spaces"],
            corruption_risk=0.05,
            origin_story="Garuda, the divine eagle, grants flight to worthy souls",
            acquisition_method="Tame a divine eagle and perform the Sky Binding ritual",
            prerequisites=["Tamed Eagle Beast", "Wind Affinity", "Level 12"]
        )
        
        # Forbidden Power - Rakshasa Shapeshifting
        powers["rakshasa_form"] = Power(
            power_id="rakshasa_form",
            name="Rakshasa's Deception",
            description="Shapeshift like the demon Rakshasas, but at great cost",
            power_type=PowerType.FORBIDDEN,
            source=PowerSource.NAGA_KING,  # Corrupted source
            abilities=["Shapeshift into animals", "Perfect disguise", "Enhanced senses"],
            stat_bonuses={"deception": 40, "stealth": 30},
            special_effects=["Can take any humanoid form", "Enhanced night vision"],
            acquisition_cost=PowerCost(
                required_items=["Demon Blood", "Cursed Mask", "Shadow Essence"],
                experience_cost=200,
                karma_cost=-50,  # Negative karma required
                sanity_cost=20,  # Permanent sanity loss
                ritual_components=["Dark Moon Blood", "Forbidden Texts"],
                ritual_location="Abandoned Temple",
                ritual_time="Eclipse",
                daily_maintenance={"blood_offerings": 1}
            ),
            side_effects=["Random unwanted transformations", "Violent urges", "Social rejection"],
            corruption_risk=0.8,  # Very high corruption risk
            origin_story="The Rakshasas were once divine beings who fell to darkness",
            acquisition_method="Make a pact with a Rakshasa lord in a dark ritual",
            prerequisites=["Negative Karma", "Dark Knowledge", "Desperation"]
        )
        
        # Add more powers...
        return powers
    
    def _initialize_rituals(self) -> Dict[str, Ritual]:
        """Initialize all rituals in the game"""
        rituals = {}
        
        # Trial of Truth - for Third Eye power
        rituals["trial_of_truth"] = Ritual(
            ritual_id="trial_of_truth",
            name="Trial of Truth",
            description="A sacred ritual to open the third eye and see beyond illusion",
            purpose="Gain the Third Eye of Shiva power",
            required_components=["Sacred Ash", "Rudraksha Beads", "Himalayan Crystal", "Ghee Lamp"],
            required_location="Mountain Peak Temple",
            required_time="New Moon Night",
            participant_count=2,  # Player + Guru
            duration_minutes=180,  # 3 hours
            steps=[
                "Purify the temple space with sacred ash",
                "Light the ghee lamp and place crystals in cardinal directions",
                "Meditate for 1 hour while wearing rudraksha beads",
                "Guru guides the opening of inner sight",
                "Face three trials of truth (illusions to overcome)",
                "If successful, the third eye chakra opens"
            ],
            difficulty=8,
            success_rate=0.7,
            success_effects=["Gain Third Eye power", "Permanent wisdom boost", "Enlightenment"],
            failure_effects=["Spiritual exhaustion", "Temporary blindness", "Wasted components"],
            component_consumption=True,
            energy_cost=50,
            risk_level=6
        )
        
        # Sky Binding - for Garuda Wings
        rituals["sky_binding"] = Ritual(
            ritual_id="sky_binding",
            name="Sky Binding Ritual",
            description="Bond with the spirit of Garuda to gain the power of flight",
            purpose="Acquire Wings of Garuda power",
            required_components=["Golden Feather", "Eagle's Talon", "Wind Crystal", "Sacred Soma"],
            required_location="Highest Mountain Peak",
            required_time="Dawn",
            participant_count=1,
            duration_minutes=120,
            steps=[
                "Climb to the highest accessible peak before dawn",
                "Create a sacred circle with wind crystals",
                "Offer the golden feather and eagle's talon to the sky",
                "Drink sacred soma to purify the spirit",
                "Call upon Garuda with ancient mantras",
                "If worthy, Garuda's blessing manifests as ethereal wings"
            ],
            difficulty=7,
            success_rate=0.6,
            success_effects=["Gain Garuda Wings power", "Sky blessing", "Enhanced agility"],
            failure_effects=["Fall from great height", "Rejection by sky spirits", "Component loss"],
            component_consumption=True,
            energy_cost=40,
            risk_level=8
        )
        
        return rituals
    
    def attempt_power_acquisition(self, player_id: str, power_id: str, 
                                 available_items: List[str], player_data: Dict) -> Dict[str, Any]:
        """Attempt to acquire a new power"""
        if power_id not in self.available_powers:
            return {"success": False, "reason": "Power not found"}
        
        power = self.available_powers[power_id]
        
        # Check prerequisites
        prereq_check = self._check_prerequisites(power, player_data)
        if not prereq_check["met"]:
            return {"success": False, "reason": f"Prerequisites not met: {prereq_check['missing']}"}
        
        # Check if player has required items
        missing_items = []
        for item in power.acquisition_cost.required_items:
            if item not in available_items:
                missing_items.append(item)
        
        if missing_items:
            return {"success": False, "reason": f"Missing items: {missing_items}"}
        
        # Check if ritual is required
        if power.acquisition_cost.ritual_location:
            ritual_result = self._perform_ritual(player_id, power_id, player_data)
            if not ritual_result["success"]:
                return ritual_result
        
        # Apply costs
        self._apply_power_costs(player_id, power)
        
        # Grant power
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerPowerProfile(player_id)
        
        profile = self.player_profiles[player_id]
        profile.active_powers[power_id] = power
        profile.total_power_level += power.level
        
        # Apply any corruption or side effects
        corruption_applied = self._apply_corruption_risk(player_id, power)
        
        return {
            "success": True,
            "power_gained": power.name,
            "abilities": power.abilities,
            "side_effects": power.side_effects,
            "corruption": corruption_applied
        }
    
    def _check_prerequisites(self, power: Power, player_data: Dict) -> Dict[str, Any]:
        """Check if player meets power prerequisites"""
        missing = []
        
        for prereq in power.prerequisites:
            if "Level" in prereq:
                required_level = int(prereq.split()[1])
                if player_data.get("level", 1) < required_level:
                    missing.append(prereq)
            elif "Karma" in prereq:
                karma = player_data.get("karma", 0)
                if "Good" in prereq and karma < 50:
                    missing.append("Good Karma (50+)")
                elif "Negative" in prereq and karma > -30:
                    missing.append("Negative Karma (-30 or lower)")
            # Add more prerequisite checks...
        
        return {"met": len(missing) == 0, "missing": missing}
    
    def _perform_ritual(self, player_id: str, power_id: str, player_data: Dict) -> Dict[str, Any]:
        """Perform the ritual required for power acquisition"""
        power = self.available_powers[power_id]
        
        # Find associated ritual
        ritual = None
        for r in self.available_rituals.values():
            if power_id in r.purpose:
                ritual = r
                break
        
        if not ritual:
            return {"success": False, "reason": "No ritual found for this power"}
        
        # Calculate success rate based on player factors
        base_success = ritual.success_rate
        player_level = player_data.get("level", 1)
        
        # Modify success rate
        if player_level >= 15:
            base_success += 0.1
        if player_data.get("karma", 0) > 30:
            base_success += 0.1
        
        # Roll for success
        success = random.random() < base_success
        
        if success:
            return {
                "success": True,
                "ritual_completed": ritual.name,
                "effects": ritual.success_effects
            }
        else:
            return {
                "success": False,
                "reason": "Ritual failed",
                "consequences": ritual.failure_effects
            }
    
    def _apply_power_costs(self, player_id: str, power: Power):
        """Apply the costs of acquiring a power"""
        # This would integrate with the player's inventory and stats
        # For now, just record that costs were applied
        pass
    
    def _apply_corruption_risk(self, player_id: str, power: Power) -> bool:
        """Apply corruption risk when gaining forbidden or dangerous powers"""
        if random.random() < power.corruption_risk:
            if player_id not in self.player_profiles:
                self.player_profiles[player_id] = PlayerPowerProfile(player_id)
            
            profile = self.player_profiles[player_id]
            profile.corruption_level += random.randint(5, 15)
            
            # Add random corruption effect
            if profile.corruption_level > 20:
                corruption_types = list(PowerCorruption)
                new_corruption = random.choice(corruption_types)
                if new_corruption not in profile.active_corruptions:
                    profile.active_corruptions.append(new_corruption)
            
            return True
        return False
    
    def get_available_powers_for_player(self, player_data: Dict) -> List[Dict[str, Any]]:
        """Get powers that the player can potentially acquire"""
        available = []
        
        for power_id, power in self.available_powers.items():
            prereq_check = self._check_prerequisites(power, player_data)
            
            power_info = {
                "id": power_id,
                "name": power.name,
                "description": power.description,
                "type": power.power_type.value,
                "source": power.source.value,
                "abilities": power.abilities,
                "requirements": power.acquisition_cost.required_items,
                "can_acquire": prereq_check["met"],
                "missing_prerequisites": prereq_check.get("missing", []),
                "risk_level": "High" if power.corruption_risk > 0.5 else "Medium" if power.corruption_risk > 0.2 else "Low"
            }
            available.append(power_info)
        
        return available
    
    def get_player_power_status(self, player_id: str) -> Dict[str, Any]:
        """Get detailed power status for a player"""
        if player_id not in self.player_profiles:
            return {"total_power": 0, "active_powers": [], "corruption": 0}
        
        profile = self.player_profiles[player_id]
        
        return {
            "total_power_level": profile.total_power_level,
            "active_powers": [
                {
                    "name": power.name,
                    "level": power.level,
                    "abilities": power.abilities,
                    "side_effects": power.side_effects
                }
                for power in profile.active_powers.values()
            ],
            "corruption_level": profile.corruption_level,
            "corruption_effects": [c.value for c in profile.active_corruptions],
            "karma_balance": profile.karma_balance,
            "completed_rituals": len(profile.completed_rituals),
            "power_stability": profile.power_stability
        }


# Global power system instance
power_system = PowerSystem()


def test_power_system():
    """Test the power system"""
    print("🔥 Testing Divine and Beast Power System")
    print("=" * 60)
    
    # Test player data
    test_player = {
        "level": 16,
        "karma": 60,
        "experience": 1000
    }
    
    test_items = ["Sacred Ash", "Rudraksha Beads", "Himalayan Crystal"]
    
    print("📊 Available Powers for Level 16 Player:")
    available_powers = power_system.get_available_powers_for_player(test_player)
    
    for power in available_powers:
        print(f"\n🔮 {power['name']}")
        print(f"   Type: {power['type']} | Source: {power['source']}")
        print(f"   Risk: {power['risk_level']}")
        print(f"   Can Acquire: {'✅' if power['can_acquire'] else '❌'}")
        if not power['can_acquire']:
            print(f"   Missing: {power['missing_prerequisites']}")
        print(f"   Abilities: {', '.join(power['abilities'])}")
    
    print("\n" + "=" * 60)
    print("🕉️ Attempting to acquire Third Eye of Shiva...")
    
    # Test power acquisition
    result = power_system.attempt_power_acquisition(
        "test_player", "third_eye", test_items, test_player
    )
    
    if result["success"]:
        print(f"✅ Successfully gained: {result['power_gained']}")
        print(f"   New Abilities: {result['abilities']}")
        if result.get('side_effects'):
            print(f"   Side Effects: {result['side_effects']}")
        if result.get('corruption'):
            print(f"   ⚠️ Corruption applied!")
    else:
        print(f"❌ Failed: {result['reason']}")
    
    # Show final power status
    print("\n📈 Final Power Status:")
    status = power_system.get_player_power_status("test_player")
    print(f"   Total Power Level: {status['total_power_level']}")
    print(f"   Active Powers: {len(status['active_powers'])}")
    print(f"   Corruption Level: {status['corruption_level']}")
    
    print("\n✅ Power system test completed!")


if __name__ == "__main__":
    test_power_system()