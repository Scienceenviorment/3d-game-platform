#!/usr/bin/env python3
"""
Comprehensive Crafting and Production System
Includes alchemy, brewing, farming, agriculture, and resource management
Based on the Beast Taming: Classic of Mountains and Seas universe
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta


class ResourceType(Enum):
    """Types of resources in the game"""
    # Natural Resources
    HERB = "herb"
    MINERAL = "mineral"
    WOOD = "wood"
    STONE = "stone"
    WATER = "water"
    
    # Beast Resources
    BEAST_PART = "beast_part"
    DIVINE_ESSENCE = "divine_essence"
    SPIRITUAL_ENERGY = "spiritual_energy"
    
    # Agricultural
    CROP = "crop"
    SEED = "seed"
    LIVESTOCK = "livestock"
    
    # Crafted Materials
    METAL = "metal"
    POTION = "potion"
    TOOL = "tool"
    WEAPON = "weapon"
    ARMOR = "armor"
    
    # Mystical
    RUNE = "rune"
    TALISMAN = "talisman"
    SCROLL = "scroll"


class CraftingSkill(Enum):
    """Crafting skills players can develop"""
    ALCHEMY = "alchemy"           # Potions and transmutation
    BREWING = "brewing"           # Beverages and elixirs
    BLACKSMITHING = "blacksmithing"  # Weapons and tools
    TAILORING = "tailoring"       # Armor and clothing
    WOODWORKING = "woodworking"   # Furniture and tools
    COOKING = "cooking"           # Food and recipes
    FARMING = "farming"           # Crops and agriculture
    ANIMAL_HUSBANDRY = "animal_husbandry"  # Livestock and beasts
    HERBALISM = "herbalism"       # Plant knowledge and gathering
    MINING = "mining"             # Ore and mineral extraction
    ENCHANTING = "enchanting"     # Magical enhancements
    INSCRIPTION = "inscription"   # Scrolls and runes


class RecipeRarity(Enum):
    """Rarity levels for crafting recipes"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHICAL = "mythical"
    DIVINE = "divine"             # Require divine intervention


@dataclass
class Resource:
    """A harvestable or craftable resource"""
    resource_id: str
    name: str
    description: str
    resource_type: ResourceType
    rarity: RecipeRarity
    
    # Gathering information
    gathering_skill: Optional[CraftingSkill] = None
    gathering_difficulty: int = 1  # 1-10
    gathering_time_minutes: int = 5
    gathering_yield: Tuple[int, int] = (1, 3)  # Min, max yield
    
    # Location and availability
    found_in_regions: List[str] = field(default_factory=list)
    seasonal_availability: List[str] = field(default_factory=list)  # seasons when available
    respawn_time_hours: int = 24
    
    # Properties
    base_value: int = 1
    stack_size: int = 100
    properties: List[str] = field(default_factory=list)  # "poisonous", "healing", etc.
    
    # Beast-related
    source_beast: Optional[str] = None
    requires_tamed_beast: bool = False


@dataclass
class CraftingRecipe:
    """A recipe for creating items"""
    recipe_id: str
    name: str
    description: str
    crafting_skill: CraftingSkill
    skill_level_required: int
    rarity: RecipeRarity
    result_item: str  # Moved up before default fields
    
    # Ingredients
    ingredients: Dict[str, int] = field(default_factory=dict)  # resource_id: quantity
    
    # Crafting process
    crafting_time_minutes: int = 30
    energy_cost: int = 20
    success_rate: float = 0.8
    
    # Equipment requirements
    required_tools: List[str] = field(default_factory=list)
    required_station: Optional[str] = None  # "alchemy_lab", "forge", etc.
    
    # Output
    result_quantity: Tuple[int, int] = (1, 1)  # Min, max output
    experience_gained: int = 10
    
    # Special requirements
    moon_phase_required: Optional[str] = None
    time_of_day_required: Optional[str] = None
    location_requirement: Optional[str] = None
    beast_assistance: Optional[str] = None  # Beast that must help
    
    # Failure consequences
    failure_effects: List[str] = field(default_factory=list)
    
    # Discovery method
    discovery_method: str = "Known"  # How players learn this recipe
    hidden_recipe: bool = False


@dataclass
class CraftingStation:
    """A crafting station where players create items"""
    station_id: str
    name: str
    description: str
    supported_skills: List[CraftingSkill]
    
    # Construction requirements
    construction_materials: Dict[str, int] = field(default_factory=dict)
    construction_time_hours: int = 4
    construction_skill_required: Optional[CraftingSkill] = None
    construction_skill_level: int = 1
    
    # Functionality
    efficiency_bonus: float = 1.0  # Multiplier for crafting speed
    quality_bonus: float = 1.0     # Multiplier for success rate
    special_abilities: List[str] = field(default_factory=list)
    
    # Maintenance
    daily_maintenance_cost: Dict[str, int] = field(default_factory=dict)
    durability: int = 100
    max_durability: int = 100


@dataclass
class Farm:
    """A player's farm for growing crops and raising animals"""
    farm_id: str
    owner_id: str
    location: str
    
    # Farm properties
    size_plots: int = 4            # Number of crop plots
    soil_quality: float = 1.0      # Multiplier for crop yield
    water_access: bool = True
    
    # Plots and crops
    crop_plots: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    # Livestock
    animals: Dict[str, int] = field(default_factory=dict)  # animal_type: count
    animal_happiness: Dict[str, float] = field(default_factory=dict)
    
    # Infrastructure
    buildings: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    
    # Resources
    stored_resources: Dict[str, int] = field(default_factory=dict)
    
    # Farm level and upgrades
    farm_level: int = 1
    experience: int = 0


@dataclass
class CraftingProgress:
    """Player's crafting skill progression"""
    player_id: str
    
    # Skill levels (0-100 for each skill)
    skill_levels: Dict[CraftingSkill, int] = field(default_factory=dict)
    skill_experience: Dict[CraftingSkill, int] = field(default_factory=dict)
    
    # Known recipes
    known_recipes: List[str] = field(default_factory=list)
    discovered_recipes: List[str] = field(default_factory=list)  # Player discovered these
    
    # Crafting achievements
    items_crafted: Dict[str, int] = field(default_factory=dict)  # item_id: count
    legendary_items_crafted: int = 0
    failed_attempts: Dict[str, int] = field(default_factory=dict)
    
    # Active projects
    active_crafting: Dict[str, datetime] = field(default_factory=dict)  # recipe_id: completion_time
    
    # Specializations
    mastery_bonuses: Dict[CraftingSkill, float] = field(default_factory=dict)
    
    # Farms owned
    farms: List[str] = field(default_factory=list)  # farm_ids


class CraftingSystem:
    """Manages all crafting, farming, and production activities"""
    
    def __init__(self):
        self.resources = self._initialize_resources()
        self.recipes = self._initialize_recipes()
        self.crafting_stations = self._initialize_stations()
        self.player_progress = {}
        self.farms = {}
    
    def _initialize_resources(self) -> Dict[str, Resource]:
        """Initialize all game resources"""
        resources = {}
        
        # Sacred herbs from Indian tradition
        resources["tulsi"] = Resource(
            resource_id="tulsi",
            name="Sacred Tulsi",
            description="Holy basil, sacred to Vishnu, powerful in healing",
            resource_type=ResourceType.HERB,
            rarity=RecipeRarity.UNCOMMON,
            gathering_skill=CraftingSkill.HERBALISM,
            gathering_difficulty=3,
            gathering_time_minutes=10,
            gathering_yield=(2, 5),
            found_in_regions=["Sacred Grove", "Temple Gardens"],
            seasonal_availability=["spring", "summer"],
            base_value=15,
            properties=["healing", "purification", "divine_blessing"]
        )
        
        resources["ashwagandha"] = Resource(
            resource_id="ashwagandha",
            name="Ashwagandha Root",
            description="Ancient root that grants strength and vitality",
            resource_type=ResourceType.HERB,
            rarity=RecipeRarity.RARE,
            gathering_skill=CraftingSkill.HERBALISM,
            gathering_difficulty=5,
            gathering_time_minutes=20,
            gathering_yield=(1, 3),
            found_in_regions=["Mountain Slopes", "Ancient Forest"],
            seasonal_availability=["autumn"],
            base_value=30,
            properties=["strength_boost", "stamina_recovery", "stress_relief"]
        )
        
        # Divine beast materials
        resources["garuda_feather"] = Resource(
            resource_id="garuda_feather",
            name="Garuda's Golden Feather",
            description="A feather from the divine eagle, radiates celestial power",
            resource_type=ResourceType.BEAST_PART,
            rarity=RecipeRarity.LEGENDARY,
            gathering_skill=None,  # Cannot be gathered normally
            source_beast="garuda",
            requires_tamed_beast=True,
            base_value=500,
            properties=["flight_enhancement", "divine_protection", "wind_control"]
        )
        
        resources["naga_scale"] = Resource(
            resource_id="naga_scale",
            name="Naga King's Scale",
            description="Iridescent scale from an ancient serpent king",
            resource_type=ResourceType.BEAST_PART,
            rarity=RecipeRarity.EPIC,
            source_beast="naga",
            requires_tamed_beast=True,
            base_value=200,
            properties=["water_breathing", "poison_immunity", "treasure_sense"]
        )
        
        # Crops and agriculture
        resources["sacred_rice"] = Resource(
            resource_id="sacred_rice",
            name="Sacred Basmati Rice",
            description="Rice blessed by Lakshmi, brings prosperity",
            resource_type=ResourceType.CROP,
            rarity=RecipeRarity.COMMON,
            gathering_skill=CraftingSkill.FARMING,
            gathering_difficulty=2,
            gathering_time_minutes=60,  # Longer for crops
            gathering_yield=(10, 20),
            seasonal_availability=["monsoon", "autumn"],
            base_value=2,
            properties=["nourishing", "prosperity_blessing"]
        )
        
        # Minerals and gems
        resources["rudraksha_seed"] = Resource(
            resource_id="rudraksha_seed",
            name="Rudraksha Seed",
            description="Sacred seed of Shiva, powerful for meditation and protection",
            resource_type=ResourceType.MINERAL,
            rarity=RecipeRarity.RARE,
            gathering_skill=CraftingSkill.HERBALISM,
            gathering_difficulty=6,
            found_in_regions=["Himalayan Foothills", "Sacred Forest"],
            base_value=100,
            properties=["spiritual_power", "protection", "meditation_enhancement"]
        )
        
        return resources
    
    def _initialize_recipes(self) -> Dict[str, CraftingRecipe]:
        """Initialize all crafting recipes"""
        recipes = {}
        
        # Healing Potion - Basic Alchemy
        recipes["healing_potion"] = CraftingRecipe(
            recipe_id="healing_potion",
            name="Ayurvedic Healing Potion",
            description="Traditional healing potion using sacred herbs",
            crafting_skill=CraftingSkill.ALCHEMY,
            skill_level_required=5,
            rarity=RecipeRarity.COMMON,
            ingredients={
                "tulsi": 3,
                "sacred_water": 1,
                "honey": 2
            },
            crafting_time_minutes=30,
            energy_cost=15,
            success_rate=0.85,
            required_tools=["mortar_pestle", "glass_vial"],
            required_station="alchemy_lab",
            result_item="healing_potion",
            result_quantity=(1, 2),
            experience_gained=15
        )
        
        # Divine Flight Elixir - Advanced Recipe
        recipes["flight_elixir"] = CraftingRecipe(
            recipe_id="flight_elixir",
            name="Elixir of Divine Flight",
            description="Grants temporary flight using Garuda's essence",
            crafting_skill=CraftingSkill.ALCHEMY,
            skill_level_required=50,
            rarity=RecipeRarity.LEGENDARY,
            ingredients={
                "garuda_feather": 1,
                "sky_lotus": 5,
                "concentrated_wind_essence": 3,
                "sacred_soma": 2
            },
            crafting_time_minutes=180,  # 3 hours
            energy_cost=60,
            success_rate=0.4,  # Very difficult
            required_tools=["divine_cauldron", "sky_crystal"],
            required_station="celestial_laboratory",
            moon_phase_required="full_moon",
            time_of_day_required="dawn",
            beast_assistance="garuda",  # Garuda must help
            result_item="flight_elixir",
            result_quantity=(1, 1),
            experience_gained=200,
            failure_effects=["explosion", "ingredient_loss", "temporary_curse"],
            discovery_method="Divine Revelation",
            hidden_recipe=True
        )
        
        # Sacred Rice Wine - Brewing
        recipes["soma_wine"] = CraftingRecipe(
            recipe_id="soma_wine",
            name="Sacred Soma Wine",
            description="Divine wine that enhances spiritual abilities",
            crafting_skill=CraftingSkill.BREWING,
            skill_level_required=25,
            rarity=RecipeRarity.RARE,
            ingredients={
                "sacred_rice": 20,
                "honey": 5,
                "sacred_yeast": 1,
                "tulsi": 3
            },
            crafting_time_minutes=1440,  # 24 hours fermentation
            energy_cost=30,
            success_rate=0.7,
            required_tools=["fermentation_vessel", "sacred_filter"],
            result_item="soma_wine",
            result_quantity=(3, 5),
            experience_gained=50,
            moon_phase_required="new_moon"  # Best brewed on new moon
        )
        
        # Divine Weapon Forging
        recipes["celestial_sword"] = CraftingRecipe(
            recipe_id="celestial_sword",
            name="Sword of Celestial Fire",
            description="A weapon forged with divine fire and blessed metals",
            crafting_skill=CraftingSkill.BLACKSMITHING,
            skill_level_required=70,
            rarity=RecipeRarity.MYTHICAL,
            ingredients={
                "divine_steel": 10,
                "phoenix_flame_essence": 3,
                "blessed_handle_wood": 1,
                "star_metal": 5
            },
            crafting_time_minutes=480,  # 8 hours
            energy_cost=80,
            success_rate=0.3,
            required_tools=["divine_forge", "celestial_hammer"],
            required_station="heavenly_smithy",
            beast_assistance="phoenix",  # Phoenix must provide flame
            result_item="celestial_sword",
            experience_gained=500,
            failure_effects=["forge_explosion", "divine_curse", "material_destruction"],
            hidden_recipe=True
        )
        
        return recipes
    
    def _initialize_stations(self) -> Dict[str, CraftingStation]:
        """Initialize crafting stations"""
        stations = {}
        
        stations["alchemy_lab"] = CraftingStation(
            station_id="alchemy_lab",
            name="Ayurvedic Alchemy Laboratory",
            description="A traditional laboratory for preparing potions and elixirs",
            supported_skills=[CraftingSkill.ALCHEMY, CraftingSkill.HERBALISM],
            construction_materials={
                "stone": 50,
                "wood": 30,
                "glass": 20,
                "copper": 10
            },
            construction_time_hours=8,
            construction_skill_required=CraftingSkill.ALCHEMY,
            construction_skill_level=10,
            efficiency_bonus=1.2,
            quality_bonus=1.1,
            special_abilities=["herb_preservation", "essence_extraction"]
        )
        
        stations["divine_forge"] = CraftingStation(
            station_id="divine_forge",
            name="Forge of Celestial Fire",
            description="A forge blessed by Agni, the fire god",
            supported_skills=[CraftingSkill.BLACKSMITHING, CraftingSkill.ENCHANTING],
            construction_materials={
                "divine_stone": 100,
                "sacred_metals": 50,
                "phoenix_essence": 5,
                "fire_crystals": 20
            },
            construction_time_hours=72,  # 3 days
            construction_skill_required=CraftingSkill.BLACKSMITHING,
            construction_skill_level=50,
            efficiency_bonus=2.0,
            quality_bonus=1.5,
            special_abilities=["divine_blessing", "elemental_infusion", "legendary_creation"]
        )
        
        return stations
    
    def attempt_crafting(self, player_id: str, recipe_id: str, 
                        available_materials: Dict[str, int],
                        available_tools: List[str],
                        current_location: str) -> Dict[str, Any]:
        """Attempt to craft an item"""
        if recipe_id not in self.recipes:
            return {"success": False, "reason": "Recipe not found"}
        
        recipe = self.recipes[recipe_id]
        
        # Get player progress
        if player_id not in self.player_progress:
            self.player_progress[player_id] = CraftingProgress(player_id)
        progress = self.player_progress[player_id]
        
        # Check if player knows the recipe
        if recipe_id not in progress.known_recipes and not recipe.hidden_recipe:
            return {"success": False, "reason": "Recipe unknown"}
        
        # Check skill level
        player_skill = progress.skill_levels.get(recipe.crafting_skill, 0)
        if player_skill < recipe.skill_level_required:
            return {
                "success": False, 
                "reason": f"Requires {recipe.crafting_skill.value} level {recipe.skill_level_required}"
            }
        
        # Check ingredients
        missing_ingredients = []
        for ingredient, needed in recipe.ingredients.items():
            if available_materials.get(ingredient, 0) < needed:
                missing_ingredients.append(f"{ingredient} ({needed} needed)")
        
        if missing_ingredients:
            return {"success": False, "reason": f"Missing: {missing_ingredients}"}
        
        # Check tools
        missing_tools = []
        for tool in recipe.required_tools:
            if tool not in available_tools:
                missing_tools.append(tool)
        
        if missing_tools:
            return {"success": False, "reason": f"Missing tools: {missing_tools}"}
        
        # Check crafting station
        if recipe.required_station:
            # Would check if player has access to required station
            pass
        
        # Check special requirements
        special_checks = self._check_special_requirements(recipe)
        if not special_checks["met"]:
            return {"success": False, "reason": special_checks["reason"]}
        
        # Calculate success rate
        base_success = recipe.success_rate
        skill_bonus = (player_skill - recipe.skill_level_required) * 0.01
        mastery_bonus = progress.mastery_bonuses.get(recipe.crafting_skill, 0)
        
        final_success_rate = min(0.95, base_success + skill_bonus + mastery_bonus)
        
        # Attempt crafting
        success = random.random() < final_success_rate
        
        if success:
            # Success - create item
            min_qty, max_qty = recipe.result_quantity
            quantity = random.randint(min_qty, max_qty)
            
            # Award experience
            self._award_crafting_experience(progress, recipe)
            
            # Record success
            progress.items_crafted[recipe.result_item] = progress.items_crafted.get(recipe.result_item, 0) + quantity
            if recipe.rarity in [RecipeRarity.LEGENDARY, RecipeRarity.MYTHICAL, RecipeRarity.DIVINE]:
                progress.legendary_items_crafted += 1
            
            return {
                "success": True,
                "item_created": recipe.result_item,
                "quantity": quantity,
                "experience_gained": recipe.experience_gained,
                "skill_improved": self._check_skill_levelup(progress, recipe.crafting_skill)
            }
        else:
            # Failure
            progress.failed_attempts[recipe_id] = progress.failed_attempts.get(recipe_id, 0) + 1
            
            return {
                "success": False,
                "reason": "Crafting failed",
                "consequences": recipe.failure_effects,
                "experience_gained": recipe.experience_gained // 4  # Small exp for trying
            }
    
    def _check_special_requirements(self, recipe: CraftingRecipe) -> Dict[str, Any]:
        """Check special requirements like moon phase, time, etc."""
        # Simplified - in full game would check actual game state
        if recipe.moon_phase_required:
            # For demo, assume 50% chance the moon phase is correct
            if random.random() < 0.5:
                return {"met": False, "reason": f"Wrong moon phase, need {recipe.moon_phase_required}"}
        
        if recipe.time_of_day_required:
            if random.random() < 0.5:
                return {"met": False, "reason": f"Wrong time, need {recipe.time_of_day_required}"}
        
        if recipe.beast_assistance:
            if random.random() < 0.3:  # 70% chance player has the beast
                return {"met": False, "reason": f"Need {recipe.beast_assistance} to assist"}
        
        return {"met": True}
    
    def _award_crafting_experience(self, progress: CraftingProgress, recipe: CraftingRecipe):
        """Award experience for successful crafting"""
        skill = recipe.crafting_skill
        exp_gained = recipe.experience_gained
        
        progress.skill_experience[skill] = progress.skill_experience.get(skill, 0) + exp_gained
        
        # Check for level up
        current_level = progress.skill_levels.get(skill, 0)
        exp_needed_for_next = (current_level + 1) * 100  # Simple progression
        
        if progress.skill_experience[skill] >= exp_needed_for_next:
            progress.skill_levels[skill] = current_level + 1
            progress.skill_experience[skill] -= exp_needed_for_next
    
    def _check_skill_levelup(self, progress: CraftingProgress, skill: CraftingSkill) -> bool:
        """Check if player leveled up in a skill"""
        # This would be called after awarding experience
        return True  # Simplified
    
    def start_farm(self, player_id: str, location: str) -> Dict[str, Any]:
        """Start a new farm for the player"""
        farm_id = f"farm_{player_id}_{len(self.farms)}"
        
        new_farm = Farm(
            farm_id=farm_id,
            owner_id=player_id,
            location=location
        )
        
        # Initialize crop plots
        for i in range(new_farm.size_plots):
            new_farm.crop_plots[i] = {
                "crop": None,
                "planted_time": None,
                "growth_stage": 0,
                "water_level": 100,
                "health": 100
            }
        
        self.farms[farm_id] = new_farm
        
        # Add to player progress
        if player_id not in self.player_progress:
            self.player_progress[player_id] = CraftingProgress(player_id)
        self.player_progress[player_id].farms.append(farm_id)
        
        return {
            "success": True,
            "farm_id": farm_id,
            "location": location,
            "plots": new_farm.size_plots
        }
    
    def plant_crop(self, farm_id: str, plot_number: int, crop_type: str) -> Dict[str, Any]:
        """Plant a crop in a farm plot"""
        if farm_id not in self.farms:
            return {"success": False, "reason": "Farm not found"}
        
        farm = self.farms[farm_id]
        
        if plot_number not in farm.crop_plots:
            return {"success": False, "reason": "Invalid plot number"}
        
        plot = farm.crop_plots[plot_number]
        
        if plot["crop"] is not None:
            return {"success": False, "reason": "Plot already has a crop"}
        
        # Plant the crop
        plot["crop"] = crop_type
        plot["planted_time"] = datetime.now()
        plot["growth_stage"] = 0
        
        return {
            "success": True,
            "crop_planted": crop_type,
            "plot": plot_number,
            "estimated_harvest": "7 days"  # Simplified
        }
    
    def get_player_crafting_status(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive crafting status for a player"""
        if player_id not in self.player_progress:
            return {"message": "No crafting progress found"}
        
        progress = self.player_progress[player_id]
        
        return {
            "skill_levels": {skill.value: level for skill, level in progress.skill_levels.items()},
            "known_recipes": len(progress.known_recipes),
            "items_crafted": sum(progress.items_crafted.values()),
            "legendary_items": progress.legendary_items_crafted,
            "farms_owned": len(progress.farms),
            "highest_skill": max(progress.skill_levels.values()) if progress.skill_levels else 0,
            "specializations": list(progress.mastery_bonuses.keys())
        }


# Global crafting system instance
crafting_system = CraftingSystem()


def test_crafting_system():
    """Test the crafting system"""
    print("🔨 Testing Comprehensive Crafting System")
    print("=" * 60)
    
    # Test materials available to player
    test_materials = {
        "tulsi": 5,
        "sacred_water": 3,
        "honey": 4,
        "glass_vial": 2
    }
    
    test_tools = ["mortar_pestle", "glass_vial"]
    
    print("📦 Available Materials:")
    for material, qty in test_materials.items():
        print(f"   {material}: {qty}")
    
    print(f"\n🔧 Available Tools: {', '.join(test_tools)}")
    
    print("\n🧪 Attempting to craft Healing Potion...")
    
    # Test crafting
    result = crafting_system.attempt_crafting(
        "test_player", "healing_potion", test_materials, test_tools, "alchemy_lab"
    )
    
    if result["success"]:
        print(f"✅ Successfully crafted: {result['item_created']} x{result['quantity']}")
        print(f"   Experience gained: {result['experience_gained']}")
    else:
        print(f"❌ Crafting failed: {result['reason']}")
    
    # Test farm creation
    print("\n🌾 Creating a farm...")
    farm_result = crafting_system.start_farm("test_player", "Fertile Valley")
    
    if farm_result["success"]:
        print(f"✅ Farm created: {farm_result['farm_id']}")
        print(f"   Location: {farm_result['location']}")
        print(f"   Plots available: {farm_result['plots']}")
        
        # Test planting
        plant_result = crafting_system.plant_crop(farm_result['farm_id'], 0, "sacred_rice")
        if plant_result["success"]:
            print(f"✅ Planted {plant_result['crop_planted']} in plot {plant_result['plot']}")
    
    # Show final status
    print("\n📊 Final Crafting Status:")
    status = crafting_system.get_player_crafting_status("test_player")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Crafting system test completed!")


if __name__ == "__main__":
    test_crafting_system()