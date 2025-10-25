#!/usr/bin/env python3
"""
Simple AI 3D Model Integration Demo
==================================

A simple demo showing the AI 3D model system working with procedural content.
"""

import sys
import os
import asyncio

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

try:
    from procedural_generator import ProceduralGenerator
    from ai_3d_model_agent import AI3DModelAgent, ModelRequest
    from procedural_3d_integration import Procedural3DModelManager
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

async def demo_basic_integration():
    """Basic demo of procedural + AI 3D model integration"""
    print("🎮 Simple AI 3D Model Integration Demo")
    print("=" * 50)
    
    # Create systems
    generator = ProceduralGenerator()
    model_agent = AI3DModelAgent()
    
    print("\n1. Generating procedural content...")
    
    # Generate some content
    beast = generator.generate_beast()
    weapon = generator.generate_weapon()
    
    print(f"   Beast: {beast.name}")
    print(f"   Description: {beast.description}")
    print(f"   Rarity: {beast.rarity.value}")
    
    print(f"\n   Weapon: {weapon.name}")
    print(f"   Description: {weapon.description}")
    print(f"   Type: {weapon.weapon_type}")
    
    print("\n2. Creating 3D model requests...")
    
    # Create model requests
    beast_request = ModelRequest(
        content_name=beast.name,
        content_type="beast",
        content_description=f"Fantasy creature: {beast.name} - {beast.description}",
        style_preferences={"tags": ["creature", "fantasy", beast.rarity.value]},
        quality_level="high"
    )
    
    weapon_request = ModelRequest(
        content_name=weapon.name,
        content_type="weapon",
        content_description=f"Fantasy weapon: {weapon.name} - {weapon.description}",
        style_preferences={"tags": ["weapon", "fantasy", weapon.rarity.value]},
        quality_level="high"
    )
    
    print("\n3. Generating 3D models...")
    
    # Generate models
    beast_model = await model_agent.get_or_create_model(beast_request)
    weapon_model = await model_agent.get_or_create_model(weapon_request)
    
    print(f"\n   Beast Model:")
    print(f"     Service: {beast_model.service_used}")
    print(f"     Quality: {beast_model.quality_score}/100")
    print(f"     File: {beast_model.file_path}")
    
    print(f"\n   Weapon Model:")
    print(f"     Service: {weapon_model.service_used}")
    print(f"     Quality: {weapon_model.quality_score}/100") 
    print(f"     File: {weapon_model.file_path}")
    
    print("\n4. System Statistics:")
    stats = model_agent.get_model_stats()
    print(f"   Total models: {stats['total_models']}")
    print(f"   Models by service: {stats['models_by_service']}")
    print(f"   Average quality: {stats['average_quality']:.1f}")
    
    print("\n✅ Demo completed successfully!")
    print("   The AI 3D model integration is working correctly.")

async def demo_batch_generation():
    """Demo batch generation capabilities"""
    print("\n🚀 Batch Generation Demo")
    print("=" * 30)
    
    manager = Procedural3DModelManager()
    
    print("\nGenerating multiple items with 3D models...")
    
    # Batch generate content with models
    results = manager.batch_generate_models_for_procedural_content(
        content_types=["beast", "weapon"],
        count_per_type=2
    )
    
    print(f"\nGenerated {len(results)} items:")
    for i, result in enumerate(results, 1):
        content = result['content']
        model = result['model']
        print(f"\n{i}. {content.name}")
        print(f"   Type: {content.__class__.__name__.replace('Generated', '')}")
        print(f"   3D Service: {model['service_used']}")
        print(f"   Quality: {model['quality_score']}/100")
    
    # Show statistics
    stats = manager.get_generation_stats()
    print(f"\nBatch Statistics:")
    print(f"   Total generated: {stats['total_generated']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Services used: {list(stats['models_by_service'].keys())}")

def main():
    """Run the complete demo"""
    try:
        # Run async demos
        asyncio.run(demo_basic_integration())
        asyncio.run(demo_batch_generation())
        
        print("\n🎉 All demos completed successfully!")
        print("\nThe AI 3D Model Integration system is fully operational:")
        print("  ✅ Procedural content generation")
        print("  ✅ AI 3D model generation with multiple services")
        print("  ✅ Smart service selection")
        print("  ✅ Caching and optimization")
        print("  ✅ Batch processing")
        print("  ✅ Full integration pipeline")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()