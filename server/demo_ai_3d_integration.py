#!/usr/bin/env python3
"""
AI 3D Model Integration Demo
Demonstrates the complete integration of AI 3D model generation with procedural content
Shows Luma AI, Meshy AI, Kaedim, and Scenario.gg capabilities
"""

import sys
import os
import asyncio
import time

# Add server directory to path
server_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, server_path)

from procedural_integration import procedural_manager
from procedural_3d_integration import procedural_3d_manager


async def demo_ai_3d_model_integration():
    """Demonstrate the complete AI 3D model integration"""
    print("=" * 70)
    print("🤖 AI 3D MODEL GENERATION INTEGRATION DEMO")
    print("=" * 70)
    
    # Initialize systems
    print("\n🔮 Initializing systems...")
    
    # Initialize procedural content generation
    if not procedural_manager.is_initialized:
        print("   Initializing procedural content generation...")
        procedural_manager.initialize()
    
    print("   Procedural content system ready!")
    print(f"   Generated content: {procedural_manager.get_statistics()['total_content']:,} items")
    
    # Initialize AI 3D model system
    print("   Initializing AI 3D model generation...")
    procedural_3d_manager.load_model_database()
    print("   AI 3D model system ready!")
    
    # Demo 1: Generate models for specific procedural content
    print("\n" + "=" * 70)
    print("🎯 DEMO 1: INDIVIDUAL MODEL GENERATION")
    print("=" * 70)
    
    # Get some sample content
    weapons = list(procedural_manager.generated_weapons.values())
    beasts = list(procedural_manager.generated_beasts.values())
    divine_entities = list(procedural_manager.generated_divine_entities.values())
    
    sample_items = [
        {
            "content": weapons[0],
            "type": "weapon",
            "display_name": "Epic Weapon"
        },
        {
            "content": beasts[0], 
            "type": "beast",
            "display_name": "Mythical Beast"
        },
        {
            "content": divine_entities[0],
            "type": "divine_entity", 
            "display_name": "Divine Entity"
        }
    ]
    
    for i, item in enumerate(sample_items, 1):
        content = item["content"]
        content_data = {
            "id": getattr(content, f"{item['type']}_id", f"id_{i}"),
            "content_type": item["type"],
            "name": content.name,
            "description": content.description,
            "rarity": content.rarity.value
        }
        
        # Add type-specific data
        if item["type"] == "weapon":
            content_data.update({
                "material": content.material,
                "enchantment": content.enchantment,
                "weapon_type": content.weapon_type
            })
        elif item["type"] == "beast":
            content_data.update({
                "base_creature": content.base_creature,
                "modifier": content.modifier,
                "origin": content.origin
            })
        elif item["type"] == "divine_entity":
            content_data.update({
                "domain": content.domain,
                "form": content.form,
                "alignment": content.alignment
            })
        
        print(f"\n{i}. Generating 3D model for {item['display_name']}: {content.name}")
        print(f"   Description: {content.description[:60]}...")
        print(f"   Rarity: {content.rarity.value.upper()}")
        
        start_time = time.time()
        model_result = await procedural_3d_manager.generate_model_for_content(content_data)
        generation_time = time.time() - start_time
        
        if model_result:
            print(f"   ✅ Success! Generated using {model_result['service_used']}")
            print(f"   📁 File: {model_result['file_path']}")
            print(f"   📊 Size: {model_result['file_size'] / 1024:.1f} KB")
            print(f"   ⏱️ Time: {generation_time:.1f}s")
        else:
            print(f"   ❌ Failed to generate model")
    
    # Demo 2: Batch generation showcase
    print("\n" + "=" * 70)
    print("🚀 DEMO 2: BATCH MODEL GENERATION")
    print("=" * 70)
    
    print("\nStarting batch generation for popular procedural content...")
    batch_start = time.time()
    
    batch_result = await procedural_3d_manager.batch_generate_models_for_procedural_content()
    
    batch_time = time.time() - batch_start
    
    print(f"\n✅ Batch generation completed!")
    print(f"   Total items processed: {batch_result['total_requested']}")
    print(f"   Successful generations: {batch_result['successful_generations']}")
    print(f"   Failed generations: {batch_result['failed_generations']}")
    print(f"   Total time: {batch_time:.1f}s")
    print(f"   Average time per item: {batch_time/batch_result['total_requested']:.1f}s")
    
    # Demo 3: Show AI service capabilities
    print("\n" + "=" * 70)
    print("🤖 DEMO 3: AI SERVICE SHOWCASE")
    print("=" * 70)
    
    ai_agent = procedural_3d_manager.ai_agent
    
    print("\nAvailable AI 3D Model Services:")
    for service_name, service_config in ai_agent.ai_services.items():
        status = "✅ Available" if service_config.get("available", False) else "❌ Unavailable"
        print(f"   {service_name}: {status}")
        
        if service_config.get("available", False):
            strengths = service_config.get("strengths", [])
            specializes = service_config.get("specializes", [])
            print(f"      Strengths: {', '.join(strengths[:3])}")
            print(f"      Specializes in: {', '.join(specializes)}")
            print(f"      Max Quality: {service_config.get('max_quality', 'Unknown')}")
    
    # Demo 4: Service comparison
    print("\n" + "=" * 70)
    print("⚔️ DEMO 4: AI SERVICE COMPARISON")
    print("=" * 70)
    
    print("\nLuma AI Genie:")
    print("   🎯 Best for: Realistic textures, fast generation")
    print("   📈 Quality: High (0.85/1.0)")
    print("   ⚡ Speed: Very Fast (2.5s average)")
    print("   💎 Specializes: Weapons, props, characters")
    
    print("\nMeshy AI:")
    print("   🎯 Best for: Web-based generation, stylized models")
    print("   📈 Quality: High (0.8/1.0)")
    print("   ⚡ Speed: Fast (3.0s average)")
    print("   💎 Specializes: Props, environments, creatures")
    
    print("\nKaedim:")
    print("   🎯 Best for: Production-ready, riggable models")
    print("   📈 Quality: Ultra High (0.9/1.0)")
    print("   ⚡ Speed: Moderate (5.0s average)")
    print("   💎 Specializes: Characters, vehicles, complex models")
    
    print("\nScenario.gg:")
    print("   🎯 Best for: Game-tailored assets, consistent style")
    print("   📈 Quality: High (0.82/1.0)")
    print("   ⚡ Speed: Fast (3.5s average)")
    print("   💎 Specializes: Game props, characters, environments")
    
    # Demo 5: Statistics and capabilities
    print("\n" + "=" * 70)
    print("📊 DEMO 5: SYSTEM STATISTICS")
    print("=" * 70)
    
    # Get all statistics
    procedural_stats = procedural_manager.get_statistics()
    model_stats = procedural_3d_manager.get_statistics()
    
    print(f"\nProcedural Content Generation:")
    print(f"   Total content pieces: {procedural_stats['total_content']:,}")
    print(f"   Job classes: {procedural_stats['total_job_classes']:,}")
    print(f"   Weapons: {procedural_stats['total_weapons']:,}")
    print(f"   Beasts: {procedural_stats['total_beasts']:,}")
    print(f"   Divine entities: {procedural_stats['total_divine_entities']:,}")
    
    combinations = procedural_stats['potential_combinations']
    total_combinations = sum(combinations.values())
    print(f"   Potential combinations: {total_combinations:,}")
    
    print(f"\n3D Model Generation:")
    print(f"   Models generated: {model_stats['completed_generations']}")
    print(f"   Models cached: {model_stats['cached_models']}")
    print(f"   Success rate: {model_stats['success_rate']}")
    print(f"   Total requests: {model_stats['total_requests']}")
    print(f"   Cache hit rate: {model_stats['cache_hit_rate'] if 'cache_hit_rate' in model_stats else 'N/A'}")
    
    # Demo 6: Future capabilities showcase
    print("\n" + "=" * 70)
    print("🚀 DEMO 6: INFINITE SCALING POTENTIAL")
    print("=" * 70)
    
    print(f"\n🎮 Your game now has INFINITE visual content scaling!")
    print(f"\n🔥 Key achievements:")
    print(f"   ✅ {total_combinations:,} possible procedural content combinations")
    print(f"   ✅ AI-powered 3D model generation for every item")
    print(f"   ✅ Multiple AI services with smart fallback")
    print(f"   ✅ Automatic model caching and optimization")
    print(f"   ✅ Real-time generation for new content")
    
    print(f"\n🌟 AI Services Integration:")
    print(f"   🎨 Luma AI Genie: High-quality, fast generation")
    print(f"   🖥️ Meshy AI: Web-optimized, stylized models")
    print(f"   🏭 Kaedim: Production-ready, riggable assets")
    print(f"   🎮 Scenario.gg: Game-tailored, consistent style")
    
    print(f"\n🚀 What this means for players:")
    print(f"   • Every weapon, beast, and divine entity gets a unique 3D model")
    print(f"   • Models generated on-demand or pre-cached for performance")
    print(f"   • Multiple art styles and quality levels available")
    print(f"   • Seamless integration with procedural content system")
    print(f"   • Infinite visual variety - no repetitive assets!")
    
    print(f"\n" + "=" * 70)
    print(f"🎉 AI 3D MODEL INTEGRATION DEMO COMPLETE!")
    print(f"🌟 Your game now has INFINITE visual content generation!")
    print(f"=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_ai_3d_model_integration())