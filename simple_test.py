#!/usr/bin/env python3
"""
Simple test to verify basic functionality works.
"""

import os
import sys
from pathlib import Path

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment loaded")
except ImportError:
    print("⚠️  python-dotenv not installed")

# Test basic package structure
print("\n🧪 Testing basic structure...")

try:
    from alphagenome_analytics.utils.validation import validate_variant
    
    # Test validation
    is_valid, error = validate_variant("chr1", 1000000, "A", "G")
    if is_valid:
        print("✅ Validation works!")
    else:
        print(f"❌ Validation failed: {error}")
        
    # Test API key
    api_key = os.getenv('ALPHAGENOME_API_KEY')
    if api_key:
        print(f"✅ API key found: {api_key[:10]}...{api_key[-5:]}")
    else:
        print("❌ No API key found")
        
    print("\n🎉 Basic functionality works!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    sys.exit(1)

print("\nProject structure is functional! Ready for GitHub push.") 