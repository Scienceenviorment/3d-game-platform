#!/usr/bin/env python3
"""
Mass 3D Model Generation Script
==============================

This script generates as many 3D models as possible using the AI 3D model integration system.
It will test all AI services and generate models for all types of procedural content.
"""

import sys
import os
import asyncio
import time
from typing import List, Dict, Any

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

try:
    from procedural_generator import ProceduralGenerator, ContentRarity
    from ai_3d_model_agent import AI3DModelAgent, ModelRequest
    from procedural_3d_integration import Procedural3DModelManager
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class Mass3DGenerator:
    """Mass generator for 3D models using procedural content"""
    
    def __init__(self):
        self.procedural_gen = ProceduralGenerator()
        self.model_agent = AI3DModelAgent()
        self.integration_manager = Procedural3DModelManager()
        self.generation_stats = {
            'total_attempts': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'cached_hits': 0,
            'by_service': {},
            'by_content_type': {},
            'by_rarity': {},
            'start_time': time.time()
        }
    
    def print_header(self, title: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_progress(self, current: int, total: int, item_name: str):
        """Print generation progress"""
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r[{bar}] {percentage:.1f}% ({current}/{total}) - {item_name[:30]}", end='', flush=True)
    
    async def generate_beast_models(self, count: int = 20) -> List[Dict]:
        """Generate 3D models for procedural beasts"""
        self.print_header(f"GENERATING {count} BEAST 3D MODELS")
        results = []
        
        for i in range(count):
            try:
                # Generate procedural beast
                beast = self.procedural_gen.generate_beast()
                self.print_progress(i + 1, count, beast.name)
                
                # Create model request
                request = ModelRequest(
                    content_name=beast.name,
                    content_type="beast",
                    content_description=f"Fantasy creature: {beast.name} - {beast.description}",
                    style_preferences={"tags": ["creature", "fantasy", beast.rarity.value]},
                    quality_level="high"
                )
                
                # Generate model
                model = await self.model_agent.get_or_create_model(request)
                if model:
                    results.append({
                        'content': beast,
                        'model': model,
                        'type': 'beast'
                    })
                    self.update_stats(model, 'beast', beast.rarity)
                
            except Exception as e:
                self.generation_stats['failed_generations'] += 1
                print(f"\n❌ Failed to generate beast model: {e}")
        
        print()  # New line after progress bar
        return results
    
    async def generate_weapon_models(self, count: int = 20) -> List[Dict]:
        """Generate 3D models for procedural weapons"""
        self.print_header(f"GENERATING {count} WEAPON 3D MODELS")
        results = []
        
        for i in range(count):
            try:
                # Generate procedural weapon
                weapon = self.procedural_gen.generate_weapon()
                self.print_progress(i + 1, count, weapon.name)
                
                # Create model request
                request = ModelRequest(
                    content_name=weapon.name,
                    content_type="weapon",
                    content_description=f"Fantasy weapon: {weapon.name} - {weapon.description}",
                    style_preferences={"tags": ["weapon", "fantasy", weapon.rarity.value]},
                    quality_level="high"
                )
                
                # Generate model
                model = await self.model_agent.get_or_create_model(request)
                if model:
                    results.append({
                        'content': weapon,
                        'model': model,
                        'type': 'weapon'
                    })
                    self.update_stats(model, 'weapon', weapon.rarity)
                
            except Exception as e:
                self.generation_stats['failed_generations'] += 1
                print(f"\n❌ Failed to generate weapon model: {e}")
        
        print()  # New line after progress bar
        return results
    
    async def generate_divine_models(self, count: int = 15) -> List[Dict]:
        """Generate 3D models for divine entities"""
        self.print_header(f"GENERATING {count} DIVINE ENTITY 3D MODELS")
        results = []
        
        for i in range(count):
            try:
                # Generate procedural divine entity
                god = self.procedural_gen.generate_divine_entity()
                self.print_progress(i + 1, count, god.name)
                
                # Create model request
                request = ModelRequest(
                    content_name=god.name,
                    content_type="god",
                    content_description=f"Divine being: {god.name} - {god.description}",
                    style_preferences={"tags": ["divine", "mythology", god.domain]},
                    quality_level="ultra"
                )
                
                # Generate model
                model = await self.model_agent.get_or_create_model(request)
                if model:
                    results.append({
                        'content': god,
                        'model': model,
                        'type': 'divine_entity'
                    })
                    self.update_stats(model, 'divine_entity', god.rarity)
                
            except Exception as e:
                self.generation_stats['failed_generations'] += 1
                print(f"\n❌ Failed to generate divine model: {e}")
        
        print()  # New line after progress bar
        return results
    
    async def generate_job_class_models(self, count: int = 10) -> List[Dict]:
        """Generate 3D models for job classes (characters)"""
        self.print_header(f"GENERATING {count} JOB CLASS CHARACTER 3D MODELS")
        results = []
        
        for i in range(count):
            try:
                # Generate procedural job class
                job_class = self.procedural_gen.generate_job_class()
                self.print_progress(i + 1, count, job_class.name)
                
                # Create model request
                request = ModelRequest(
                    content_name=job_class.name,
                    content_type="character",
                    content_description=f"Fantasy character: {job_class.name} - {job_class.description}",
                    style_preferences={"tags": ["character", "fantasy", job_class.role]},
                    quality_level="high"
                )
                
                # Generate model
                model = await self.model_agent.get_or_create_model(request)
                if model:
                    results.append({
                        'content': job_class,
                        'model': model,
                        'type': 'character'
                    })
                    self.update_stats(model, 'character', job_class.rarity)
                
            except Exception as e:
                self.generation_stats['failed_generations'] += 1
                print(f"\n❌ Failed to generate character model: {e}")
        
        print()  # New line after progress bar
        return results
    
    def update_stats(self, model, content_type: str, rarity):
        """Update generation statistics"""
        self.generation_stats['total_attempts'] += 1
        self.generation_stats['successful_generations'] += 1
        
        # Track by service (use source instead of service_used)
        service = getattr(model, 'source', 'unknown')
        if hasattr(service, 'value'):
            service = service.value
        service = str(service)
        
        if service not in self.generation_stats['by_service']:
            self.generation_stats['by_service'][service] = 0
        self.generation_stats['by_service'][service] += 1
        
        # Track by content type
        if content_type not in self.generation_stats['by_content_type']:
            self.generation_stats['by_content_type'][content_type] = 0
        self.generation_stats['by_content_type'][content_type] += 1
        
        # Track by rarity
        rarity_str = rarity.value if hasattr(rarity, 'value') else str(rarity)
        if rarity_str not in self.generation_stats['by_rarity']:
            self.generation_stats['by_rarity'][rarity_str] = 0
        self.generation_stats['by_rarity'][rarity_str] += 1
    
    async def test_all_ai_services(self):
        """Test each AI service with different content types"""
        self.print_header("TESTING ALL AI SERVICES")
        
        test_cases = [
            {
                'name': 'Luma AI Test - Realistic Beast',
                'content_type': 'beast',
                'description': 'A majestic dragon with realistic scales and lighting'
            },
            {
                'name': 'Meshy AI Test - Stylized Weapon',
                'content_type': 'weapon',
                'description': 'A cartoon-style magical sword with glowing runes'
            },
            {
                'name': 'Kaedim Test - Production Character',
                'content_type': 'character',
                'description': 'A game-ready warrior with detailed armor'
            },
            {
                'name': 'Scenario.gg Test - Game Asset',
                'content_type': 'environment',
                'description': 'A fantasy castle environment piece'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}")
            
            try:
                request = ModelRequest(
                    content_name=f"Test_{test_case['content_type']}_{i}",
                    content_type=test_case['content_type'],
                    content_description=test_case['description'],
                    style_preferences={"tags": ["test", "ai_service"]},
                    quality_level="high"
                )
                
                model = await self.model_agent.get_or_create_model(request)
                if model:
                    service_info = getattr(model, 'source', 'unknown')
                    if hasattr(service_info, 'value'):
                        service_info = service_info.value
                    print(f"   ✅ Generated successfully with {service_info}")
                    self.update_stats(model, test_case['content_type'], 
                                    ContentRarity.COMMON)
                else:
                    print(f"   ❌ Generation failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def print_final_statistics(self):
        """Print comprehensive generation statistics"""
        self.print_header("MASS GENERATION STATISTICS")
        
        elapsed_time = time.time() - self.generation_stats['start_time']
        
        print(f"🕒 Total Generation Time: {elapsed_time:.1f} seconds")
        print(f"📊 Total Attempts: {self.generation_stats['total_attempts']}")
        print(f"✅ Successful Generations: {self.generation_stats['successful_generations']}")
        print(f"❌ Failed Generations: {self.generation_stats['failed_generations']}")
        print(f"💾 Cache Hits: {self.generation_stats['cached_hits']}")
        
        if self.generation_stats['total_attempts'] > 0:
            success_rate = (self.generation_stats['successful_generations'] / self.generation_stats['total_attempts']) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
            
            avg_time = elapsed_time / self.generation_stats['total_attempts']
            print(f"⚡ Average Generation Time: {avg_time:.2f} seconds per model")
        
        print(f"\n🤖 Models by AI Service:")
        for service, count in self.generation_stats['by_service'].items():
            print(f"   {service}: {count}")
        
        print(f"\n📦 Models by Content Type:")
        for content_type, count in self.generation_stats['by_content_type'].items():
            print(f"   {content_type}: {count}")
        
        print(f"\n💎 Models by Rarity:")
        for rarity, count in self.generation_stats['by_rarity'].items():
            print(f"   {rarity}: {count}")
        
        # Get agent statistics
        agent_stats = self.model_agent.get_model_stats()
        print(f"\n🗂️ Total Models in Cache: {agent_stats['total_models']}")
        print(f"🎯 Average Quality Score: {agent_stats['average_quality']:.1f}")


async def main():
    """Run mass 3D model generation"""
    print("🚀 Mass 3D Model Generation System")
    print("==================================")
    print("Generating maximum number of 3D models using AI services")
    print("Services: Luma AI, Meshy AI, Kaedim, Scenario.gg")
    
    generator = Mass3DGenerator()
    all_results = []
    
    try:
        # Test AI services first
        await generator.test_all_ai_services()
        
        # Generate different types of content
        beast_results = await generator.generate_beast_models(25)  # 25 beasts
        all_results.extend(beast_results)
        
        weapon_results = await generator.generate_weapon_models(25)  # 25 weapons
        all_results.extend(weapon_results)
        
        divine_results = await generator.generate_divine_models(20)  # 20 divine entities
        all_results.extend(divine_results)
        
        character_results = await generator.generate_job_class_models(15)  # 15 characters
        all_results.extend(character_results)
        
        # Print final statistics
        generator.print_final_statistics()
        
        print(f"\n🎉 MASS GENERATION COMPLETE!")
        print(f"Generated {len(all_results)} total 3D models")
        print(f"Content breakdown:")
        print(f"  🐉 Beasts: {len(beast_results)}")
        print(f"  ⚔️ Weapons: {len(weapon_results)}")
        print(f"  👑 Divine Entities: {len(divine_results)}")
        print(f"  🧙 Characters: {len(character_results)}")
        
        print(f"\n📁 All models stored in: game_data/3d_models/")
        print(f"🎮 Ready for use in your 3D game platform!")
        
    except KeyboardInterrupt:
        print(f"\n🛑 Generation interrupted by user")
        generator.print_final_statistics()
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())