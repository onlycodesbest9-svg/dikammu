"""
Quick script to fix config file
Run this if you get config errors
"""

import os
import json
from pathlib import Path

# Find config file
documents = Path.home() / "Documents"
config_dir = documents / "RecursiveLearn_Data"
config_file = config_dir / "config.json"

print("=" * 60)
print("RecursiveLearn Config Fixer")
print("=" * 60)
print()

if config_file.exists():
    print(f"Found config file: {config_file}")
    print("Deleting old config...")
    
    try:
        os.remove(config_file)
        print("✅ Old config deleted successfully!")
        print()
        print("The app will create a fresh config on next launch.")
    except Exception as e:
        print(f"❌ Error deleting config: {e}")
        print()
        print("You can manually delete it:")
        print(f"  {config_file}")
else:
    print("No config file found. You're good to go!")

print()
print("=" * 60)
print("Now run: python main.py")
print("=" * 60)
