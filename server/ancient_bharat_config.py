#!/usr/bin/env python3
"""
Ancient Bharat Configuration
Python-based configuration management for the game server
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ServerConfig:
    """Server configuration using Python dataclass"""
    # Network settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Game settings
    max_players: int = 100
    world_size: int = 1000
    auto_save_interval: int = 300  # seconds
    
    # Ancient Bharat specific settings
    enable_weather_system: bool = True
    enable_day_night_cycle: bool = True
    enable_cultural_events: bool = True
    
    # Region settings
    region_transition_distance: float = 200.0
    npc_interaction_radius: float = 10.0
    
    # Chat and social
    max_chat_history: int = 100
    chat_rate_limit: int = 5  # messages per minute
    
    # Performance
    chunk_size: int = 16
    max_chunks_loaded: int = 100
    player_update_rate: int = 30  # updates per second


@dataclass
class QuestConfig:
    """Configuration for quest system"""
    # Main quest settings
    sarasvati_fragments_total: int = 7
    fragment_discovery_radius: float = 5.0
    
    # Side quest settings
    village_rebuilding_tasks: int = 5
    scripture_locations: int = 12
    animal_spirit_guardians: int = 8
    
    # Quest rewards
    fragment_reward_xp: int = 1000
    side_quest_reward_xp: int = 250
    daily_task_reward_xp: int = 50


@dataclass 
class WorldConfig:
    """World generation and biome settings"""
    # Terrain generation
    terrain_seed: int = 12345
    terrain_scale: float = 0.02
    max_elevation: float = 100.0
    
    # Biome boundaries (in world coordinates)
    dust_plains_boundary: float = -200.0
    ocean_frontier_boundary: float = 200.0
    himalayan_peaks_boundary: float = 200.0
    narmada_forest_boundary: float = -100.0
    
    # Object spawning
    max_objects_per_chunk: int = 10
    special_object_chance: float = 0.3
    
    # Weather system
    weather_change_interval: int = 1800  # seconds (30 minutes)
    monsoon_season_months: list = None
    
    def __post_init__(self):
        if self.monsoon_season_months is None:
            self.monsoon_season_months = [6, 7, 8, 9]  # June-September


class ConfigManager:
    """Manages all game configuration using Python JSON files"""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize configuration manager"""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)  # Create config directory if it doesn't exist
        
        # Configuration objects
        self.server_config = ServerConfig()
        self.quest_config = QuestConfig()
        self.world_config = WorldConfig()
        
        # Load existing configs
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all configuration files"""
        try:
            self.server_config = self._load_config("server_config.json", ServerConfig)
            self.quest_config = self._load_config("quest_config.json", QuestConfig)
            self.world_config = self._load_config("world_config.json", WorldConfig)
            print("✅ All configurations loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading configs: {e}")
            print("🔧 Using default configurations")
    
    def save_all_configs(self):
        """Save all configurations to JSON files"""
        try:
            self._save_config("server_config.json", self.server_config)
            self._save_config("quest_config.json", self.quest_config)
            self._save_config("world_config.json", self.world_config)
            print("✅ All configurations saved successfully")
        except Exception as e:
            print(f"❌ Error saving configs: {e}")
    
    def _load_config(self, filename: str, config_class):
        """Load a specific config file"""
        config_path = self.config_dir / filename
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return config_class(**config_data)
        else:
            # Create default config file
            default_config = config_class()
            self._save_config(filename, default_config)
            return default_config
    
    def _save_config(self, filename: str, config_object):
        """Save a config object to JSON file"""
        config_path = self.config_dir / filename
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(config_object), f, indent=4, ensure_ascii=False)
    
    def get_server_address(self) -> str:
        """Get full server address"""
        return f"http://{self.server_config.host}:{self.server_config.port}"
    
    def get_websocket_address(self) -> str:
        """Get WebSocket address"""
        protocol = "wss" if self.server_config.host != "localhost" else "ws"
        return f"{protocol}://{self.server_config.host}:{self.server_config.port}/ws"
    
    def update_server_config(self, **kwargs):
        """Update server configuration dynamically"""
        for key, value in kwargs.items():
            if hasattr(self.server_config, key):
                setattr(self.server_config, key, value)
        self.save_all_configs()
    
    def is_in_region(self, x: float, z: float, region: str) -> bool:
        """Check if coordinates are in specific region"""
        if region == "dust_plains":
            return x < self.world_config.dust_plains_boundary
        elif region == "ocean_frontier":
            return x > self.world_config.ocean_frontier_boundary
        elif region == "himalayan_peaks":
            return z > self.world_config.himalayan_peaks_boundary
        elif region == "narmada_forest":
            return z < self.world_config.narmada_forest_boundary
        else:  # indrapura_city (center)
            return (self.world_config.dust_plains_boundary <= x <= self.world_config.ocean_frontier_boundary and
                   self.world_config.narmada_forest_boundary <= z <= self.world_config.himalayan_peaks_boundary)


# Game data management using Python JSON
class GameDataManager:
    """Manages persistent game data using Python JSON files"""
    
    def __init__(self, data_dir: str = "game_data"):
        """Initialize data manager"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.player_data = {}      # Player progress and stats
        self.world_state = {}      # World objects and changes
        self.quest_progress = {}   # Quest completion status
        self.npc_states = {}       # NPC interaction history
        
        # Load existing data
        self.load_all_data()
    
    def load_all_data(self):
        """Load all persistent game data"""
        try:
            self.player_data = self._load_json_file("player_data.json")
            self.world_state = self._load_json_file("world_state.json")
            self.quest_progress = self._load_json_file("quest_progress.json")
            self.npc_states = self._load_json_file("npc_states.json")
            print("📊 Game data loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading game data: {e}")
            self._initialize_empty_data()
    
    def save_all_data(self):
        """Save all game data to JSON files"""
        try:
            self._save_json_file("player_data.json", self.player_data)
            self._save_json_file("world_state.json", self.world_state)
            self._save_json_file("quest_progress.json", self.quest_progress)
            self._save_json_file("npc_states.json", self.npc_states)
            print("💾 Game data saved successfully")
        except Exception as e:
            print(f"❌ Error saving game data: {e}")
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load data from JSON file"""
        file_path = self.data_dir / filename
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    
    def _save_json_file(self, filename: str, data: Dict[str, Any]):
        """Save data to JSON file"""
        file_path = self.data_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def _initialize_empty_data(self):
        """Initialize empty data structures"""
        self.player_data = {}
        self.world_state = {
            "sarasvati_fragments_found": [],
            "world_objects": {},
            "cultural_events": []
        }
        self.quest_progress = {
            "main_quest": {"fragments_collected": 0, "total_fragments": 7},
            "side_quests": {},
            "daily_tasks": {}
        }
        self.npc_states = {}
    
    # Player data methods
    def save_player_progress(self, player_id: str, player_data: dict):
        """Save player progress and statistics"""
        self.player_data[player_id] = {
            "name": player_data.get("name", f"Player_{player_id[:8]}"),
            "level": player_data.get("level", 1),
            "experience": player_data.get("experience", 0),
            "regions_visited": player_data.get("regions_visited", ["ocean_frontier"]),
            "quests_completed": player_data.get("quests_completed", []),
            "npc_reputation": player_data.get("npc_reputation", {}),
            "last_position": player_data.get("last_position", {"x": 0, "y": 2, "z": 0}),
            "play_time": player_data.get("play_time", 0),
            "last_login": player_data.get("last_login", 0)
        }
    
    def get_player_progress(self, player_id: str) -> dict:
        """Get player progress data"""
        return self.player_data.get(player_id, {
            "name": f"Player_{player_id[:8]}",
            "level": 1,
            "experience": 0,
            "regions_visited": ["ocean_frontier"],
            "quests_completed": [],
            "npc_reputation": {},
            "last_position": {"x": 0, "y": 2, "z": 0},
            "play_time": 0,
            "last_login": 0
        })
    
    # Quest data methods
    def update_quest_progress(self, quest_id: str, progress_data: dict):
        """Update quest progress"""
        if quest_id not in self.quest_progress["side_quests"]:
            self.quest_progress["side_quests"][quest_id] = {}
        
        self.quest_progress["side_quests"][quest_id].update(progress_data)
    
    def add_sarasvati_fragment(self, fragment_id: str, found_by: str):
        """Record discovery of Sarasvati Map fragment"""
        if fragment_id not in self.world_state["sarasvati_fragments_found"]:
            self.world_state["sarasvati_fragments_found"].append({
                "fragment_id": fragment_id,
                "found_by": found_by,
                "found_at": time.time(),
                "total_found": len(self.world_state["sarasvati_fragments_found"]) + 1
            })
            
            # Update main quest progress
            self.quest_progress["main_quest"]["fragments_collected"] = len(
                self.world_state["sarasvati_fragments_found"]
            )
    
    # NPC interaction methods
    def record_npc_interaction(self, player_id: str, npc_id: str, interaction_data: dict):
        """Record player interaction with NPC"""
        if player_id not in self.npc_states:
            self.npc_states[player_id] = {}
        
        if npc_id not in self.npc_states[player_id]:
            self.npc_states[player_id][npc_id] = {
                "first_meeting": time.time(),
                "interactions": 0,
                "reputation": 0,
                "completed_quests": []
            }
        
        # Update interaction data
        npc_state = self.npc_states[player_id][npc_id]
        npc_state["interactions"] += 1
        npc_state["last_interaction"] = time.time()
        
        # Update reputation based on interaction
        if interaction_data.get("quest_completed"):
            npc_state["reputation"] += 10
            npc_state["completed_quests"].append(interaction_data["quest_id"])
        elif interaction_data.get("helpful_response"):
            npc_state["reputation"] += 1
    
    def get_npc_relationship(self, player_id: str, npc_id: str) -> dict:
        """Get player's relationship status with NPC"""
        if player_id in self.npc_states and npc_id in self.npc_states[player_id]:
            return self.npc_states[player_id][npc_id]
        else:
            return {
                "first_meeting": None,
                "interactions": 0,
                "reputation": 0,
                "completed_quests": []
            }
    
    def get_game_statistics(self) -> dict:
        """Get overall game statistics"""
        return {
            "total_players": len(self.player_data),
            "fragments_found": len(self.world_state["sarasvati_fragments_found"]),
            "total_fragments": self.quest_progress["main_quest"]["total_fragments"],
            "active_quests": len(self.quest_progress["side_quests"]),
            "npc_interactions": sum(
                sum(npc_data["interactions"] for npc_data in player_npcs.values())
                for player_npcs in self.npc_states.values()
            )
        }


# Create global instances
config_manager = ConfigManager()
data_manager = GameDataManager()


# Utility functions for easy access
def get_config() -> ConfigManager:
    """Get global configuration manager"""
    return config_manager


def get_data_manager() -> GameDataManager:
    """Get global data manager"""
    return data_manager


def save_game_state():
    """Save all game configuration and data"""
    config_manager.save_all_configs()
    data_manager.save_all_data()


# Example usage and testing
if __name__ == "__main__":
    print("🔧 Ancient Bharat Configuration & Data Management")
    print("=" * 60)
    
    # Test configuration management
    print("\n📋 Server Configuration:")
    server_cfg = config_manager.server_config
    print(f"  Host: {server_cfg.host}:{server_cfg.port}")
    print(f"  Max Players: {server_cfg.max_players}")
    print(f"  World Size: {server_cfg.world_size}")
    
    print("\n🗺️ World Configuration:")
    world_cfg = config_manager.world_config
    print(f"  Terrain Seed: {world_cfg.terrain_seed}")
    print(f"  Region Boundaries: {world_cfg.dust_plains_boundary} to {world_cfg.ocean_frontier_boundary}")
    
    print("\n📊 Quest Configuration:")
    quest_cfg = config_manager.quest_config
    print(f"  Sarasvati Fragments: {quest_cfg.sarasvati_fragments_total}")
    print(f"  Village Tasks: {quest_cfg.village_rebuilding_tasks}")
    
    # Test data management
    print("\n💾 Testing Data Management:")
    
    # Simulate player progress
    test_player_data = {
        "name": "TestPlayer",
        "level": 5,
        "experience": 1250,
        "regions_visited": ["ocean_frontier", "indrapura_city"]
    }
    data_manager.save_player_progress("test_player_123", test_player_data)
    
    # Simulate quest progress
    data_manager.add_sarasvati_fragment("fragment_001", "test_player_123")
    
    # Get statistics
    stats = data_manager.get_game_statistics()
    print(f"  Players: {stats['total_players']}")
    print(f"  Fragments Found: {stats['fragments_found']}/{stats['total_fragments']}")
    
    # Save everything
    save_game_state()
    print("\n✅ Configuration and data management test completed!")