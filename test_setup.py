#!/usr/bin/env python3
"""
Test script to verify OpenVoice setup
"""

import os
import sys
import torch

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from openvoice import se_extractor
        print("✓ openvoice.se_extractor imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import openvoice.se_extractor: {e}")
        return False
    
    try:
        from openvoice.api import ToneColorConverter
        print("✓ openvoice.api.ToneColorConverter imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import openvoice.api.ToneColorConverter: {e}")
        return False
    
    return True

def test_checkpoints():
    """Test if checkpoint files exist"""
    print("\nTesting checkpoint files...")
    
    required_files = [
        'checkpoints_v2/converter/config.json',
        'checkpoints_v2/converter/checkpoint.pth'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_torch():
    """Test PyTorch installation"""
    print("\nTesting PyTorch...")
    
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU count: {torch.cuda.device_count()}")
    
    return True

def test_model_loading():
    """Test if models can be loaded"""
    print("\nTesting model loading...")
    
    try:
        from openvoice.api import ToneColorConverter
        
        device = "cpu"
        config_path = 'checkpoints_v2/converter/config.json'
        checkpoint_path = 'checkpoints_v2/converter/checkpoint.pth'
        
        print("Loading tone color converter...")
        tone_color_converter = ToneColorConverter(config_path, device=device)
        tone_color_converter.load_ckpt(checkpoint_path)
        print("✓ Models loaded successfully")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load models: {e}")
        return False

def main():
    """Run all tests"""
    print("OpenVoice Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Checkpoints", test_checkpoints),
        ("PyTorch", test_torch),
        ("Model Loading", test_model_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"✗ {test_name} test failed")
        except Exception as e:
            print(f"✗ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! OpenVoice is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 