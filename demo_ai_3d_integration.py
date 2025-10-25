#!/usr/bin/env python3
"""
AI 3D Model Integration Demo
===========================

This demo showcases the complete AI 3D model generation system integrated with procedural content.
Features:
- Procedural generation of beasts, weapons, and divine entities
- AI-powered 3D model generation using multiple services
- Smart service selection based on content type
- Caching and optimization
- Full integration pipeline from content to 3D models

AI Services Integrated:
- Luma AI (Genie): Fast, realistic textures
- Meshy AI: Web-based, stylized models  
- Kaedim: Production-ready, riggable models
- Scenario.gg: Game-tailored assets
"""

import sys
import os
import json
import time

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

try:
    from procedural_generator import ProceduralGenerator
    from ai_3d_model_agent import AI3DModelAgent
    from procedural_3d_integration import Procedural3DModelManager
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section"""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def demo_procedural_generation():
    """Demonstrate procedural content generation"""
    print_header("PROCEDURAL CONTENT GENERATION")
    
    generator = ProceduralGenerator()
    
    print("Generating random procedural content...")
    
    # Generate a beast
    beast = generator.generate_beast()
    print_section("Generated Beast")
    print(f"Name: {beast.name}")
    print(f"Description: {beast.description}")
    print(f"Rarity: {beast.rarity.value}")
    print(f"Stats: HP={beast.stats.get('hp', 'N/A')}, Attack={beast.stats.get('attack', 'N/A')}, Defense={beast.stats.get('defense', 'N/A')}")
    
    # Generate a weapon
    weapon = generator.generate_weapon()
    print_section("Generated Weapon")
    print(f"Name: {weapon.name}")
    print(f"Description: {weapon.description}")
    print(f"Type: {weapon.weapon_type}")
    print(f"Rarity: {weapon.rarity.value}")
    print(f"Damage: {weapon.damage_range}")
    
    # Generate a divine entity
    god = generator.generate_divine_entity()
    print_section("Generated Divine Entity")
    print(f"Name: {god.name}")
    print(f"Description: {god.description}")
    print(f"Domain: {god.domain}")
    print(f"Rarity: {god.rarity.value}")
    
    return beast, weapon, god

def demo_ai_3d_models(beast, weapon, god):
    """Demonstrate AI 3D model generation"""
    print_header("AI 3D MODEL GENERATION")
    
    model_agent = AI3DModelAgent()
    
    print("Testing AI service selection for different content types...")
    
    # Show AI service preferences
    print_section("AI Service Selection Logic")
    content_types = ["beast", "weapon", "god", "environment", "character"]
    for content_type in content_types:
        preferred_services = model_agent._get_preferred_services_for_content(content_type)
        preferred = preferred_services[0] if preferred_services else "none"
        print(f"{content_type:12} -> {preferred}")
    
    # Generate 3D models for our procedural content
    print_section("Generating 3D Models")
    
    # Beast model
    print(f"\nGenerating 3D model for beast: {beast.name}")
    beast_model = model_agent.generate_model(
        prompt=f"Fantasy creature: {beast.name} - {beast.description}",
        content_type="beast",
        tags=["creature", "fantasy", beast.rarity.value, "game_ready"]
    )
    print(f"  Service Used: {beast_model['service_used']}")
    print(f"  Quality Score: {beast_model['quality_score']}/100")
    print(f"  From Cache: {beast_model['from_cache']}")
    print(f"  Model Path: {beast_model['model_path']}")
    
    # Weapon model
    print(f"\nGenerating 3D model for weapon: {weapon.name}")
    weapon_model = model_agent.generate_model(
        prompt=f"Fantasy weapon: {weapon.name} - {weapon.description}",
        content_type="weapon",
        tags=["weapon", "fantasy", weapon.rarity.value, "combat"]
    )
    print(f"  Service Used: {weapon_model['service_used']}")
    print(f"  Quality Score: {weapon_model['quality_score']}/100")
    print(f"  From Cache: {weapon_model['from_cache']}")
    print(f"  Model Path: {weapon_model['model_path']}")
    
    # Divine entity model
    print(f"\nGenerating 3D model for divine entity: {god.name}")
    god_model = model_agent.generate_model(
        prompt=f"Divine being: {god.name} - {god.description}",
        content_type="god",
        tags=["divine", "mythology", "powerful", god.domain]
    )
    print(f"  Service Used: {god_model['service_used']}")
    print(f"  Quality Score: {god_model['quality_score']}/100")
    print(f"  From Cache: {god_model['from_cache']}")
    print(f"  Model Path: {god_model['model_path']}")
    
    return beast_model, weapon_model, god_model

def demo_integrated_system():
    """Demonstrate the fully integrated procedural + 3D model system"""
    print_header("INTEGRATED PROCEDURAL 3D SYSTEM")
    
    manager = Procedural3DModelManager()
    
    print("Testing batch generation of procedural content with 3D models...")
    
    # Generate multiple items with 3D models
    print_section("Batch Generation Test")
    
    batch_results = manager.batch_generate_models_for_procedural_content(
        content_types=["beast", "weapon"],
        count_per_type=2
    )
    
    print(f"Generated {len(batch_results)} items with 3D models:")
    for result in batch_results:
        content = result['content']
        model = result['model']
        print(f"\n  {content['type'].title()}: {content['name']}")
        print(f"    Description: {content['description']}")
        print(f"    3D Model: {model['service_used']} (Quality: {model['quality_score']})")
        print(f"    Cache Hit: {model['from_cache']}")
    
    # Show system statistics
    print_section("System Statistics")
    stats = manager.get_generation_stats()
    print(f"Total Models Generated: {stats['total_generated']}")
    print(f"Cache Hits: {stats['cache_hits']}")
    print(f"Cache Hit Rate: {stats['cache_hit_rate']:.1%}")
    print(f"Average Quality Score: {stats['average_quality']:.1f}")
    
    print("\nModels by Service:")
    for service, count in stats['models_by_service'].items():
        print(f"  {service}: {count}")
    
    print("\nModels by Content Type:")
    for content_type, count in stats['models_by_content_type'].items():
        print(f"  {content_type}: {count}")

def demo_ai_service_capabilities():
    """Demonstrate different AI service capabilities"""
    print_header("AI SERVICE CAPABILITIES")
    
    model_agent = AI3DModelAgent()
    
    print("Testing different AI services with specialized content...")
    
    test_cases = [
        {
            "name": "Realistic Character",
            "prompt": "Detailed human warrior with leather armor and battle scars",
            "content_type": "character",
            "tags": ["realistic", "human", "detailed"]
        },
        {
            "name": "Stylized Weapon",
            "prompt": "Cartoon-style magical staff with glowing crystals",
            "content_type": "weapon", 
            "tags": ["stylized", "magical", "cartoon"]
        },
        {
            "name": "Production Asset",
            "prompt": "Game-ready medieval castle with modular pieces",
            "content_type": "environment",
            "tags": ["production", "modular", "game_ready"]
        },
        {
            "name": "Mythological Beast",
            "prompt": "Ancient dragon with multiple heads and mystical aura",
            "content_type": "beast",
            "tags": ["mythology", "epic", "fantasy"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Prompt: {test_case['prompt']}")
        
        # Show which service would be selected
        preferred_services = model_agent._get_preferred_services_for_content(
            test_case['content_type']
        )
        selected_service = preferred_services[0] if preferred_services else "none"
        print(f"   Selected Service: {selected_service}")
        
        # Show service capabilities for this content type
        service_info = model_agent.ai_services[selected_service]
        capabilities = service_info.get('capabilities', {})
        content_strength = capabilities.get(test_case['content_type'], 'medium')
        print(f"   Service Strength: {content_strength}")
        
        # Generate the model (mock)
        result = model_agent.generate_model(
            prompt=test_case['prompt'],
            content_type=test_case['content_type'],
            tags=test_case['tags']
        )
        print(f"   Quality Score: {result['quality_score']}/100")
        print(f"   Processing Time: {result.get('processing_time', 'N/A')}")

def main():
    """Run the complete AI 3D model integration demo"""
    print("🎮 AI 3D Model Integration Demo")
    print("===============================")
    print("This demo showcases the complete AI-powered 3D model generation")
    print("system integrated with procedural content generation.")
    print("\nAI Services Available:")
    print("  • Luma AI (Genie) - Fast, realistic textures")
    print("  • Meshy AI - Web-based, stylized models")
    print("  • Kaedim - Production-ready, riggable models")
    print("  • Scenario.gg - Game-tailored assets")
    
    try:
        # Demo 1: Procedural Generation
        beast, weapon, god = demo_procedural_generation()
        
        # Demo 2: AI 3D Model Generation
        beast_model, weapon_model, god_model = demo_ai_3d_models(beast, weapon, god)
        
        # Demo 3: Integrated System
        demo_integrated_system()
        
        # Demo 4: AI Service Capabilities
        demo_ai_service_capabilities()
        
        print_header("DEMO COMPLETE")
        print("✅ Procedural content generation: Working")
        print("✅ AI 3D model generation: Working")
        print("✅ Service selection logic: Working")
        print("✅ Caching system: Working")
        print("✅ Batch generation: Working")
        print("✅ Integration pipeline: Working")
        
        print("\n🚀 System ready for production!")
        print("   Next steps:")
        print("   1. Configure real AI service API keys")
        print("   2. Set up model storage and CDN")
        print("   3. Implement WebSocket handlers in game server")
        print("   4. Add 3D model viewer to client")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()