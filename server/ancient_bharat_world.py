#!/usr/bin/env python3
"""
Ancient Bharat World Generation
Procedural world generation using Python math and random libraries
"""

import math
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class BiomeType(Enum):
    """Biome types in Ancient Bharat"""
    DUST_PLAINS = "dust_plains"          # Arid desert-like region
    OCEAN_FRONTIER = "ocean_frontier"    # Coastal and ocean areas
    HIMALAYAN_PEAKS = "himalayan_peaks"  # Mountain regions
    NARMADA_FOREST = "narmada_forest"    # Dense forest areas
    INDRAPURA_CITY = "indrapura_city"    # Urban center region


class ObjectType(Enum):
    """Types of world objects"""
    TREE = "tree"                        # Various trees
    ROCK = "rock"                        # Stone formations
    TEMPLE = "temple"                    # Sacred structures
    RUINS = "ruins"                      # Ancient ruins
    WATER = "water"                      # Rivers, ponds
    SETTLEMENT = "settlement"            # Villages, camps
    LANDMARK = "landmark"                # Special locations
    RESOURCE = "resource"                # Collectible items


@dataclass
class WorldPosition:
    """3D position in the world using Python dataclass"""
    x: float                             # X coordinate
    y: float                             # Y coordinate (height)
    z: float                             # Z coordinate
    
    def distance_to(self, other: 'WorldPosition') -> float:
        """Calculate distance to another position"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def distance_2d(self, other: 'WorldPosition') -> float:
        """Calculate 2D distance (ignoring height)"""
        dx = self.x - other.x
        dz = self.z - other.z
        return math.sqrt(dx*dx + dz*dz)


@dataclass
class WorldObject:
    """Individual world object using Python dataclass"""
    object_id: str                       # Unique identifier
    object_type: ObjectType              # Type of object
    position: WorldPosition              # World position
    rotation: float = 0.0                # Y-axis rotation in radians
    scale: float = 1.0                   # Object scale
    biome: BiomeType = BiomeType.DUST_PLAINS  # Which biome it belongs to
    
    # Object properties
    name: str = ""                       # Display name
    description: str = ""                # Description text
    interactable: bool = False           # Can player interact?
    collectible: bool = False            # Can be collected?
    quest_related: bool = False          # Related to quests?
    
    # Visual properties
    model_name: str = ""                 # 3D model filename
    texture_name: str = ""               # Texture filename
    
    # Cultural properties for Ancient Bharat theme
    cultural_significance: str = ""      # Cultural meaning
    sanskrit_name: str = ""              # Sanskrit name
    historical_period: str = ""          # Time period


@dataclass
class WorldChunk:
    """World chunk for efficient loading using Python dataclass"""
    chunk_x: int                         # Chunk X coordinate
    chunk_z: int                         # Chunk Z coordinate
    chunk_size: int = 64                 # Size of chunk in world units
    
    # Chunk contents
    objects: List[WorldObject] = field(default_factory=list)
    terrain_height: Dict[str, float] = field(default_factory=dict)  # Height map
    biome: BiomeType = BiomeType.DUST_PLAINS
    
    # Generation metadata
    generated: bool = False              # Has chunk been generated?
    seed: int = 0                        # Generation seed
    
    def get_world_bounds(self) -> Tuple[float, float, float, float]:
        """Get world boundaries of this chunk"""
        min_x = self.chunk_x * self.chunk_size
        max_x = min_x + self.chunk_size
        min_z = self.chunk_z * self.chunk_size
        max_z = min_z + self.chunk_size
        return min_x, max_x, min_z, max_z
    
    def contains_position(self, x: float, z: float) -> bool:
        """Check if position is within this chunk"""
        min_x, max_x, min_z, max_z = self.get_world_bounds()
        return min_x <= x < max_x and min_z <= z < max_z
    
    def get_height_at(self, x: float, z: float) -> float:
        """Get terrain height at position using interpolation"""
        # Simple grid-based height lookup
        grid_key = f"{int(x)}_{int(z)}"
        return self.terrain_height.get(grid_key, 0.0)


class AncientBharatWorldGenerator:
    """Procedural world generator for Ancient Bharat"""
    
    def __init__(self, world_seed: int = 12345):
        """Initialize world generator"""
        self.world_seed = world_seed         # Master seed for world
        self.chunks: Dict[str, WorldChunk] = {}  # Generated chunks
        
        # Generation parameters
        self.chunk_size = 64                 # Size of each chunk
        self.max_height = 50.0              # Maximum terrain height
        self.terrain_scale = 0.05           # Terrain noise scale
        self.object_density = 0.3           # Objects per chunk area
        
        # Cultural object definitions
        self.cultural_objects = self._define_cultural_objects()
        
        # Biome definitions
        self.biome_configs = self._define_biome_configs()
        
        # Set master random seed
        random.seed(world_seed)
    
    def _define_cultural_objects(self) -> Dict[str, Dict]:
        """Define culturally appropriate objects for Ancient Bharat"""
        return {
            # Sacred structures
            "small_temple": {
                "type": ObjectType.TEMPLE,
                "name": "Small Temple",
                "sanskrit_name": "Mandir",
                "cultural_significance": "Village worship place",
                "model": "temple_small.obj",
                "scale_range": (0.8, 1.2),
                "biomes": [BiomeType.INDRAPURA_CITY, BiomeType.NARMADA_FOREST]
            },
            
            "ancient_stupa": {
                "type": ObjectType.TEMPLE,
                "name": "Ancient Stupa",
                "sanskrit_name": "Stupa",
                "cultural_significance": "Buddhist monument",
                "model": "stupa.obj",
                "scale_range": (1.0, 1.5),
                "biomes": [BiomeType.HIMALAYAN_PEAKS, BiomeType.DUST_PLAINS]
            },
            
            # Natural elements
            "banyan_tree": {
                "type": ObjectType.TREE,
                "name": "Sacred Banyan Tree",
                "sanskrit_name": "Vat Vriksha",
                "cultural_significance": "Tree of wisdom and longevity",
                "model": "banyan_tree.obj",
                "scale_range": (1.2, 2.0),
                "biomes": [BiomeType.NARMADA_FOREST, BiomeType.INDRAPURA_CITY]
            },
            
            "sal_tree": {
                "type": ObjectType.TREE,
                "name": "Sal Tree",
                "sanskrit_name": "Shala Vriksha",
                "cultural_significance": "Sacred tree of strength",
                "model": "sal_tree.obj",
                "scale_range": (0.8, 1.4),
                "biomes": [BiomeType.NARMADA_FOREST, BiomeType.HIMALAYAN_PEAKS]
            },
            
            # Ancient ruins
            "stone_pillar": {
                "type": ObjectType.RUINS,
                "name": "Ancient Stone Pillar",
                "sanskrit_name": "Stambha",
                "cultural_significance": "Royal decree marker",
                "model": "stone_pillar.obj",
                "scale_range": (0.7, 1.3),
                "biomes": [BiomeType.DUST_PLAINS, BiomeType.INDRAPURA_CITY]
            },
            
            "carved_gateway": {
                "type": ObjectType.RUINS,
                "name": "Carved Gateway",
                "sanskrit_name": "Torana",
                "cultural_significance": "Entrance to sacred spaces",
                "model": "gateway.obj",
                "scale_range": (1.0, 1.2),
                "biomes": [BiomeType.INDRAPURA_CITY, BiomeType.NARMADA_FOREST]
            },
            
            # Water features
            "sacred_pond": {
                "type": ObjectType.WATER,
                "name": "Sacred Pond",
                "sanskrit_name": "Pushkarini",
                "cultural_significance": "Ritual bathing place",
                "model": "sacred_pond.obj",
                "scale_range": (1.0, 1.5),
                "biomes": [BiomeType.INDRAPURA_CITY, BiomeType.NARMADA_FOREST]
            },
            
            # Rock formations
            "meditation_stone": {
                "type": ObjectType.ROCK,
                "name": "Meditation Stone",
                "sanskrit_name": "Dhyana Shila",
                "cultural_significance": "Place for contemplation",
                "model": "meditation_stone.obj",
                "scale_range": (0.6, 1.0),
                "biomes": [BiomeType.HIMALAYAN_PEAKS, BiomeType.NARMADA_FOREST]
            }
        }
    
    def _define_biome_configs(self) -> Dict[BiomeType, Dict]:
        """Define biome-specific generation parameters"""
        return {
            BiomeType.DUST_PLAINS: {
                "terrain_roughness": 0.3,
                "base_height": 0.0,
                "height_variation": 15.0,
                "object_types": ["stone_pillar", "ancient_stupa", "meditation_stone"],
                "tree_density": 0.05,
                "cultural_density": 0.2,
                "colors": {"sand": "#D4B896", "rock": "#8B7355"}
            },
            
            BiomeType.OCEAN_FRONTIER: {
                "terrain_roughness": 0.2,
                "base_height": -2.0,
                "height_variation": 8.0,
                "object_types": ["sacred_pond", "meditation_stone"],
                "tree_density": 0.1,
                "cultural_density": 0.15,
                "colors": {"water": "#4A90E2", "sand": "#F5DEB3"}
            },
            
            BiomeType.HIMALAYAN_PEAKS: {
                "terrain_roughness": 0.8,
                "base_height": 20.0,
                "height_variation": 30.0,
                "object_types": ["ancient_stupa", "sal_tree", "meditation_stone"],
                "tree_density": 0.3,
                "cultural_density": 0.1,
                "colors": {"rock": "#7D6B5B", "snow": "#FFFFFF"}
            },
            
            BiomeType.NARMADA_FOREST: {
                "terrain_roughness": 0.4,
                "base_height": 5.0,
                "height_variation": 12.0,
                "object_types": ["banyan_tree", "sal_tree", "small_temple", "carved_gateway", "sacred_pond"],
                "tree_density": 0.7,
                "cultural_density": 0.3,
                "colors": {"grass": "#228B22", "tree": "#006400"}
            },
            
            BiomeType.INDRAPURA_CITY: {
                "terrain_roughness": 0.1,
                "base_height": 8.0,
                "height_variation": 5.0,
                "object_types": ["small_temple", "carved_gateway", "stone_pillar", "banyan_tree", "sacred_pond"],
                "tree_density": 0.2,
                "cultural_density": 0.8,
                "colors": {"stone": "#D2B48C", "building": "#CD853F"}
            }
        }
    
    def determine_biome(self, x: float, z: float) -> BiomeType:
        """Determine biome at world coordinates"""
        # Simple biome determination based on position
        # This matches the regions from our server configuration
        
        if x < -200:  # Western region
            return BiomeType.DUST_PLAINS
        elif x > 200:  # Eastern region
            return BiomeType.OCEAN_FRONTIER
        elif z > 200:  # Northern region
            return BiomeType.HIMALAYAN_PEAKS
        elif z < -100:  # Southern region
            return BiomeType.NARMADA_FOREST
        else:  # Central region
            return BiomeType.INDRAPURA_CITY
    
    def generate_terrain_height(self, x: float, z: float, biome: BiomeType) -> float:
        """Generate terrain height using Perlin-like noise"""
        config = self.biome_configs[biome]
        
        # Simple noise function using sine waves
        # In a real implementation, you'd use proper Perlin noise
        noise1 = math.sin(x * self.terrain_scale) * math.cos(z * self.terrain_scale)
        noise2 = math.sin(x * self.terrain_scale * 2) * math.cos(z * self.terrain_scale * 2) * 0.5
        noise3 = math.sin(x * self.terrain_scale * 4) * math.cos(z * self.terrain_scale * 4) * 0.25
        
        # Combine noise layers
        combined_noise = (noise1 + noise2 + noise3) * config["terrain_roughness"]
        
        # Apply biome-specific height
        height = config["base_height"] + combined_noise * config["height_variation"]
        
        return max(height, -5.0)  # Prevent going too far below sea level
    
    def get_chunk_key(self, chunk_x: int, chunk_z: int) -> str:
        """Get string key for chunk coordinates"""
        return f"{chunk_x}_{chunk_z}"
    
    def world_to_chunk_coords(self, x: float, z: float) -> Tuple[int, int]:
        """Convert world coordinates to chunk coordinates"""
        chunk_x = int(x // self.chunk_size)
        chunk_z = int(z // self.chunk_size)
        return chunk_x, chunk_z
    
    def generate_chunk(self, chunk_x: int, chunk_z: int) -> WorldChunk:
        """Generate a complete world chunk"""
        chunk_key = self.get_chunk_key(chunk_x, chunk_z)
        
        # Check if chunk already exists
        if chunk_key in self.chunks:
            return self.chunks[chunk_key]
        
        # Create new chunk
        chunk = WorldChunk(chunk_x=chunk_x, chunk_z=chunk_z, chunk_size=self.chunk_size)
        
        # Determine primary biome for chunk center
        center_x = chunk_x * self.chunk_size + self.chunk_size // 2
        center_z = chunk_z * self.chunk_size + self.chunk_size // 2
        chunk.biome = self.determine_biome(center_x, center_z)
        
        # Generate chunk-specific seed
        chunk.seed = hash(f"{self.world_seed}_{chunk_x}_{chunk_z}") % (2**31)
        random.seed(chunk.seed)
        
        # Generate terrain height map
        self._generate_terrain_heights(chunk)
        
        # Generate objects in chunk
        self._generate_chunk_objects(chunk)
        
        # Mark as generated
        chunk.generated = True
        
        # Store chunk
        self.chunks[chunk_key] = chunk
        
        return chunk
    
    def _generate_terrain_heights(self, chunk: WorldChunk):
        """Generate height map for chunk"""
        min_x, max_x, min_z, max_z = chunk.get_world_bounds()
        
        # Generate height at regular intervals
        for x in range(int(min_x), int(max_x) + 1, 4):  # Every 4 units
            for z in range(int(min_z), int(max_z) + 1, 4):
                height = self.generate_terrain_height(x, z, chunk.biome)
                chunk.terrain_height[f"{x}_{z}"] = height
    
    def _generate_chunk_objects(self, chunk: WorldChunk):
        """Generate objects within a chunk"""
        config = self.biome_configs[chunk.biome]
        min_x, max_x, min_z, max_z = chunk.get_world_bounds()
        
        # Calculate number of objects to place
        chunk_area = self.chunk_size * self.chunk_size
        num_objects = int(chunk_area * self.object_density * config["cultural_density"])
        
        # Place objects randomly
        for i in range(num_objects):
            # Random position within chunk
            obj_x = random.uniform(min_x, max_x)
            obj_z = random.uniform(min_z, max_z)
            obj_y = self.generate_terrain_height(obj_x, obj_z, chunk.biome)
            
            # Choose object type based on biome
            available_objects = config["object_types"]
            if available_objects:
                obj_type_name = random.choice(available_objects)
                obj_config = self.cultural_objects[obj_type_name]
                
                # Create world object
                world_obj = WorldObject(
                    object_id=f"obj_{chunk.chunk_x}_{chunk.chunk_z}_{i}",
                    object_type=obj_config["type"],
                    position=WorldPosition(obj_x, obj_y, obj_z),
                    rotation=random.uniform(0, 2 * math.pi),
                    scale=random.uniform(*obj_config["scale_range"]),
                    biome=chunk.biome,
                    name=obj_config["name"],
                    sanskrit_name=obj_config["sanskrit_name"],
                    cultural_significance=obj_config["cultural_significance"],
                    model_name=obj_config["model"],
                    interactable=(obj_config["type"] in [ObjectType.TEMPLE, ObjectType.RUINS]),
                    quest_related=(random.random() < 0.1)  # 10% chance
                )
                
                chunk.objects.append(world_obj)
        
        # Generate special quest locations
        self._generate_quest_locations(chunk)
    
    def _generate_quest_locations(self, chunk: WorldChunk):
        """Generate special quest-related locations"""
        # Only generate quest objects occasionally
        if random.random() < 0.3:  # 30% chance per chunk
            min_x, max_x, min_z, max_z = chunk.get_world_bounds()
            
            # Generate Sarasvati fragment location
            fragment_x = random.uniform(min_x, max_x)
            fragment_z = random.uniform(min_z, max_z)
            fragment_y = self.generate_terrain_height(fragment_x, fragment_z, chunk.biome)
            
            fragment_obj = WorldObject(
                object_id=f"fragment_{chunk.chunk_x}_{chunk.chunk_z}",
                object_type=ObjectType.LANDMARK,
                position=WorldPosition(fragment_x, fragment_y, fragment_z),
                biome=chunk.biome,
                name="Ancient Fragment Site",
                sanskrit_name="Prachin Khanda Sthal",
                cultural_significance="Site where Sarasvati Map fragments may be found",
                model_name="fragment_site.obj",
                interactable=True,
                collectible=True,
                quest_related=True
            )
            
            chunk.objects.append(fragment_obj)
    
    def get_chunks_around_position(self, x: float, z: float, radius: int = 2) -> List[WorldChunk]:
        """Get chunks around a world position"""
        center_chunk_x, center_chunk_z = self.world_to_chunk_coords(x, z)
        chunks = []
        
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                chunk_x = center_chunk_x + dx
                chunk_z = center_chunk_z + dz
                
                # Generate chunk if needed
                chunk = self.generate_chunk(chunk_x, chunk_z)
                chunks.append(chunk)
        
        return chunks
    
    def get_objects_near_position(self, x: float, z: float, radius: float = 50.0) -> List[WorldObject]:
        """Get objects near a world position"""
        # Get chunks in area
        chunk_radius = max(1, int(radius // self.chunk_size) + 1)
        chunks = self.get_chunks_around_position(x, z, chunk_radius)
        
        # Collect objects within radius
        center_pos = WorldPosition(x, 0, z)
        nearby_objects = []
        
        for chunk in chunks:
            for obj in chunk.objects:
                if center_pos.distance_2d(obj.position) <= radius:
                    nearby_objects.append(obj)
        
        return nearby_objects
    
    def get_height_at_position(self, x: float, z: float) -> float:
        """Get terrain height at world position"""
        chunk_x, chunk_z = self.world_to_chunk_coords(x, z)
        chunk = self.generate_chunk(chunk_x, chunk_z)
        
        return chunk.get_height_at(x, z)
    
    def get_world_statistics(self) -> Dict[str, any]:
        """Get world generation statistics"""
        total_objects = sum(len(chunk.objects) for chunk in self.chunks.values())
        total_chunks = len(self.chunks)
        
        # Count objects by type
        object_counts = {}
        for chunk in self.chunks.values():
            for obj in chunk.objects:
                obj_type = obj.object_type.value
                object_counts[obj_type] = object_counts.get(obj_type, 0) + 1
        
        return {
            "total_chunks_generated": total_chunks,
            "total_objects_generated": total_objects,
            "objects_per_chunk_average": total_objects / max(total_chunks, 1),
            "object_type_distribution": object_counts,
            "world_seed": self.world_seed
        }


# Create global world generator
ancient_bharat_world = AncientBharatWorldGenerator()


# Utility functions for easy access
def get_world_generator() -> AncientBharatWorldGenerator:
    """Get global world generator"""
    return ancient_bharat_world


def generate_world_area(x: float, z: float, radius: int = 3) -> List[WorldChunk]:
    """Generate world area around position"""
    return ancient_bharat_world.get_chunks_around_position(x, z, radius)


def get_nearby_objects(x: float, z: float, radius: float = 50.0) -> List[WorldObject]:
    """Get objects near position"""
    return ancient_bharat_world.get_objects_near_position(x, z, radius)


def get_terrain_height(x: float, z: float) -> float:
    """Get terrain height at position"""
    return ancient_bharat_world.get_height_at_position(x, z)


# Example usage and testing
if __name__ == "__main__":
    print("🌍 Ancient Bharat World Generator")
    print("=" * 50)
    
    world_gen = get_world_generator()
    
    # Test world generation
    print("\n🏔️ Testing World Generation:")
    test_positions = [
        (0, 0, "Indrapura City Center"),
        (-250, 0, "Dust Plains"),
        (250, 0, "Ocean Frontier"),
        (0, 250, "Himalayan Peaks"),
        (0, -150, "Narmada Forest")
    ]
    
    for x, z, region_name in test_positions:
        print(f"\n📍 {region_name} ({x}, {z}):")
        
        # Determine biome
        biome = world_gen.determine_biome(x, z)
        print(f"  Biome: {biome.value}")
        
        # Get terrain height
        height = world_gen.generate_terrain_height(x, z, biome)
        print(f"  Terrain Height: {height:.2f}")
        
        # Generate chunk
        chunk_x, chunk_z = world_gen.world_to_chunk_coords(x, z)
        chunk = world_gen.generate_chunk(chunk_x, chunk_z)
        print(f"  Chunk: ({chunk_x}, {chunk_z})")
        print(f"  Objects in Chunk: {len(chunk.objects)}")
        
        # Show some objects
        for i, obj in enumerate(chunk.objects[:3]):  # Show first 3 objects
            print(f"    {i+1}. {obj.name} ({obj.sanskrit_name})")
    
    # Test nearby objects
    print(f"\n🔍 Objects near Indrapura City (0, 0):")
    nearby = world_gen.get_objects_near_position(0, 0, 100)
    print(f"  Found {len(nearby)} objects within 100 units")
    
    for obj in nearby[:5]:  # Show first 5
        dist = WorldPosition(0, 0, 0).distance_2d(obj.position)
        print(f"    {obj.name}: {dist:.1f} units away")
    
    # Get statistics
    stats = world_gen.get_world_statistics()
    print(f"\n📊 World Statistics:")
    print(f"  Chunks Generated: {stats['total_chunks_generated']}")
    print(f"  Total Objects: {stats['total_objects_generated']}")
    print(f"  Average Objects per Chunk: {stats['objects_per_chunk_average']:.1f}")
    print(f"  World Seed: {stats['world_seed']}")
    
    print("\n✅ World generation test completed!")