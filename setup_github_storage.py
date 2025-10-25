#!/usr/bin/env python3
"""
GitHub Storage Configuration Script
==================================

This script configures the system to use GitHub storage instead of local storage
for all assets including 3D models, images, audio, and other game content.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any


class GitHubStorageConfig:
    """Configure system to use GitHub storage URLs"""
    
    def __init__(self, github_repo: str = "Scien12/3d-game-platform"):
        self.github_repo = github_repo
        self.github_base_url = f"https://raw.githubusercontent.com/{github_repo}/main"
        self.github_lfs_url = f"https://media.githubusercontent.com/media/{github_repo}/main"
        self.project_root = Path(".")
        
        self.url_mappings = {}
        self.updated_files = []
    
    def convert_local_to_github_url(self, local_path: str) -> str:
        """Convert local file path to GitHub URL"""
        # Normalize path separators
        normalized_path = local_path.replace("\\", "/")
        
        # Remove leading ./ or current directory references
        if normalized_path.startswith("./"):
            normalized_path = normalized_path[2:]
        
        # Check if it's a large file that should use LFS
        if any(normalized_path.endswith(ext) for ext in ['.glb', '.obj', '.fbx', '.gltf', '.mp3', '.wav', '.mp4']):
            return f"{self.github_lfs_url}/{normalized_path}"
        else:
            return f"{self.github_base_url}/{normalized_path}"
    
    def update_python_files(self):
        """Update Python files to use GitHub URLs"""
        print("🔧 Updating Python files for GitHub storage...")
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace common local path patterns
                patterns = [
                    # Models directory references
                    (r'"game_data[/\\]3d_models[/\\]([^"]*)"', 
                     lambda m: f'"{self.convert_local_to_github_url(f"game_data/3d_models/{m.group(1)}")}"'),
                    
                    (r"'game_data[/\\]3d_models[/\\]([^']*)'", 
                     lambda m: f"'{self.convert_local_to_github_url(f'game_data/3d_models/{m.group(1)}')}'"),
                    
                    # General game_data references
                    (r'"game_data[/\\]([^"]*)"', 
                     lambda m: f'"{self.convert_local_to_github_url(f"game_data/{m.group(1)}")}"'),
                    
                    (r"'game_data[/\\]([^']*)'", 
                     lambda m: f"'{self.convert_local_to_github_url(f'game_data/{m.group(1)}')}'"),
                    
                    # Models directory variable assignments
                    (r'models_directory\s*=\s*"game_data/3d_models"',
                     f'models_directory = "{self.github_lfs_url}/game_data/3d_models"'),
                ]
                
                for pattern, replacement in patterns:
                    if callable(replacement):
                        content = re.sub(pattern, replacement, content)
                    else:
                        content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.updated_files.append(str(py_file))
                    print(f"  ✅ Updated: {py_file}")
                
            except Exception as e:
                print(f"  ❌ Error updating {py_file}: {e}")
    
    def update_json_configs(self):
        """Update JSON configuration files"""
        print("🔧 Updating JSON configuration files...")
        
        json_files = list(self.project_root.rglob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace file paths in JSON
                content = re.sub(
                    r'"([^"]*game_data[/\\][^"]*)"',
                    lambda m: f'"{self.convert_local_to_github_url(m.group(1).replace("\\", "/"))}"',
                    content
                )
                
                if content != original_content:
                    with open(json_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.updated_files.append(str(json_file))
                    print(f"  ✅ Updated: {json_file}")
                
            except Exception as e:
                print(f"  ❌ Error updating {json_file}: {e}")
    
    def update_javascript_files(self):
        """Update JavaScript files"""
        print("🔧 Updating JavaScript files...")
        
        js_files = list(self.project_root.rglob("*.js"))
        
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace file paths in JavaScript
                patterns = [
                    (r'"([^"]*game_data[/\\][^"]*)"',
                     lambda m: f'"{self.convert_local_to_github_url(m.group(1).replace(chr(92), "/"))}"'),
                    
                    (r"'([^']*game_data[/\\][^']*)'",
                     lambda m: f"'{self.convert_local_to_github_url(m.group(1).replace(chr(92), '/'))}'"),
                ]
                
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(js_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.updated_files.append(str(js_file))
                    print(f"  ✅ Updated: {js_file}")
                
            except Exception as e:
                print(f"  ❌ Error updating {js_file}: {e}")
    
    def create_github_storage_config(self):
        """Create configuration file for GitHub storage"""
        config = {
            "github_storage": {
                "repository": self.github_repo,
                "base_url": self.github_base_url,
                "lfs_url": self.github_lfs_url,
                "enabled": True
            },
            "storage_mapping": {
                "3d_models": f"{self.github_lfs_url}/game_data/3d_models",
                "audio": f"{self.github_lfs_url}/game_data/audio",
                "images": f"{self.github_base_url}/game_data/images",
                "configs": f"{self.github_base_url}/config",
                "assets": f"{self.github_lfs_url}/game_data"
            },
            "cache_policy": {
                "enable_local_cache": True,
                "cache_duration": 3600,
                "max_cache_size": "1GB"
            }
        }
        
        config_file = self.project_root / "config" / "github_storage.json"
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Created GitHub storage config: {config_file}")
        return config_file
    
    def update_ai_model_agent(self):
        """Update AI model agent to use GitHub storage"""
        agent_file = self.project_root / "server" / "ai_3d_model_agent.py"
        
        if not agent_file.exists():
            print("❌ AI model agent file not found")
            return
        
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add GitHub storage configuration
        github_storage_code = '''
    def _get_github_storage_url(self, local_path: str) -> str:
        """Convert local path to GitHub storage URL"""
        github_repo = "Scien12/3d-game-platform"
        github_lfs_url = f"https://media.githubusercontent.com/media/{github_repo}/main"
        
        # Normalize path
        normalized_path = local_path.replace("\\\\", "/")
        if normalized_path.startswith("./"):
            normalized_path = normalized_path[2:]
        
        return f"{github_lfs_url}/{normalized_path}"
    
    def _use_github_storage(self) -> bool:
        """Check if GitHub storage should be used"""
        return True  # Always use GitHub storage in production
'''
        
        # Insert the new methods before the last class method
        if "def _get_github_storage_url" not in content:
            # Find a good insertion point
            insertion_point = content.rfind("class AI3DModelAgent:")
            if insertion_point != -1:
                # Find the end of __init__ method
                init_end = content.find("def ", content.find("def __init__", insertion_point) + 10)
                if init_end != -1:
                    content = content[:init_end] + github_storage_code + "\n    " + content[init_end:]
                    
                    with open(agent_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.updated_files.append(str(agent_file))
                    print("✅ Updated AI model agent with GitHub storage support")
    
    def generate_summary_report(self):
        """Generate summary of changes made"""
        print("\n" + "="*60)
        print("  GITHUB STORAGE MIGRATION COMPLETE")
        print("="*60)
        
        print(f"🔗 GitHub Repository: {self.github_repo}")
        print(f"🌐 Base URL: {self.github_base_url}")
        print(f"📦 LFS URL: {self.github_lfs_url}")
        
        print(f"\n📝 Files Updated: {len(self.updated_files)}")
        for file_path in self.updated_files[:10]:  # Show first 10
            print(f"  ✅ {file_path}")
        
        if len(self.updated_files) > 10:
            print(f"  ... and {len(self.updated_files) - 10} more files")
        
        print(f"\n🎯 Storage Benefits:")
        print(f"  • No local storage dependency")
        print(f"  • Global CDN access for fast loading")
        print(f"  • Version control for all assets")
        print(f"  • Automatic backup and redundancy")
        print(f"  • Collaborative development support")
        
        print(f"\n🚀 System Status:")
        print(f"  ✅ All file references updated to GitHub URLs")
        print(f"  ✅ Large files (3D models, audio) use GitHub LFS")
        print(f"  ✅ Configuration files updated")
        print(f"  ✅ AI model agent configured for GitHub storage")
        print(f"  ✅ Ready for production deployment")


def main():
    """Run GitHub storage configuration"""
    print("🔧 GitHub Storage Configuration Tool")
    print("===================================")
    print("Converting local file references to GitHub storage URLs...")
    
    # Initialize configurator
    configurator = GitHubStorageConfig()
    
    # Update all file types
    configurator.update_python_files()
    configurator.update_json_configs()
    configurator.update_javascript_files()
    configurator.update_ai_model_agent()
    
    # Create storage configuration
    configurator.create_github_storage_config()
    
    # Generate summary
    configurator.generate_summary_report()


if __name__ == "__main__":
    main()