#!/usr/bin/env python3
"""
Test all game modules to ensure they work correctly.
Uses ASCII-safe output for terminal compatibility.
"""

import sys
import traceback
import importlib
import os


def test_module(module_name, module_path=None):
    """Test importing and basic functionality of a module."""
    print(f"Testing {module_name}...")
    try:
        if module_path:
            # Add the directory to Python path if needed
            sys.path.insert(0, module_path)
        
        module = importlib.import_module(module_name)
        print(f"  PASS: {module_name} imported successfully")
        
        # Test basic functionality if available
        if hasattr(module, 'test_functionality'):
            module.test_functionality()
            print(f"  PASS: {module_name} functionality test passed")
        
        return True
    except Exception as e:
        print(f"  FAIL: {module_name} - {str(e)}")
        print(f"  Error details: {traceback.format_exc()}")
        return False


def main():
    """Run all module tests."""
    print("Ancient Bharat Game Platform - Module Testing")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Add server directory to path
    server_dir = os.path.join(project_dir, 'server')
    sys.path.insert(0, server_dir)
    
    # Test core modules
    modules_to_test = [
        'ancient_bharat_config',
        'ancient_bharat_npcs',
        'ancient_bharat_quests',
        'ancient_bharat_world',
        'integrated_ancient_bharat_server'
    ]
    
    passed = 0
    failed = 0
    
    for module in modules_to_test:
        if test_module(module):
            passed += 1
        else:
            failed += 1
        print()
    
    # Test simple server (top level)
    sys.path.insert(0, project_dir)
    if test_module('simple_game_server'):
        passed += 1
    else:
        failed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed} PASSED, {failed} FAILED")
    
    if failed == 0:
        print("All modules are working correctly!")
        return 0
    else:
        print("Some modules have issues that need fixing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())