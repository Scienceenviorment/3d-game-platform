"""
Procedural 3D Model Integration
Connects AI 3D Model Agent with Procedural Generation System
Automatically generates 3D models for procedural content
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
from pathlib import Path

# Import our systems
from ai_3d_model_agent import AI3DModelAgent, ModelRequest, ModelFormat
from procedural_integration import procedural_manager


@dataclass
class ModelGenerationTask:
    """Task for generating a 3D model"""
    content_id: str
    content_type: str
    content_data: Dict[str, Any]
    priority: int = 1  # 1=low, 2=medium, 3=high
    created_at: float = 0.0
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()


class Procedural3DModelManager:
    """Manages 3D model generation for procedural content"""
    
    def __init__(self, ai_agent: AI3DModelAgent = None):
        self.ai_agent = ai_agent or AI3DModelAgent()
        self.generation_queue: List[ModelGenerationTask] = []
        self.active_generations = {}
        self.generated_models = {}
        
        # Configuration
        self.max_concurrent_generations = 3
        self.auto_generate_enabled = True
        self.batch_size = 10
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "completed_generations": 0,
            "failed_generations": 0,
            "cache_hits": 0,
            "queue_size": 0
        }
        
        print("🎨 Procedural 3D Model Manager initialized")
    
    async def generate_model_for_content(self, content_data: Dict) -> Optional[Dict]:
        """Generate 3D model for specific procedural content"""
        try:
            self.stats["total_requests"] += 1
            
            content_id = content_data.get("id", "unknown")
            content_type = content_data.get("content_type", "unknown")
            
            # Check if model already exists
            if content_id in self.generated_models:
                self.stats["cache_hits"] += 1
                print(f"📦 Using cached 3D model for {content_data.get('name', content_id)}")
                return self.generated_models[content_id]
            
            # Generate new model using AI agent
            print(f"🎨 Generating 3D model for {content_data.get('name', content_id)}...")
            
            model_result = await self.ai_agent.generate_model_for_content(content_data)
            
            if model_result:
                # Convert to our format and cache
                model_info = {
                    "model_id": model_result.model_id,
                    "file_path": model_result.file_path,
                    "format": model_result.format.value,
                    "file_size": model_result.file_size,
                    "generation_time": model_result.generation_time,
                    "service_used": model_result.service_used.value,
                    "quality_score": model_result.metadata.get("quality_score", 0.5),
                    "content_name": content_data.get("name", "Unknown"),
                    "content_type": content_type,
                    "created_at": time.time()
                }
                
                self.generated_models[content_id] = model_info
                self.stats["completed_generations"] += 1
                
                print(f"✅ Generated 3D model for {content_data.get('name')} using {model_result.service_used.value}")
                return model_info
            else:
                self.stats["failed_generations"] += 1
                print(f"❌ Failed to generate 3D model for {content_data.get('name')}")
                return None
                
        except Exception as e:
            self.stats["failed_generations"] += 1
            print(f"❌ Error generating 3D model: {e}")
            return None
    
    async def batch_generate_models_for_procedural_content(self) -> Dict[str, Any]:
        """Generate 3D models for popular procedural content"""
        print("🚀 Starting batch 3D model generation for procedural content...")
        
        # Get statistics from procedural manager
        if not procedural_manager.is_initialized:
            print("⚠️ Procedural manager not initialized")
            return {"error": "Procedural manager not initialized"}
        
        # Get content to generate models for
        content_to_generate = []
        
        # Get popular job classes
        job_classes = list(procedural_manager.generated_job_classes.values())[:5]
        for job_class in job_classes:
            content_to_generate.append({
                "id": job_class.class_id,
                "content_type": "job_class",
                "name": job_class.name,
                "description": job_class.description,
                "rarity": job_class.rarity.value,
                "element": job_class.element,
                "theme": job_class.theme,
                "role": job_class.role
            })
        
        # Get popular weapons
        weapons = list(procedural_manager.generated_weapons.values())[:8]
        for weapon in weapons:
            content_to_generate.append({
                "id": weapon.weapon_id,
                "content_type": "weapon",
                "name": weapon.name,
                "description": weapon.description,
                "rarity": weapon.rarity.value,
                "material": weapon.material,
                "enchantment": weapon.enchantment,
                "weapon_type": weapon.weapon_type
            })
        
        # Get popular beasts
        beasts = list(procedural_manager.generated_beasts.values())[:6]
        for beast in beasts:
            content_to_generate.append({
                "id": beast.beast_id,
                "content_type": "beast",
                "name": beast.name,
                "description": beast.description,
                "rarity": beast.rarity.value,
                "base_creature": beast.base_creature,
                "modifier": beast.modifier,
                "origin": beast.origin
            })
        
        # Get divine entities
        divine_entities = list(procedural_manager.generated_divine_entities.values())[:4]
        for divine in divine_entities:
            content_to_generate.append({
                "id": divine.entity_id,
                "content_type": "divine_entity",
                "name": divine.name,
                "description": divine.description,
                "rarity": divine.rarity.value,
                "domain": divine.domain,
                "form": divine.form,
                "alignment": divine.alignment
            })
        
        print(f"📋 Generating 3D models for {len(content_to_generate)} procedural items...")
        
        # Generate models with concurrency control
        semaphore = asyncio.Semaphore(self.max_concurrent_generations)
        
        async def limited_generate(content):
            async with semaphore:
                return await self.generate_model_for_content(content)
        
        # Execute batch generation
        start_time = time.time()
        tasks = [limited_generate(content) for content in content_to_generate]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = [r for r in results if isinstance(r, dict) and r is not None]
        failed_count = len(results) - len(successful_results)
        
        generation_time = time.time() - start_time
        
        print(f"✅ Batch generation complete!")
        print(f"   Generated: {len(successful_results)}/{len(content_to_generate)} models")
        print(f"   Total time: {generation_time:.1f}s")
        print(f"   Average time per model: {generation_time/len(content_to_generate):.1f}s")
        
        return {
            "total_requested": len(content_to_generate),
            "successful_generations": len(successful_results),
            "failed_generations": failed_count,
            "generation_time": generation_time,
            "models_generated": successful_results
        }
    
    def get_model_for_content(self, content_id: str) -> Optional[Dict]:
        """Get 3D model info for specific content"""
        return self.generated_models.get(content_id)
    
    def get_models_by_type(self, content_type: str) -> List[Dict]:
        """Get all 3D models of specific type"""
        return [
            model for model in self.generated_models.values() 
            if model.get("content_type") == content_type
        ]
    
    async def preload_priority_models(self) -> Dict[str, Any]:
        """Preload 3D models for high-priority content"""
        print("🔄 Preloading priority 3D models...")
        
        priority_content = []
        
        # High-priority content that should have models ready
        # Epic and legendary weapons
        for weapon in procedural_manager.generated_weapons.values():
            if weapon.rarity.value in ["epic", "legendary", "mythical"]:
                priority_content.append({
                    "id": weapon.weapon_id,
                    "content_type": "weapon", 
                    "name": weapon.name,
                    "description": weapon.description,
                    "rarity": weapon.rarity.value,
                    "material": weapon.material,
                    "enchantment": weapon.enchantment
                })
                if len(priority_content) >= 5:  # Limit to 5 priority weapons
                    break
        
        # Legendary beasts
        for beast in procedural_manager.generated_beasts.values():
            if beast.rarity.value in ["legendary", "mythical"]:
                priority_content.append({
                    "id": beast.beast_id,
                    "content_type": "beast",
                    "name": beast.name, 
                    "description": beast.description,
                    "rarity": beast.rarity.value,
                    "base_creature": beast.base_creature
                })
                if len([c for c in priority_content if c["content_type"] == "beast"]) >= 3:
                    break
        
        # Generate models for priority content
        results = []
        for content in priority_content:
            result = await self.generate_model_for_content(content)
            if result:
                results.append(result)
        
        print(f"✅ Preloaded {len(results)} priority 3D models")
        return {"preloaded_models": len(results), "models": results}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics"""
        success_rate = 0
        if self.stats["total_requests"] > 0:
            success_rate = (self.stats["completed_generations"] / self.stats["total_requests"]) * 100
        
        return {
            **self.stats,
            "queue_size": len(self.generation_queue),
            "active_generations": len(self.active_generations),
            "cached_models": len(self.generated_models),
            "success_rate": f"{success_rate:.1f}%",
            "ai_agent_stats": self.ai_agent.get_statistics()
        }
    
    async def auto_generate_models_for_new_content(self, content_data: Dict):
        """Automatically generate 3D models when new content is created"""
        if not self.auto_generate_enabled:
            return
        
        # Check if this content should get a model
        content_type = content_data.get("content_type", "")
        rarity = content_data.get("rarity", "common")
        
        # Auto-generate for rare+ content
        if rarity in ["rare", "epic", "legendary", "mythical", "divine"]:
            await self.generate_model_for_content(content_data)
    
    def save_model_database(self, filepath: str = "models/model_database.json"):
        """Save generated model database"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            database = {
                "metadata": {
                    "created_at": time.time(),
                    "total_models": len(self.generated_models),
                    "statistics": self.get_statistics()
                },
                "models": self.generated_models
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved 3D model database: {len(self.generated_models)} models")
            
        except Exception as e:
            print(f"⚠️ Failed to save model database: {e}")
    
    def load_model_database(self, filepath: str = "models/model_database.json"):
        """Load generated model database"""
        try:
            if Path(filepath).exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    database = json.load(f)
                
                self.generated_models = database.get("models", {})
                print(f"📂 Loaded 3D model database: {len(self.generated_models)} models")
            
        except Exception as e:
            print(f"⚠️ Failed to load model database: {e}")


# Global instance
procedural_3d_manager = Procedural3DModelManager()


async def test_procedural_3d_integration():
    """Test the procedural 3D model integration"""
    print("=" * 60)
    print("🎨 TESTING PROCEDURAL 3D MODEL INTEGRATION")
    print("=" * 60)
    
    # Initialize procedural content if needed
    if not procedural_manager.is_initialized:
        print("🔮 Initializing procedural content...")
        procedural_manager.initialize()
    
    # Test individual model generation
    print("\n🎯 Testing Individual Model Generation...")
    
    # Get a sample weapon from procedural generation
    sample_weapon = next(iter(procedural_manager.generated_weapons.values()))
    weapon_data = {
        "id": sample_weapon.weapon_id,
        "content_type": "weapon",
        "name": sample_weapon.name,
        "description": sample_weapon.description,
        "rarity": sample_weapon.rarity.value,
        "material": sample_weapon.material,
        "enchantment": sample_weapon.enchantment
    }
    
    model_result = await procedural_3d_manager.generate_model_for_content(weapon_data)
    if model_result:
        print(f"✅ Generated 3D model for {weapon_data['name']}")
        print(f"   Service: {model_result['service_used']}")
        print(f"   File: {model_result['file_path']}")
        print(f"   Time: {model_result['generation_time']:.1f}s")
    
    # Test batch generation
    print(f"\n🚀 Testing Batch Generation...")
    batch_result = await procedural_3d_manager.batch_generate_models_for_procedural_content()
    print(f"   Success: {batch_result['successful_generations']}/{batch_result['total_requested']}")
    
    # Show statistics
    print(f"\n📊 3D Model Manager Statistics:")
    stats = procedural_3d_manager.get_statistics()
    for key, value in stats.items():
        if key != "ai_agent_stats":
            print(f"   {key}: {value}")
    
    print(f"\n🎉 Procedural 3D Model Integration test complete!")


if __name__ == "__main__":
    asyncio.run(test_procedural_3d_integration())