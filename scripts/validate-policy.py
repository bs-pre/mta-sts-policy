#!/usr/bin/env python3
"""
MTA-STS Policy Validator

This script validates MTA-STS policy files for syntax and best practices.
"""

import re
import sys
from pathlib import Path


def validate_policy(file_path):
    """Validate an MTA-STS policy file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the policy
        lines = content.strip().split('\n')
        policy = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                policy[key.strip()] = value.strip()
        
        # Validate required fields
        required_fields = ['version', 'mode', 'mx', 'max_age']
        missing_fields = []
        
        for field in required_fields:
            if field not in policy:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        # Validate version
        if policy['version'] != 'STSv1':
            print(f"❌ Invalid version: {policy['version']} (must be STSv1)")
            return False
        
        # Validate mode
        valid_modes = ['testing', 'enforce']
        if policy['mode'] not in valid_modes:
            print(f"❌ Invalid mode: {policy['mode']} (must be testing or enforce)")
            return False
        
        # Validate max_age
        try:
            max_age = int(policy['max_age'])
            if max_age < 300 or max_age > 86400:
                print(f"❌ Invalid max_age: {max_age} (must be between 300 and 86400 seconds)")
                return False
        except ValueError:
            print(f"❌ Invalid max_age: {policy['max_age']} (must be a number)")
            return False
        
        print("✅ Policy validation passed!")
        print(f"   Version: {policy['version']}")
        print(f"   Mode: {policy['mode']}")
        print(f"   MX: {policy['mx']}")
        print(f"   Max Age: {policy['max_age']} seconds")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False


def main():
    """Main function."""
    policy_file = Path('.well-known/mta-sts.txt')
    
    if not policy_file.exists():
        print("❌ Policy file not found at .well-known/mta-sts.txt")
        sys.exit(1)
    
    success = validate_policy(policy_file)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
