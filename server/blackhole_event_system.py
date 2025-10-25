"""
Blackhole Event System - Dimensional Collision Event
Part of the Beast Taming: Classic of Mountains and Seas expansion

This system creates a hidden boss encounter in the beginner village that triggers
a massive blackhole event, causing multiple dimensions to collide and introducing
new races, thousands of job classes, and exclusive server-wide unique classes.
"""

import asyncio
import random
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Tuple
from enum import Enum

class DimensionalRealm(Enum):
    MORTAL_REALM = "mortal_realm"
    CELESTIAL_HEAVEN = "celestial_heaven"
    SHADOW_ABYSS = "shadow_abyss"
    FAIRY_KINGDOM = "fairy_kingdom"
    UNDEAD_NETHERWORLD = "undead_netherworld"
    DEMONIC_PLANE = "demonic_plane"
    ANGELIC_SPHERE = "angelic_sphere"
    ELEMENTAL_CHAOS = "elemental_chaos"

class RaceType(Enum):
    # Original races
    HUMAN = "human"
    DIVINE_HUMAN = "divine_human"
    
    # New dimensional races
    ELF = "elf"
    DARK_ELF = "dark_elf"
    HIGH_ELF = "high_elf"
    FAIRY = "fairy"
    PIXIE = "pixie"
    VAMPIRE = "vampire"
    VAMPIRE_LORD = "vampire_lord"
    DEMON = "demon"
    ARCH_DEMON = "arch_demon"
    ZOMBIE = "zombie"
    LICH = "lich"
    UNDEAD = "undead"
    ANGEL = "angel"
    SERAPH = "seraph"
    DEMIHUMAN = "demihuman"
    BEAST_KIN = "beast_kin"
    DRAGONBORN = "dragonborn"
    CELESTIAL = "celestial"
    SHADOW_BEING = "shadow_being"

@dataclass
class RacialTrait:
    name: str
    description: str
    stat_bonus: Dict[str, int]
    special_abilities: List[str]
    weaknesses: List[str]
    realm_affinity: DimensionalRealm

@dataclass
class ExclusiveClass:
    """Server-unique classes that only one player can hold"""
    class_id: str
    name: str
    description: str
    requirements: Dict[str, Any]
    holder_player_id: Optional[str] = None
    secret_traits: List[str] = field(default_factory=list)
    specialized_weapon: str = ""
    unique_storyline: str = ""
    power_level: int = 100  # Scale 1-100
    dimensional_origin: DimensionalRealm = DimensionalRealm.MORTAL_REALM

@dataclass
class DimensionalBoss:
    """High-level boss with strategic AI that triggers the blackhole event"""
    name: str
    level_offset: int = 5  # Always 5 levels above player
    health_multiplier: float = 3.0
    ai_intelligence: int = 95  # Out of 100
    special_attacks: List[str] = field(default_factory=list)
    movement_patterns: List[str] = field(default_factory=list)
    phase_mechanics: Dict[str, Any] = field(default_factory=dict)
    defeat_triggers_blackhole: bool = True

@dataclass
class BlackholeEvent:
    """The dimensional collision event"""
    event_id: str
    trigger_player: str
    trigger_time: datetime
    active: bool = False
    dimensions_colliding: List[DimensionalRealm] = field(default_factory=list)
    new_races_unlocked: List[RaceType] = field(default_factory=list)
    new_classes_available: List[str] = field(default_factory=list)
    exclusive_classes_released: List[str] = field(default_factory=list)
    world_changes: Dict[str, Any] = field(default_factory=dict)

class BlackholeEventSystem:
    def __init__(self):
        self.secret_area_discovered = False
        self.boss_defeated = False
        self.blackhole_active = False
        self.dimensional_boss = None
        self.current_event = None
        self.server_exclusive_classes = {}
        self.racial_traits = {}
        self.job_classes = {}
        
        self._initialize_secret_area()
        self._initialize_dimensional_boss()
        self._initialize_racial_traits()
        self._initialize_job_classes()
        self._initialize_exclusive_classes()

    def _initialize_secret_area(self):
        """Set up the hidden area in beginner village"""
        self.secret_area = {
            "name": "The Forgotten Shrine of Cosmic Convergence",
            "location": "Hidden beneath the Ancient Banyan Tree in beginner village",
            "discovery_requirements": {
                "player_level": 5,
                "secret_knowledge": "Ancient inscription about 'where earth meets sky'",
                "time_requirement": "Must be discovered at midnight",
                "offering_required": "Sacred flower from village temple"
            },
            "description": "A mysterious underground shrine with swirling cosmic energy",
            "hidden_entrance": "Touch the banyan tree roots while holding sacred flower at midnight",
            "area_effects": {
                "energy_drain": "Slowly drains mana while inside",
                "time_distortion": "Time moves differently here",
                "dimensional_weakness": "Reality is unstable"
            }
        }

    def _initialize_dimensional_boss(self):
        """Create the high-level strategic AI boss"""
        self.dimensional_boss = DimensionalBoss(
            name="Void Keeper Kshemendra",
            level_offset=5,
            health_multiplier=3.0,
            ai_intelligence=95,
            special_attacks=[
                "Dimensional Rift Strike - Creates portals that attack from behind",
                "Reality Warp - Teleports player to random locations",
                "Cosmic Drain - Steals player's mana and health over time",
                "Mirror Dimension - Creates false copies of the arena",
                "Void Chains - Restricts player movement with energy bonds",
                "Prophecy Strike - Predicts and counters player's next 3 moves"
            ],
            movement_patterns=[
                "Dimensional Phase - Becomes untargetable while moving",
                "Predictive Positioning - Moves to counter player strategy",
                "Zone Control - Creates dangerous areas to limit player movement",
                "Adaptive Kiting - Maintains optimal distance based on player class",
                "Confusion Tactics - Rapid teleportation to disorient player"
            ],
            phase_mechanics={
                "phase_1": {
                    "health_threshold": 100,
                    "behavior": "Tests player with basic attacks and movement",
                    "special": "Studies player combat patterns"
                },
                "phase_2": {
                    "health_threshold": 60,
                    "behavior": "Adapts strategy based on observed patterns",
                    "special": "Counters player's preferred tactics"
                },
                "phase_3": {
                    "health_threshold": 30,
                    "behavior": "Desperate dimensional manipulation",
                    "special": "Reality becomes increasingly unstable"
                },
                "final_phase": {
                    "health_threshold": 5,
                    "behavior": "Attempts to tear open dimensional barrier",
                    "special": "If defeated here, triggers blackhole event"
                }
            }
        )

    def _initialize_racial_traits(self):
        """Define traits for all new races"""
        self.racial_traits = {
            RaceType.ELF: RacialTrait(
                name="High Elf",
                description="Graceful beings with natural magic affinity",
                stat_bonus={"mana": 50, "intelligence": 20, "agility": 15},
                special_abilities=["Nature Magic", "Enhanced Archery", "Long Lifespan"],
                weaknesses=["Iron Sensitivity", "Lower Physical Strength"],
                realm_affinity=DimensionalRealm.FAIRY_KINGDOM
            ),
            RaceType.DARK_ELF: RacialTrait(
                name="Dark Elf",
                description="Shadow-dwelling elves with dark magic mastery",
                stat_bonus={"mana": 40, "stealth": 25, "dark_resistance": 30},
                special_abilities=["Shadow Magic", "Night Vision", "Poison Immunity"],
                weaknesses=["Light Sensitivity", "Holy Damage Vulnerability"],
                realm_affinity=DimensionalRealm.SHADOW_ABYSS
            ),
            RaceType.VAMPIRE: RacialTrait(
                name="Vampire",
                description="Undead beings with blood magic and immortality",
                stat_bonus={"strength": 30, "regeneration": 50, "charm": 25},
                special_abilities=["Blood Drain", "Bat Transformation", "Hypnosis"],
                weaknesses=["Sunlight Damage", "Holy Water", "Wooden Stakes"],
                realm_affinity=DimensionalRealm.UNDEAD_NETHERWORLD
            ),
            RaceType.FAIRY: RacialTrait(
                name="Fairy",
                description="Tiny magical beings with flight and nature powers",
                stat_bonus={"mana": 60, "agility": 40, "nature_affinity": 50},
                special_abilities=["Flight", "Plant Growth", "Healing Magic"],
                weaknesses=["Physical Fragility", "Cold Iron", "Small Size"],
                realm_affinity=DimensionalRealm.FAIRY_KINGDOM
            ),
            RaceType.DEMON: RacialTrait(
                name="Demon",
                description="Fiery beings from the infernal planes",
                stat_bonus={"strength": 25, "fire_resistance": 40, "intimidation": 30},
                special_abilities=["Fire Magic", "Fear Aura", "Damage Resistance"],
                weaknesses=["Holy Damage", "Cold Iron", "Sacred Symbols"],
                realm_affinity=DimensionalRealm.DEMONIC_PLANE
            ),
            RaceType.ANGEL: RacialTrait(
                name="Angel",
                description="Divine beings of pure light and healing",
                stat_bonus={"wisdom": 30, "healing": 50, "light_affinity": 40},
                special_abilities=["Divine Magic", "Flight", "Undead Turning"],
                weaknesses=["Dark Magic", "Corruption", "Unholy Ground"],
                realm_affinity=DimensionalRealm.ANGELIC_SPHERE
            ),
            RaceType.ZOMBIE: RacialTrait(
                name="Zombie",
                description="Reanimated corpses with incredible endurance",
                stat_bonus={"endurance": 50, "pain_resistance": 100, "intimidation": 20},
                special_abilities=["Undead Resilience", "Disease Immunity", "Hunger Drive"],
                weaknesses=["Holy Damage", "Fire", "Headshot Vulnerability"],
                realm_affinity=DimensionalRealm.UNDEAD_NETHERWORLD
            ),
            RaceType.DRAGONBORN: RacialTrait(
                name="Dragonborn",
                description="Humanoid dragons with ancient power",
                stat_bonus={"strength": 35, "mana": 30, "elemental_resistance": 25},
                special_abilities=["Dragon Breath", "Scale Armor", "Ancient Knowledge"],
                weaknesses=["Dragon Hunter Weapons", "Opposite Element"],
                realm_affinity=DimensionalRealm.ELEMENTAL_CHAOS
            ),
            # Add more races as needed...
        }

    def _initialize_job_classes(self):
        """Generate 1000+ job classes across all dimensions"""
        # Base class categories
        base_categories = [
            "Warrior", "Mage", "Rogue", "Priest", "Ranger", "Paladin", "Necromancer",
            "Bard", "Monk", "Druid", "Warlock", "Sorcerer", "Barbarian", "Artificer"
        ]
        
        # Dimensional specializations
        dimensional_specs = {
            DimensionalRealm.CELESTIAL_HEAVEN: ["Divine", "Celestial", "Holy", "Sacred", "Blessed"],
            DimensionalRealm.SHADOW_ABYSS: ["Shadow", "Dark", "Void", "Cursed", "Forbidden"],
            DimensionalRealm.FAIRY_KINGDOM: ["Fey", "Nature", "Wild", "Primal", "Enchanted"],
            DimensionalRealm.UNDEAD_NETHERWORLD: ["Death", "Bone", "Soul", "Grave", "Undying"],
            DimensionalRealm.DEMONIC_PLANE: ["Infernal", "Demon", "Hellish", "Corrupted", "Chaos"],
            DimensionalRealm.ANGELIC_SPHERE: ["Angelic", "Pure", "Radiant", "Heavenly", "Divine"],
            DimensionalRealm.ELEMENTAL_CHAOS: ["Fire", "Water", "Earth", "Air", "Lightning"]
        }
        
        # Generate classes
        class_id = 1
        for realm, specs in dimensional_specs.items():
            for base in base_categories:
                for spec in specs:
                    for tier in ["Apprentice", "Adept", "Master", "Grandmaster", "Legendary"]:
                        class_name = f"{spec} {base} {tier}"
                        self.job_classes[f"class_{class_id}"] = {
                            "id": f"class_{class_id}",
                            "name": class_name,
                            "category": base,
                            "specialization": spec,
                            "tier": tier,
                            "realm": realm,
                            "requirements": self._generate_class_requirements(tier, realm),
                            "abilities": self._generate_class_abilities(base, spec, tier),
                            "exclusive": False
                        }
                        class_id += 1
        
        # Add more unique combinations to reach 1000+
        unique_combinations = [
            "Beast", "Dragon", "Phoenix", "Serpent", "Wolf", "Eagle", "Lion", "Tiger",
            "Spider", "Scorpion", "Kraken", "Leviathan", "Behemoth", "Chimera",
            "Crystal", "Metal", "Poison", "Acid", "Ice", "Magma", "Storm", "Cosmic"
        ]
        
        for combo in unique_combinations:
            for base in base_categories:
                for tier in ["Initiate", "Warrior", "Champion", "Lord", "Emperor"]:
                    class_name = f"{combo} {base} {tier}"
                    self.job_classes[f"class_{class_id}"] = {
                        "id": f"class_{class_id}",
                        "name": class_name,
                        "category": base,
                        "specialization": combo,
                        "tier": tier,
                        "realm": DimensionalRealm.MORTAL_REALM,
                        "requirements": self._generate_class_requirements(tier, DimensionalRealm.MORTAL_REALM),
                        "abilities": self._generate_class_abilities(base, combo, tier),
                        "exclusive": False
                    }
                    class_id += 1

    def _generate_class_requirements(self, tier: str, realm: DimensionalRealm) -> Dict[str, Any]:
        """Generate requirements for class access"""
        base_level = {"Apprentice": 1, "Adept": 20, "Master": 50, "Grandmaster": 80, "Legendary": 100}
        return {
            "min_level": base_level.get(tier, 1),
            "realm_access": realm.value,
            "stat_requirements": {"strength": 10, "mana": 10, "agility": 10},
            "quest_completion": f"Complete {tier} Trial in {realm.value}"
        }

    def _generate_class_abilities(self, base: str, spec: str, tier: str) -> List[str]:
        """Generate abilities for each class"""
        abilities = [f"{spec} {base} Mastery"]
        
        if tier == "Legendary":
            abilities.extend([
                f"Ultimate {spec} Power",
                f"{base} Perfection",
                "Dimensional Awareness"
            ])
        elif tier == "Grandmaster":
            abilities.extend([
                f"Advanced {spec} Control",
                f"{base} Expertise"
            ])
        
        return abilities

    def _initialize_exclusive_classes(self):
        """Create server-unique classes that only one player can hold"""
        self.exclusive_classes = {
            "void_emperor": ExclusiveClass(
                class_id="void_emperor",
                name="Emperor of the Void",
                description="Master of dimensional rifts and cosmic power",
                requirements={
                    "defeat_dimensional_boss": True,
                    "trigger_blackhole_event": True,
                    "min_level": 100,
                    "corruption_resistance": 90
                },
                secret_traits=[
                    "Can create permanent dimensional portals",
                    "Commands lesser void entities",
                    "Immune to dimensional damage",
                    "Can banish players to void realm temporarily"
                ],
                specialized_weapon="Void Scepter of Cosmic Dominion",
                unique_storyline="The Emperor seeks to unite all dimensions under void rule",
                power_level=100,
                dimensional_origin=DimensionalRealm.SHADOW_ABYSS
            ),
            "celestial_harbinger": ExclusiveClass(
                class_id="celestial_harbinger",
                name="Harbinger of Celestial Convergence",
                description="Prophet of the dimensional collision",
                requirements={
                    "witness_blackhole_event": True,
                    "pure_karma": 100,
                    "divine_favor": 90
                },
                secret_traits=[
                    "Predicts future dimensional events",
                    "Can communicate with all dimensional beings",
                    "Grants dimensional blessings to others",
                    "Sees through all illusions and deceptions"
                ],
                specialized_weapon="Staff of Infinite Realms",
                unique_storyline="The Harbinger guides souls through the merged dimensions",
                power_level=95,
                dimensional_origin=DimensionalRealm.CELESTIAL_HEAVEN
            ),
            "shadow_sovereign": ExclusiveClass(
                class_id="shadow_sovereign",
                name="Sovereign of Merged Shadows",
                description="Ruler of all shadow beings across dimensions",
                requirements={
                    "shadow_mastery": 100,
                    "defeat_100_shadow_beings": True,
                    "corruption_level": 75
                },
                secret_traits=[
                    "Controls shadow portals between dimensions",
                    "Commands shadow armies",
                    "Can exist in multiple dimensions simultaneously",
                    "Drains power from light-based abilities"
                ],
                specialized_weapon="Blade of Consuming Darkness",
                unique_storyline="The Sovereign seeks to merge all dimensions into eternal shadow",
                power_level=98,
                dimensional_origin=DimensionalRealm.SHADOW_ABYSS
            ),
            "fairy_monarch": ExclusiveClass(
                class_id="fairy_monarch",
                name="Monarch of All Fairy Realms",
                description="Supreme ruler of fairy kingdoms across dimensions",
                requirements={
                    "fairy_friendship": 100,
                    "nature_mastery": 95,
                    "protect_fairy_realm": True
                },
                secret_traits=[
                    "Can shrink or enlarge at will",
                    "Commands all natural forces",
                    "Creates magical fairy rings for fast travel",
                    "Grants fairy blessings that boost XP gain"
                ],
                specialized_weapon="Crown of Eternal Seasons",
                unique_storyline="The Monarch protects fairy realms from dimensional chaos",
                power_level=85,
                dimensional_origin=DimensionalRealm.FAIRY_KINGDOM
            ),
            "undead_overlord": ExclusiveClass(
                class_id="undead_overlord",
                name="Overlord of the Undead Legions",
                description="Supreme commander of all undead across dimensions",
                requirements={
                    "necromancy_mastery": 100,
                    "raise_1000_undead": True,
                    "resist_holy_magic": True
                },
                secret_traits=[
                    "Instantly raises fallen enemies as undead servants",
                    "Immune to death magic and life drain",
                    "Can create permanent undead settlements",
                    "Commands liches and vampire lords"
                ],
                specialized_weapon="Scythe of Eternal Undeath",
                unique_storyline="The Overlord seeks to convert all living beings to undeath",
                power_level=92,
                dimensional_origin=DimensionalRealm.UNDEAD_NETHERWORLD
            )
        }

    async def check_secret_area_discovery(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Check if player can discover the secret area"""
        current_time = datetime.now().hour
        requirements = self.secret_area["discovery_requirements"]
        
        result = {
            "can_discover": False,
            "missing_requirements": [],
            "hints": []
        }
        
        # Check level requirement
        if player.get("level", 0) < requirements["player_level"]:
            result["missing_requirements"].append(f"Must be level {requirements['player_level']} or higher")
        
        # Check time requirement
        if current_time != 0:  # Not midnight
            result["missing_requirements"].append("Must visit at the stroke of midnight")
            result["hints"].append("The ancient inscription mentions 'when darkness is deepest'")
        
        # Check if player has sacred flower
        if "sacred_flower" not in player.get("inventory", []):
            result["missing_requirements"].append("Must possess a sacred flower from the village temple")
            result["hints"].append("The village priest might know about sacred offerings")
        
        # Check if player has the secret knowledge
        if not player.get("secret_knowledge", {}).get("cosmic_convergence", False):
            result["missing_requirements"].append("Must understand the ancient inscription")
            result["hints"].append("Seek wisdom from the old scholar about 'where earth meets sky'")
        
        if not result["missing_requirements"]:
            result["can_discover"] = True
            result["discovery_message"] = (
                "As you approach the ancient banyan tree at midnight, holding the sacred flower, "
                "the roots begin to glow with otherworldly energy. A hidden passage opens beneath..."
            )
        
        return result

    async def initiate_boss_fight(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Start the dimensional boss encounter"""
        if not self.secret_area_discovered:
            return {"error": "Secret area not discovered yet"}
        
        # Set boss level based on player level
        boss_level = player.get("level", 1) + self.dimensional_boss.level_offset
        boss_health = player.get("max_health", 100) * self.dimensional_boss.health_multiplier
        
        boss_encounter = {
            "boss": {
                "name": self.dimensional_boss.name,
                "level": boss_level,
                "health": boss_health,
                "max_health": boss_health,
                "current_phase": 1,
                "ai_state": "analyzing_player",
                "learned_patterns": []
            },
            "arena": {
                "name": "Cosmic Convergence Chamber",
                "effects": [
                    "Reality distortion - Random teleportation",
                    "Dimensional energy - Mana regeneration altered",
                    "Void presence - Gradual sanity loss"
                ],
                "danger_zones": []
            },
            "combat_log": [
                f"You enter the cosmic chamber and face {self.dimensional_boss.name}!",
                f"The Void Keeper's eyes glow with ancient knowledge as it studies your movements...",
                "Reality itself seems unstable in this place."
            ]
        }
        
        return boss_encounter

    async def process_boss_ai_turn(self, boss_state: Dict[str, Any], player_action: str) -> Dict[str, Any]:
        """Process the boss's AI decision making"""
        ai_response = {
            "boss_action": "",
            "movement": "",
            "special_effect": "",
            "ai_learning": "",
            "phase_change": False
        }
        
        # AI learns from player patterns
        boss_state["learned_patterns"].append(player_action)
        
        # Determine boss phase based on health
        health_percentage = (boss_state["health"] / boss_state["max_health"]) * 100
        
        if health_percentage <= 5:
            current_phase = "final_phase"
        elif health_percentage <= 30:
            current_phase = "phase_3"
        elif health_percentage <= 60:
            current_phase = "phase_2"
        else:
            current_phase = "phase_1"
        
        # Get phase mechanics
        phase_info = self.dimensional_boss.phase_mechanics.get(current_phase, {})
        
        # AI decision based on learned patterns and phase
        if len(boss_state["learned_patterns"]) >= 3:
            # Counter player's most common action
            common_actions = {}
            for action in boss_state["learned_patterns"][-6:]:  # Last 6 actions
                common_actions[action] = common_actions.get(action, 0) + 1
            
            most_common = max(common_actions.items(), key=lambda x: x[1])[0]
            ai_response["boss_action"] = self._counter_player_action(most_common)
            ai_response["ai_learning"] = f"The Void Keeper has learned to counter your {most_common}!"
        
        # Phase-specific behavior
        if current_phase == "final_phase":
            ai_response["special_effect"] = "Reality tears as the Void Keeper attempts dimensional breach!"
            if random.random() < 0.3:  # 30% chance to trigger event preparation
                ai_response["dimensional_warning"] = "Dimensional barriers are failing! Defeat the boss quickly!"
        
        # Strategic movement
        movement_pattern = random.choice(self.dimensional_boss.movement_patterns)
        ai_response["movement"] = movement_pattern
        
        return ai_response

    def _counter_player_action(self, player_action: str) -> str:
        """AI counters for common player actions"""
        counters = {
            "attack": "Dimensional Phase - becomes untargetable",
            "defend": "Reality Warp - bypasses defense",
            "cast_spell": "Void Drain - absorbs magical energy",
            "heal": "Prophecy Strike - predicts and interrupts",
            "move": "Zone Control - limits movement options"
        }
        return counters.get(player_action, "Adaptive Counter - responds to unknown strategy")

    async def trigger_blackhole_event(self, triggering_player: str) -> Dict[str, Any]:
        """Trigger the massive dimensional collision event"""
        if self.blackhole_active:
            return {"error": "Blackhole event already active"}
        
        # Create the blackhole event
        self.current_event = BlackholeEvent(
            event_id=f"blackhole_{datetime.now().isoformat()}",
            trigger_player=triggering_player,
            trigger_time=datetime.now(),
            active=True,
            dimensions_colliding=[
                DimensionalRealm.MORTAL_REALM,
                DimensionalRealm.CELESTIAL_HEAVEN,
                DimensionalRealm.SHADOW_ABYSS,
                DimensionalRealm.FAIRY_KINGDOM,
                DimensionalRealm.UNDEAD_NETHERWORLD,
                DimensionalRealm.DEMONIC_PLANE,
                DimensionalRealm.ANGELIC_SPHERE,
                DimensionalRealm.ELEMENTAL_CHAOS
            ],
            new_races_unlocked=list(RaceType),
            new_classes_available=list(self.job_classes.keys()),
            exclusive_classes_released=list(self.exclusive_classes.keys()),
            world_changes={
                "dimensional_rifts": "Rifts appear throughout the world",
                "mixed_biomes": "Different dimensional areas merge",
                "new_npcs": "Beings from other dimensions appear",
                "altered_physics": "Magic and technology work differently",
                "time_distortions": "Some areas experience time differently"
            }
        )
        
        self.blackhole_active = True
        
        # Server-wide announcement
        event_announcement = {
            "type": "DIMENSIONAL_COLLISION",
            "title": "🌌 THE GREAT CONVERGENCE HAS BEGUN! 🌌",
            "message": f"""
ATTENTION ALL PLAYERS!

{triggering_player} has defeated the Void Keeper and triggered a catastrophic dimensional event!

🌍 MULTIPLE DIMENSIONS ARE COLLIDING! 🌍

IMMEDIATE CHANGES:
✨ 20+ NEW PLAYABLE RACES available (Elves, Fairies, Vampires, Demons, Angels, and more!)
⚔️ 1000+ NEW JOB CLASSES unlocked across all dimensions!
👑 EXCLUSIVE SERVER-UNIQUE CLASSES now available (only ONE player can hold each!)
🌟 New dimensional areas, NPCs, and storylines!
⚡ World physics and magic systems altered!

The world will never be the same. Choose your new destiny wisely!

New races can be selected at any Dimensional Rift.
Exclusive classes require special quests and achievements.

May the convergence bring you power or doom...
            """,
            "duration": 300,  # 5 minutes
            "effects": {
                "new_races": True,
                "expanded_classes": True,
                "world_transformation": True
            }
        }
        
        return {
            "success": True,
            "event": self.current_event,
            "announcement": event_announcement,
            "immediate_effects": self._apply_immediate_world_changes()
        }

    def _apply_immediate_world_changes(self) -> Dict[str, Any]:
        """Apply immediate changes to the world"""
        return {
            "dimensional_rifts": [
                {
                    "location": "Village Square",
                    "leads_to": "Fairy Kingdom Outpost",
                    "requirements": "None - beginner friendly"
                },
                {
                    "location": "Dark Forest",
                    "leads_to": "Shadow Abyss Border",
                    "requirements": "Level 20+ recommended"
                },
                {
                    "location": "Temple Grounds",
                    "leads_to": "Celestial Heaven Gateway",
                    "requirements": "Pure karma required"
                },
                {
                    "location": "Ancient Ruins",
                    "leads_to": "Undead Netherworld",
                    "requirements": "Warning: High danger zone"
                }
            ],
            "new_npcs": [
                {
                    "name": "Lyralei the High Elf",
                    "location": "Village Square",
                    "services": ["Race change to Elf", "Archery training", "Nature magic"]
                },
                {
                    "name": "Valdris the Vampire Lord",
                    "location": "Dark Alley",
                    "services": ["Race change to Vampire", "Blood magic", "Night abilities"]
                },
                {
                    "name": "Seraphina the Angel",
                    "location": "Temple",
                    "services": ["Race change to Angel", "Divine magic", "Healing arts"]
                }
            ],
            "altered_areas": {
                "beginner_village": "Now has dimensional rifts and new NPCs",
                "dark_forest": "Partially merged with Shadow Abyss",
                "temple_grounds": "Touched by celestial energy",
                "ancient_ruins": "Undead presence detected"
            }
        }

    async def check_exclusive_class_eligibility(self, player: Dict[str, Any], class_id: str) -> Dict[str, Any]:
        """Check if player is eligible for an exclusive class"""
        if class_id not in self.exclusive_classes:
            return {"error": "Exclusive class not found"}
        
        exclusive_class = self.exclusive_classes[class_id]
        
        # Check if class is already taken
        if exclusive_class.holder_player_id:
            return {
                "eligible": False,
                "reason": f"Class already held by {exclusive_class.holder_player_id}",
                "challenge_option": "You may challenge the current holder to a duel"
            }
        
        # Check requirements
        eligible = True
        missing_requirements = []
        
        for req, value in exclusive_class.requirements.items():
            if req == "defeat_dimensional_boss" and not player.get("defeated_void_keeper", False):
                eligible = False
                missing_requirements.append("Must defeat the Void Keeper")
            elif req == "trigger_blackhole_event" and player.get("username") != self.current_event.trigger_player:
                eligible = False
                missing_requirements.append("Must be the one who triggered the blackhole event")
            elif req == "min_level" and player.get("level", 0) < value:
                eligible = False
                missing_requirements.append(f"Must be level {value} or higher")
            # Add more requirement checks...
        
        return {
            "eligible": eligible,
            "missing_requirements": missing_requirements,
            "class_info": exclusive_class,
            "quest_available": eligible
        }

    async def grant_exclusive_class(self, player_id: str, class_id: str) -> Dict[str, Any]:
        """Grant an exclusive class to a player"""
        if class_id not in self.exclusive_classes:
            return {"error": "Exclusive class not found"}
        
        exclusive_class = self.exclusive_classes[class_id]
        
        if exclusive_class.holder_player_id:
            return {"error": "Class already taken"}
        
        # Grant the class
        exclusive_class.holder_player_id = player_id
        
        return {
            "success": True,
            "message": f"Congratulations! You are now the {exclusive_class.name}!",
            "class_granted": exclusive_class,
            "server_announcement": f"{player_id} has claimed the title of {exclusive_class.name}!",
            "unique_abilities": exclusive_class.secret_traits,
            "specialized_weapon": exclusive_class.specialized_weapon
        }

    def get_available_races(self) -> Dict[str, RacialTrait]:
        """Get all available races after blackhole event"""
        if not self.blackhole_active:
            return {
                RaceType.HUMAN.value: RacialTrait(
                    name="Human", 
                    description="Original mortal race",
                    stat_bonus={},
                    special_abilities=[],
                    weaknesses=[],
                    realm_affinity=DimensionalRealm.MORTAL_REALM
                )
            }
        
        return {race.value: trait for race, trait in self.racial_traits.items()}

    def get_available_job_classes(self, player_level: int = 1) -> Dict[str, Any]:
        """Get job classes available to the player"""
        available = {}
        
        for class_id, job_class in self.job_classes.items():
            if player_level >= job_class["requirements"]["min_level"]:
                available[class_id] = job_class
        
        return available

    def get_event_status(self) -> Dict[str, Any]:
        """Get current status of the blackhole event"""
        return {
            "blackhole_active": self.blackhole_active,
            "secret_area_discovered": self.secret_area_discovered,
            "boss_defeated": self.boss_defeated,
            "current_event": self.current_event.__dict__ if self.current_event else None,
            "dimensions_available": len(DimensionalRealm) if self.blackhole_active else 1,
            "races_available": len(self.racial_traits) if self.blackhole_active else 1,
            "total_job_classes": len(self.job_classes),
            "exclusive_classes_taken": len([c for c in self.exclusive_classes.values() if c.holder_player_id])
        }

# Example usage and testing
async def main():
    """Test the blackhole event system"""
    system = BlackholeEventSystem()
    
    # Test player
    test_player = {
        "username": "TestPlayer",
        "level": 15,
        "inventory": ["sacred_flower"],
        "secret_knowledge": {"cosmic_convergence": True},
        "max_health": 100
    }
    
    print("=== BLACKHOLE EVENT SYSTEM TEST ===\n")
    
    # Test secret area discovery
    print("1. Testing secret area discovery...")
    discovery_result = await system.check_secret_area_discovery(test_player)
    print(f"Can discover: {discovery_result['can_discover']}")
    if discovery_result['can_discover']:
        print(f"Discovery message: {discovery_result['discovery_message']}")
        system.secret_area_discovered = True
    else:
        print(f"Missing requirements: {discovery_result['missing_requirements']}")
        # For testing, assume discovery
        system.secret_area_discovered = True
    
    print("\n2. Testing boss encounter initiation...")
    boss_fight = await system.initiate_boss_fight(test_player)
    print(f"Boss: {boss_fight['boss']['name']} (Level {boss_fight['boss']['level']})")
    print(f"Arena: {boss_fight['arena']['name']}")
    
    print("\n3. Testing boss AI...")
    ai_turn = await system.process_boss_ai_turn(boss_fight['boss'], "attack")
    print(f"Boss action: {ai_turn['boss_action']}")
    print(f"AI learning: {ai_turn['ai_learning']}")
    
    print("\n4. Testing blackhole event trigger...")
    blackhole_result = await system.trigger_blackhole_event("TestPlayer")
    if blackhole_result.get("success"):
        print("✅ BLACKHOLE EVENT TRIGGERED!")
        print(f"Dimensions colliding: {len(blackhole_result['event'].dimensions_colliding)}")
        print(f"New races unlocked: {len(blackhole_result['event'].new_races_unlocked)}")
        print(f"New job classes: {len(blackhole_result['event'].new_classes_available)}")
    
    print("\n5. Testing available content after event...")
    races = system.get_available_races()
    print(f"Available races: {len(races)}")
    for race_key in list(races.keys())[:5]:  # Show first 5
        race = races[race_key]
        print(f"  - {race.name}: {race.description}")
    
    job_classes = system.get_available_job_classes(test_player["level"])
    print(f"\nAvailable job classes for level {test_player['level']}: {len(job_classes)}")
    for class_key in list(job_classes.keys())[:5]:  # Show first 5
        job_class = job_classes[class_key]
        print(f"  - {job_class['name']} ({job_class['tier']})")
    
    print("\n6. Testing exclusive class eligibility...")
    exclusive_check = await system.check_exclusive_class_eligibility(test_player, "void_emperor")
    print(f"Eligible for Void Emperor: {exclusive_check['eligible']}")
    if not exclusive_check['eligible']:
        print(f"Missing: {exclusive_check['missing_requirements']}")
    
    print(f"\n=== EVENT STATUS ===")
    status = system.get_event_status()
    print(f"Blackhole active: {status['blackhole_active']}")
    print(f"Dimensions available: {status['dimensions_available']}")
    print(f"Total races: {status['races_available']}")
    print(f"Total job classes: {status['total_job_classes']}")
    print(f"Exclusive classes taken: {status['exclusive_classes_taken']}/5")

if __name__ == "__main__":
    asyncio.run(main())