#!/usr/bin/env python3
"""
Test script for MTA-STS policy validation
"""

import sys
import os
import subprocess
from pathlib import Path

def test_valid_policy():
    """Test with a valid policy file"""
    test_file = Path("tests/test-policy.txt")
    if test_file.exists():
        # Run the validation script as a subprocess
        result = subprocess.run([
            sys.executable, 
            "scripts/validate-policy.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Test policy validation passed")
            return True
        else:
            print("❌ Test policy validation failed")
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
            return False
    else:
        print("⚠️  Test policy file not found")
        return True

def test_invalid_policy():
    """Test with an invalid policy file"""
    # Create a temporary invalid policy
    invalid_policy = """version: STSv1
mode: invalid_mode
mx: *.example.com
max_age: 999999"""
    
    test_file = Path("tests/invalid-policy.txt")
    with open(test_file, 'w') as f:
        f.write(invalid_policy)
    
    try:
        # Run validation on the invalid policy
        result = subprocess.run([
            sys.executable, 
            "scripts/validate-policy.py"
        ], capture_output=True, text=True, cwd="tests")
        
        if result.returncode != 0:
            print("✅ Invalid policy correctly rejected")
            return True
        else:
            print("❌ Invalid policy should have been rejected")
            return False
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()

def main():
    """Run all tests"""
    print("🧪 Running MTA-STS validation tests...")
    
    tests = [
        test_valid_policy,
        test_invalid_policy
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
