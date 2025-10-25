"""
Procedural Generation Framework - Dynamic Content Creator
Generates thousands of job classes, weapons, beasts, and divine entities
using combinatorial algorithms and template systems
"""

import random
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class ContentRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"
    DIVINE = "divine"


@dataclass
class GeneratedJobClass:
    class_id: str
    name: str
    role: str
    element: str
    theme: str
    description: str
    rarity: ContentRarity
    abilities: List[str] = field(default_factory=list)
    stat_bonuses: Dict[str, int] = field(default_factory=dict)
    requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GeneratedWeapon:
    weapon_id: str
    name: str
    weapon_type: str
    material: str
    enchantment: str
    description: str
    rarity: ContentRarity
    damage_range: Tuple[int, int] = (10, 20)
    special_effects: List[str] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GeneratedBeast:
    beast_id: str
    name: str
    base_creature: str
    modifier: str
    origin: str
    description: str
    rarity: ContentRarity
    abilities: List[str] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    taming_difficulty: int = 50

@dataclass
class GeneratedDivineEntity:
    entity_id: str
    name: str
    domain: str
    form: str
    alignment: str
    description: str
    rarity: ContentRarity
    powers: List[str] = field(default_factory=list)
    favor_requirements: List[str] = field(default_factory=list)

class ProceduralGenerator:
    def __init__(self):
        # Job Class Components
        self.roles = [
            "Warrior", "Mage", "Rogue", "Cleric", "Ranger", "Artisan", "Hybrid", "Exotic",
            "Paladin", "Necromancer", "Bard", "Monk", "Druid", "Warlock", "Sorcerer", "Barbarian",
            "Assassin", "Guardian", "Healer", "Scout", "Enchanter", "Summoner", "Berserker",
            "Templar", "Shaman", "Oracle", "Mystic", "Bladedancer", "Spellsword", "Shadowmancer"
        ]
        
        self.elements = [
            "Fire", "Ice", "Lightning", "Earth", "Wind", "Shadow", "Light", "Void",
            "Water", "Metal", "Wood", "Crystal", "Plasma", "Acid", "Poison", "Spirit",
            "Cosmic", "Temporal", "Psychic", "Arcane", "Divine", "Infernal", "Primal", "Astral"
        ]
        
        self.themes = [
            "Time", "Dreams", "Blood", "Stars", "Machines", "Nature", "Chaos", "Order",
            "Death", "Life", "Memory", "Fate", "Honor", "Vengeance", "Wisdom", "Madness",
            "Storm", "Ocean", "Mountain", "Desert", "Forest", "Sky", "Abyss", "Paradise",
            "War", "Peace", "Hunt", "Song", "Dance", "Forge", "Harvest", "Eclipse"
        ]
        
        # Weapon Components
        self.weapon_types = [
            "Sword", "Staff", "Bow", "Dagger", "Axe", "Gun", "Whip", "Orb",
            "Spear", "Hammer", "Shield", "Gauntlet", "Crossbow", "Blade", "Wand", "Scepter",
            "Katana", "Scythe", "Mace", "Flail", "Halberd", "Rapier", "Claymore", "Chakram",
            "Trident", "Javelin", "Kris", "Falchion", "Glaive", "Partisan"
        ]
        
        self.materials = [
            "Crystal", "Bone", "Iron", "Ether", "Flame", "Ice", "Shadow", "Light",
            "Steel", "Mithril", "Adamant", "Obsidian", "Diamond", "Ruby", "Sapphire", "Emerald",
            "Void", "Star", "Moon", "Sun", "Storm", "Ocean", "Earth", "Wind",
            "Blood", "Soul", "Spirit", "Dream", "Nightmare", "Time"
        ]
        
        self.enchantments = [
            "Screaming", "Whispering", "Echoing", "Burning", "Frozen", "Pulsing",
            "Singing", "Howling", "Glowing", "Vibrating", "Humming", "Crackling",
            "Shimmering", "Thundering", "Bleeding", "Healing", "Cursed", "Blessed",
            "Raging", "Calm", "Sharp", "Dull", "Heavy", "Light", "Fast", "Slow",
            "Wise", "Mad", "Ancient", "Eternal"
        ]
        
        # Beast Components
        self.base_creatures = [
            "Dragon", "Wolf", "Serpent", "Phoenix", "Spider", "Leviathan", "Wyrm",
            "Tiger", "Bear", "Eagle", "Shark", "Panther", "Scorpion", "Mantis",
            "Raven", "Falcon", "Lion", "Elephant", "Rhino", "Kraken", "Hydra",
            "Chimera", "Griffin", "Basilisk", "Cockatrice", "Manticore", "Sphinx",
            "Pegasus", "Unicorn", "Qilin"
        ]
        
        self.creature_modifiers = [
            "Skyrazor", "Flamehowl", "Frostfang", "Voidmaw", "Thornhide", "Dream-Eater",
            "Stormclaw", "Shadowstrike", "Lightbringer", "Doomcaller", "Bloodthirst", "Soulrend",
            "Ironhide", "Swiftwing", "Deathgaze", "Lifebane", "Windwalker", "Earthshaker",
            "Starfall", "Moonhowl", "Sunburst", "Nightstalker", "Dawnbreaker", "Duskbringer",
            "Crystalclaw", "Bonecrusher", "Spiritbane", "Ghostwalker", "Wraithcaller", "Soulforge"
        ]
        
        self.origins = [
            "Abyssal", "Celestial", "Elemental", "Undead", "Primordial", "Mechanical",
            "Divine", "Infernal", "Astral", "Ethereal", "Temporal", "Spectral",
            "Ancient", "Forgotten", "Lost", "Hidden", "Sacred", "Cursed",
            "Eternal", "Mortal", "Immortal", "Legendary", "Mythical", "Arcane",
            "Primal", "Pure", "Corrupted", "Blessed", "Damned", "Neutral"
        ]
        
        # Divine Entity Components
        self.domains = [
            "Time", "War", "Secrets", "Dreams", "Harvest", "Chaos", "Stars",
            "Death", "Life", "Love", "Hate", "Wisdom", "Madness", "Justice",
            "Vengeance", "Hope", "Despair", "Memory", "Forge", "Hunt",
            "Song", "Dance", "Art", "Craft", "Trade", "Travel", "Home",
            "Storm", "Ocean", "Mountain", "Forest", "Desert", "Sky"
        ]
        
        self.divine_forms = [
            "Whisper", "Flame", "Mask", "Blade", "Song", "Eye", "Crown",
            "Voice", "Shadow", "Light", "Storm", "Wind", "Earth", "Water",
            "Star", "Moon", "Sun", "Mirror", "Book", "Key", "Door",
            "Tree", "Flower", "Stone", "River", "Mountain", "Sky", "Void",
            "Heart", "Soul", "Mind", "Spirit"
        ]
        
        self.alignments = [
            "Benevolent", "Malevolent", "Neutral", "Forgotten", "Ascended",
            "Fallen", "Hidden", "Lost", "Ancient", "Young", "Wise", "Mad",
            "Pure", "Corrupted", "Balanced", "Extreme", "Gentle", "Fierce",
            "Patient", "Hasty", "Kind", "Cruel", "Just", "Chaotic"
        ]
        
        # Generated content cache
        self.generated_job_classes: Dict[str, GeneratedJobClass] = {}
        self.generated_weapons: Dict[str, GeneratedWeapon] = {}
        self.generated_beasts: Dict[str, GeneratedBeast] = {}
        self.generated_divine_entities: Dict[str, GeneratedDivineEntity] = {}
        
    def generate_job_class(self, role: str = None, element: str = None, theme: str = None) -> GeneratedJobClass:
        """Generate a unique job class using the formula: [Element] [Theme] [Role]"""
        
        # Use provided components or select random ones
        selected_role = role or random.choice(self.roles)
        selected_element = element or random.choice(self.elements)
        selected_theme = theme or random.choice(self.themes)
        
        # Create unique class name
        class_name = f"{selected_element} {selected_theme} {selected_role}"
        class_id = f"class_{selected_element.lower()}_{selected_theme.lower()}_{selected_role.lower()}"
        
        # Determine rarity based on component combinations
        rarity = self._calculate_job_class_rarity(selected_element, selected_theme, selected_role)
        
        # Generate description
        description = self._generate_job_class_description(selected_element, selected_theme, selected_role)
        
        # Generate abilities based on components
        abilities = self._generate_job_class_abilities(selected_element, selected_theme, selected_role)
        
        # Generate stat bonuses
        stat_bonuses = self._generate_job_class_stats(selected_element, selected_theme, selected_role)
        
        # Generate requirements
        requirements = self._generate_job_class_requirements(rarity, selected_element, selected_theme)
        
        job_class = GeneratedJobClass(
            class_id=class_id,
            name=class_name,
            role=selected_role,
            element=selected_element,
            theme=selected_theme,
            description=description,
            rarity=rarity,
            abilities=abilities,
            stat_bonuses=stat_bonuses,
            requirements=requirements
        )
        
        self.generated_job_classes[class_id] = job_class
        return job_class
    
    def generate_weapon(self, weapon_type: str = None, material: str = None, enchantment: str = None) -> GeneratedWeapon:
        """Generate a unique weapon using the formula: [Enchantment] [Material] [Type]"""
        
        selected_type = weapon_type or random.choice(self.weapon_types)
        selected_material = material or random.choice(self.materials)
        selected_enchantment = enchantment or random.choice(self.enchantments)
        
        weapon_name = f"{selected_enchantment} {selected_material} {selected_type}"
        weapon_id = f"weapon_{selected_enchantment.lower()}_{selected_material.lower()}_{selected_type.lower()}"
        
        rarity = self._calculate_weapon_rarity(selected_enchantment, selected_material, selected_type)
        description = self._generate_weapon_description(selected_enchantment, selected_material, selected_type)
        damage_range = self._calculate_weapon_damage(selected_material, selected_type, rarity)
        special_effects = self._generate_weapon_effects(selected_enchantment, selected_material)
        requirements = self._generate_weapon_requirements(rarity, selected_material)
        
        weapon = GeneratedWeapon(
            weapon_id=weapon_id,
            name=weapon_name,
            weapon_type=selected_type,
            material=selected_material,
            enchantment=selected_enchantment,
            description=description,
            rarity=rarity,
            damage_range=damage_range,
            special_effects=special_effects,
            requirements=requirements
        )
        
        self.generated_weapons[weapon_id] = weapon
        return weapon
    
    def generate_beast(self, base_creature: str = None, modifier: str = None, origin: str = None) -> GeneratedBeast:
        """Generate a unique beast using the formula: [Modifier] [Base Creature] of the [Origin]"""
        
        selected_creature = base_creature or random.choice(self.base_creatures)
        selected_modifier = modifier or random.choice(self.creature_modifiers)
        selected_origin = origin or random.choice(self.origins)
        
        beast_name = f"{selected_modifier} {selected_creature} of the {selected_origin}"
        beast_id = f"beast_{selected_modifier.lower()}_{selected_creature.lower()}_{selected_origin.lower()}"
        
        rarity = self._calculate_beast_rarity(selected_modifier, selected_creature, selected_origin)
        description = self._generate_beast_description(selected_modifier, selected_creature, selected_origin)
        abilities = self._generate_beast_abilities(selected_modifier, selected_creature, selected_origin)
        stats = self._generate_beast_stats(selected_creature, selected_origin, rarity)
        taming_difficulty = self._calculate_taming_difficulty(rarity, selected_origin)
        
        beast = GeneratedBeast(
            beast_id=beast_id,
            name=beast_name,
            base_creature=selected_creature,
            modifier=selected_modifier,
            origin=selected_origin,
            description=description,
            rarity=rarity,
            abilities=abilities,
            stats=stats,
            taming_difficulty=taming_difficulty
        )
        
        self.generated_beasts[beast_id] = beast
        return beast
    
    def generate_divine_entity(self, domain: str = None, form: str = None, alignment: str = None) -> GeneratedDivineEntity:
        """Generate a unique divine entity using the formula: [Form] of [Domain] the [Alignment]"""
        
        selected_domain = domain or random.choice(self.domains)
        selected_form = form or random.choice(self.divine_forms)
        selected_alignment = alignment or random.choice(self.alignments)
        
        entity_name = f"{selected_form} of {selected_domain} the {selected_alignment}"
        entity_id = f"divine_{selected_form.lower()}_{selected_domain.lower()}_{selected_alignment.lower()}"
        
        rarity = self._calculate_divine_rarity(selected_domain, selected_form, selected_alignment)
        description = self._generate_divine_description(selected_domain, selected_form, selected_alignment)
        powers = self._generate_divine_powers(selected_domain, selected_form, selected_alignment)
        favor_requirements = self._generate_favor_requirements(selected_domain, selected_alignment)
        
        entity = GeneratedDivineEntity(
            entity_id=entity_id,
            name=entity_name,
            domain=selected_domain,
            form=selected_form,
            alignment=selected_alignment,
            description=description,
            rarity=rarity,
            powers=powers,
            favor_requirements=favor_requirements
        )
        
        self.generated_divine_entities[entity_id] = entity
        return entity
    
    def _calculate_job_class_rarity(self, element: str, theme: str, role: str) -> ContentRarity:
        """Calculate rarity based on component combinations"""
        rare_elements = ["Void", "Cosmic", "Temporal", "Divine", "Infernal"]
        rare_themes = ["Time", "Dreams", "Chaos", "Fate", "Madness", "Eclipse"]
        rare_roles = ["Exotic", "Shadowmancer", "Oracle", "Bladedancer"]
        
        rarity_score = 0
        if element in rare_elements:
            rarity_score += 2
        if theme in rare_themes:
            rarity_score += 2
        if role in rare_roles:
            rarity_score += 2
        
        rarity_map = {
            0: ContentRarity.COMMON,
            1: ContentRarity.UNCOMMON,
            2: ContentRarity.RARE,
            3: ContentRarity.EPIC,
            4: ContentRarity.LEGENDARY,
            5: ContentRarity.MYTHICAL,
            6: ContentRarity.DIVINE
        }
        
        return rarity_map.get(rarity_score, ContentRarity.COMMON)
    
    def _generate_job_class_description(self, element: str, theme: str, role: str) -> str:
        """Generate flavorful description for job class"""
        descriptions = {
            "Warrior": f"A fierce {role.lower()} who harnesses the power of {element.lower()} through {theme.lower()}",
            "Mage": f"A wise {role.lower()} who weaves {element.lower()} magic with the essence of {theme.lower()}",
            "Rogue": f"A cunning {role.lower()} who strikes from the shadows using {element.lower()} and {theme.lower()}",
            "Cleric": f"A devout {role.lower()} blessed with {element.lower()} powers through {theme.lower()}"
        }
        
        base_desc = descriptions.get(role, f"A master of {element.lower()} who embodies the spirit of {theme.lower()}")
        return f"{base_desc}. Known for their unique combination of elemental mastery and thematic focus."
    
    def _generate_job_class_abilities(self, element: str, theme: str, role: str) -> List[str]:
        """Generate abilities based on components"""
        abilities = []
        
        # Element-based abilities
        element_abilities = {
            "Fire": f"{element} Burst", "Ice": f"{element} Shield", "Lightning": f"{element} Strike",
            "Shadow": f"{element} Step", "Light": f"{element} Heal", "Void": f"{element} Drain"
        }
        abilities.append(element_abilities.get(element, f"{element} Mastery"))
        
        # Theme-based abilities
        theme_abilities = {
            "Time": "Temporal Shift", "Dreams": "Dream Walk", "Blood": "Blood Pact",
            "Chaos": "Chaos Storm", "Nature": "Nature's Call", "Stars": "Stellar Guidance"
        }
        abilities.append(theme_abilities.get(theme, f"{theme} Focus"))
        
        # Role-based abilities
        role_abilities = {
            "Warrior": "Combat Mastery", "Mage": "Spell Weaving", "Rogue": "Stealth Strike",
            "Cleric": "Divine Blessing", "Ranger": "Beast Bond", "Artisan": "Master Craft"
        }
        abilities.append(role_abilities.get(role, f"{role} Expertise"))
        
        # Ultimate combination ability
        abilities.append(f"Ultimate {element} {theme} Technique")
        
        return abilities
    
    def _generate_job_class_stats(self, element: str, theme: str, role: str) -> Dict[str, int]:
        """Generate stat bonuses based on components"""
        stats = {"strength": 0, "magic": 0, "agility": 0, "vitality": 0, "wisdom": 0}
        
        # Role-based stat focus
        role_stats = {
            "Warrior": {"strength": 15, "vitality": 10},
            "Mage": {"magic": 15, "wisdom": 10},
            "Rogue": {"agility": 15, "magic": 5},
            "Cleric": {"wisdom": 15, "vitality": 5}
        }
        
        base_stats = role_stats.get(role, {"strength": 5, "magic": 5, "agility": 5})
        for stat, value in base_stats.items():
            stats[stat] += value
        
        # Element bonuses
        if element in ["Fire", "Lightning"]:
            stats["magic"] += 5
        elif element in ["Earth", "Metal"]:
            stats["vitality"] += 5
        
        return stats
    
    def _generate_job_class_requirements(self, rarity: ContentRarity, element: str, theme: str) -> Dict[str, Any]:
        """Generate requirements for accessing the job class"""
        requirements = {"min_level": 1}
        
        rarity_levels = {
            ContentRarity.COMMON: 1,
            ContentRarity.UNCOMMON: 10,
            ContentRarity.RARE: 25,
            ContentRarity.EPIC: 50,
            ContentRarity.LEGENDARY: 75,
            ContentRarity.MYTHICAL: 90,
            ContentRarity.DIVINE: 100
        }
        
        requirements["min_level"] = rarity_levels[rarity]
        
        if rarity.value in ["epic", "legendary", "mythical", "divine"]:
            requirements["special_quest"] = f"Complete the Trial of {element} {theme}"
        
        return requirements
    
    # Similar methods for weapons, beasts, and divine entities...
    def _calculate_weapon_rarity(self, enchantment: str, material: str, weapon_type: str) -> ContentRarity:
        """Calculate weapon rarity"""
        rare_materials = ["Ether", "Void", "Star", "Soul", "Dream", "Time"]
        rare_enchantments = ["Screaming", "Whispering", "Eternal", "Ancient"]
        
        rarity_score = 0
        if material in rare_materials:
            rarity_score += 2
        if enchantment in rare_enchantments:
            rarity_score += 1
        
        return [ContentRarity.COMMON, ContentRarity.UNCOMMON, ContentRarity.RARE, 
                ContentRarity.EPIC, ContentRarity.LEGENDARY][min(rarity_score, 4)]
    
    def _generate_weapon_description(self, enchantment: str, material: str, weapon_type: str) -> str:
        return f"A {enchantment.lower()} {weapon_type.lower()} forged from pure {material.lower()}. This weapon pulses with otherworldly energy."
    
    def _calculate_weapon_damage(self, material: str, weapon_type: str, rarity: ContentRarity) -> Tuple[int, int]:
        base_damage = {"Sword": 20, "Staff": 15, "Bow": 18, "Dagger": 12}.get(weapon_type, 15)
        material_multiplier = {"Crystal": 1.5, "Ether": 2.0, "Void": 2.5}.get(material, 1.0)
        rarity_multiplier = {
            ContentRarity.COMMON: 1.0, ContentRarity.RARE: 1.5, ContentRarity.LEGENDARY: 2.0
        }.get(rarity, 1.0)
        
        min_damage = int(base_damage * material_multiplier * rarity_multiplier)
        max_damage = int(min_damage * 1.8)
        return (min_damage, max_damage)
    
    def _generate_weapon_effects(self, enchantment: str, material: str) -> List[str]:
        effects = []
        
        enchantment_effects = {
            "Burning": "Deals fire damage over time",
            "Frozen": "Has chance to freeze enemies",
            "Screaming": "Causes fear in enemies",
            "Whispering": "Reveals enemy weaknesses"
        }
        effects.append(enchantment_effects.get(enchantment, f"{enchantment} effect"))
        
        material_effects = {
            "Crystal": "Amplifies magical abilities",
            "Ether": "Phases through armor",
            "Void": "Drains enemy life force"
        }
        if material in material_effects:
            effects.append(material_effects[material])
        
        return effects
    
    def _generate_weapon_requirements(self, rarity: ContentRarity, material: str) -> Dict[str, Any]:
        requirements = {"min_level": 1}
        
        if rarity in [ContentRarity.LEGENDARY, ContentRarity.MYTHICAL]:
            requirements["special_material"] = f"Rare {material} essence"
        
        return requirements
    
    # Beast generation methods
    def _calculate_beast_rarity(self, modifier: str, creature: str, origin: str) -> ContentRarity:
        legendary_creatures = ["Dragon", "Phoenix", "Leviathan", "Kraken", "Sphinx"]
        mythical_origins = ["Divine", "Infernal", "Temporal", "Astral"]
        
        rarity_score = 0
        if creature in legendary_creatures:
            rarity_score += 2
        if origin in mythical_origins:
            rarity_score += 2
        if "void" in modifier.lower() or "dream" in modifier.lower():
            rarity_score += 1
        
        return [ContentRarity.COMMON, ContentRarity.UNCOMMON, ContentRarity.RARE,
                ContentRarity.EPIC, ContentRarity.LEGENDARY][min(rarity_score, 4)]
    
    def _generate_beast_description(self, modifier: str, creature: str, origin: str) -> str:
        return f"A magnificent {creature.lower()} with {modifier.lower()} characteristics, born from the {origin.lower()} realm. Its presence commands both fear and respect."
    
    def _generate_beast_abilities(self, modifier: str, creature: str, origin: str) -> List[str]:
        abilities = []
        
        # Creature base abilities
        creature_abilities = {
            "Dragon": ["Fire Breath", "Flight", "Ancient Wisdom"],
            "Wolf": ["Pack Hunt", "Howl", "Tracking"],
            "Phoenix": ["Rebirth", "Healing Flames", "Flight"]
        }
        abilities.extend(creature_abilities.get(creature, [f"{creature} Instinct"]))
        
        # Modifier abilities
        modifier_abilities = {
            "Flamehowl": "Flame Roar",
            "Frostfang": "Ice Bite", 
            "Voidmaw": "Void Drain"
        }
        if modifier in modifier_abilities:
            abilities.append(modifier_abilities[modifier])
        
        return abilities
    
    def _generate_beast_stats(self, creature: str, origin: str, rarity: ContentRarity) -> Dict[str, int]:
        base_stats = {
            "Dragon": {"strength": 80, "magic": 70, "vitality": 90},
            "Wolf": {"strength": 50, "agility": 70, "vitality": 60},
            "Phoenix": {"magic": 85, "agility": 60, "vitality": 70}
        }
        
        stats = base_stats.get(creature, {"strength": 40, "magic": 40, "vitality": 40})
        
        # Origin bonuses
        origin_bonuses = {
            "Divine": {"magic": 20, "vitality": 15},
            "Abyssal": {"strength": 20, "magic": 10},
            "Celestial": {"magic": 15, "vitality": 15}
        }
        
        if origin in origin_bonuses:
            for stat, bonus in origin_bonuses[origin].items():
                stats[stat] = stats.get(stat, 0) + bonus
        
        return stats
    
    def _calculate_taming_difficulty(self, rarity: ContentRarity, origin: str) -> int:
        base_difficulty = {
            ContentRarity.COMMON: 20,
            ContentRarity.UNCOMMON: 35,
            ContentRarity.RARE: 50,
            ContentRarity.EPIC: 70,
            ContentRarity.LEGENDARY: 85
        }.get(rarity, 50)
        
        # Origin modifiers
        if origin in ["Divine", "Infernal"]:
            base_difficulty += 20
        elif origin in ["Abyssal", "Temporal"]:
            base_difficulty += 15
        
        return min(base_difficulty, 100)
    
    # Divine entity generation methods
    def _calculate_divine_rarity(self, domain: str, form: str, alignment: str) -> ContentRarity:
        major_domains = ["Time", "War", "Death", "Life", "Chaos"]
        powerful_forms = ["Crown", "Eye", "Void", "Heart"]
        
        rarity_score = 0
        if domain in major_domains:
            rarity_score += 2
        if form in powerful_forms:
            rarity_score += 1
        if alignment in ["Ascended", "Fallen"]:
            rarity_score += 1
        
        return [ContentRarity.RARE, ContentRarity.EPIC, ContentRarity.LEGENDARY,
                ContentRarity.MYTHICAL, ContentRarity.DIVINE][min(rarity_score, 4)]
    
    def _generate_divine_description(self, domain: str, form: str, alignment: str) -> str:
        return f"The {alignment.lower()} {form.lower()} that governs {domain.lower()}. Ancient beyond mortal comprehension, this entity shapes reality itself."
    
    def _generate_divine_powers(self, domain: str, form: str, alignment: str) -> List[str]:
        powers = []
        
        domain_powers = {
            "Time": ["Temporal Manipulation", "Age Control", "Future Sight"],
            "War": ["Battle Fury", "Weapon Blessing", "Victory Assurance"],
            "Dreams": ["Dream Walking", "Nightmare Creation", "Sleep Command"]
        }
        powers.extend(domain_powers.get(domain, [f"{domain} Mastery"]))
        
        form_powers = {
            "Crown": "Divine Authority",
            "Eye": "All-Seeing Vision",
            "Flame": "Purifying Fire"
        }
        if form in form_powers:
            powers.append(form_powers[form])
        
        return powers
    
    def _generate_favor_requirements(self, domain: str, alignment: str) -> List[str]:
        requirements = []
        
        domain_requirements = {
            "War": ["Win 100 battles", "Protect allies in combat"],
            "Wisdom": ["Study ancient texts", "Teach others"],
            "Nature": ["Protect forests", "Tame wild beasts"]
        }
        requirements.extend(domain_requirements.get(domain, [f"Master {domain.lower()}"]))
        
        if alignment == "Benevolent":
            requirements.append("Maintain high karma")
        elif alignment == "Malevolent":
            requirements.append("Embrace corruption")
        
        return requirements
    
    def generate_bulk_content(self, job_classes: int = 100, weapons: int = 100, 
                            beasts: int = 100, divine_entities: int = 50) -> Dict[str, int]:
        """Generate bulk content for the game"""
        
        generated_counts = {"job_classes": 0, "weapons": 0, "beasts": 0, "divine_entities": 0}
        
        # Generate job classes
        for _ in range(job_classes):
            self.generate_job_class()
            generated_counts["job_classes"] += 1
        
        # Generate weapons
        for _ in range(weapons):
            self.generate_weapon()
            generated_counts["weapons"] += 1
        
        # Generate beasts
        for _ in range(beasts):
            self.generate_beast()
            generated_counts["beasts"] += 1
        
        # Generate divine entities
        for _ in range(divine_entities):
            self.generate_divine_entity()
            generated_counts["divine_entities"] += 1
        
        return generated_counts
    
    def get_content_by_rarity(self, content_type: str, rarity: ContentRarity) -> List[Any]:
        """Get all content of specific type and rarity"""
        
        content_maps = {
            "job_classes": self.generated_job_classes,
            "weapons": self.generated_weapons,
            "beasts": self.generated_beasts,
            "divine_entities": self.generated_divine_entities
        }
        
        if content_type not in content_maps:
            return []
        
        content_dict = content_maps[content_type]
        return [item for item in content_dict.values() if item.rarity == rarity]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics"""
        return {
            "total_job_classes": len(self.generated_job_classes),
            "total_weapons": len(self.generated_weapons),
            "total_beasts": len(self.generated_beasts),
            "total_divine_entities": len(self.generated_divine_entities),
            "total_content": (len(self.generated_job_classes) + len(self.generated_weapons) + 
                            len(self.generated_beasts) + len(self.generated_divine_entities)),
            "potential_combinations": {
                "job_classes": len(self.roles) * len(self.elements) * len(self.themes),
                "weapons": len(self.weapon_types) * len(self.materials) * len(self.enchantments),
                "beasts": len(self.base_creatures) * len(self.creature_modifiers) * len(self.origins),
                "divine_entities": len(self.domains) * len(self.divine_forms) * len(self.alignments)
            }
        }

# Test the procedural generator
def test_procedural_generator():
    """Test the procedural generation system"""
    generator = ProceduralGenerator()
    
    print("=== PROCEDURAL GENERATION TEST ===\n")
    
    # Test job class generation
    print("1. Testing Job Class Generation...")
    job_class = generator.generate_job_class()
    print(f"Generated: {job_class.name}")
    print(f"Description: {job_class.description}")
    print(f"Rarity: {job_class.rarity.value}")
    print(f"Abilities: {job_class.abilities}")
    
    # Test weapon generation
    print("\n2. Testing Weapon Generation...")
    weapon = generator.generate_weapon()
    print(f"Generated: {weapon.name}")
    print(f"Description: {weapon.description}")
    print(f"Damage: {weapon.damage_range}")
    print(f"Effects: {weapon.special_effects}")
    
    # Test beast generation
    print("\n3. Testing Beast Generation...")
    beast = generator.generate_beast()
    print(f"Generated: {beast.name}")
    print(f"Description: {beast.description}")
    print(f"Abilities: {beast.abilities}")
    print(f"Taming Difficulty: {beast.taming_difficulty}")
    
    # Test divine entity generation
    print("\n4. Testing Divine Entity Generation...")
    divine = generator.generate_divine_entity()
    print(f"Generated: {divine.name}")
    print(f"Description: {divine.description}")
    print(f"Powers: {divine.powers}")
    
    # Test bulk generation
    print("\n5. Testing Bulk Generation...")
    counts = generator.generate_bulk_content(50, 50, 50, 25)
    print(f"Generated content: {counts}")
    
    # Show statistics
    print("\n6. Generation Statistics...")
    stats = generator.get_statistics()
    print(f"Total content generated: {stats['total_content']}")
    print(f"Potential combinations: {stats['potential_combinations']}")

if __name__ == "__main__":
    test_procedural_generator()