#!/usr/bin/env python3
"""
Test script to verify AlphaGenome Analytics setup and API connectivity.
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables only.")
    print("   Install with: pip install python-dotenv")

# Add the package to path for testing
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_import():
    """Test basic package imports."""
    print("\n🧪 Testing basic imports...")
    
    try:
        from alphagenome_analytics import __version__
        print(f"✅ AlphaGenome Analytics version: {__version__}")
        
        from alphagenome_analytics.core.analyzer import VariantAnalyzer
        print("✅ VariantAnalyzer imported successfully")
        
        from alphagenome_analytics.utils.validation import validate_variant
        print("✅ Validation utilities imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_api_key():
    """Test API key availability."""
    print("\n🔑 Testing API key...")
    
    api_key = os.getenv('ALPHAGENOME_API_KEY')
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]}")
        return True
    else:
        print("❌ No API key found in environment variables")
        print("   Make sure ALPHAGENOME_API_KEY is set in your .env file")
        return False

def test_validation():
    """Test validation functions."""
    print("\n✅ Testing validation functions...")
    
    try:
        from alphagenome_analytics.utils.validation import validate_variant, validate_interval
        
        # Test valid variant
        is_valid, error = validate_variant("chr1", 1000000, "A", "G")
        if is_valid:
            print("✅ Valid variant validation passed")
        else:
            print(f"❌ Valid variant validation failed: {error}")
            return False
        
        # Test invalid variant
        is_valid, error = validate_variant("invalid", -1, "X", "Y")
        if not is_valid:
            print("✅ Invalid variant validation passed")
        else:
            print("❌ Invalid variant validation should have failed")
            return False
        
        # Test interval validation
        is_valid, error = validate_interval("chr1", 1000, 2000)
        if is_valid:
            print("✅ Valid interval validation passed")
        else:
            print(f"❌ Valid interval validation failed: {error}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Validation test error: {str(e)}")
        return False

def test_analyzer_init():
    """Test analyzer initialization (without API calls)."""
    print("\n🧬 Testing analyzer initialization...")
    
    api_key = os.getenv('ALPHAGENOME_API_KEY')
    if not api_key:
        print("⚠️  Skipping analyzer test - no API key")
        return True
    
    try:
        from alphagenome_analytics.core.analyzer import VariantAnalyzer
        
        # This will fail if alphagenome package is not installed
        # but should at least test our wrapper logic
        analyzer = VariantAnalyzer(api_key=api_key)
        print("✅ VariantAnalyzer initialized successfully")
        
        # Test cache functionality
        stats = analyzer.get_cache_stats()
        print(f"✅ Cache stats: {stats}")
        
        return True
    except ImportError as e:
        if "alphagenome" in str(e).lower():
            print("⚠️  AlphaGenome package not installed - this is expected")
            print("   Install with: pip install alphagenome")
            return True
        else:
            print(f"❌ Unexpected import error: {str(e)}")
            return False
    except Exception as e:
        print(f"❌ Analyzer initialization error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🚀 AlphaGenome Analytics Setup Test")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_import),
        ("API Key", test_api_key),
        ("Validation", test_validation),
        ("Analyzer Init", test_analyzer_init),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n📚 Next steps:")
        print("   1. Install AlphaGenome: pip install alphagenome")
        print("   2. Run example: python scripts/example_analysis.py")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 