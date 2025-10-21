"""
Configuration and Settings Management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Application configuration manager"""
    
    _instance = None
    _data_dir = None
    _config_file = None
    _default_config = {
        "theme": "dark",  # Default to dark mode
        "instructor_pin": "1234",
        "current_user": None,
        "user_mode": "student",  # "student" or "instructor"
        "window_geometry": None,
        "first_run": True
    }
    
    @classmethod
    def initialize(cls):
        """Initialize configuration directory and load settings"""
        if cls._instance is None:
            cls._instance = {}
            
            # Set up data directory in user's Documents folder
            documents_dir = Path.home() / "Documents"
            cls._data_dir = documents_dir / "RecursiveLearn_Data"
            cls._data_dir.mkdir(parents=True, exist_ok=True)
            
            cls._config_file = cls._data_dir / "config.json"
            cls._load_config()
    
    @classmethod
    def _load_config(cls):
        """Load configuration from file or create default"""
        if cls._config_file.exists():
            try:
                with open(cls._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Start with defaults and update with loaded values
                cls._instance = cls._default_config.copy()
                
                # Only keep keys that exist in defaults (ignore old keys)
                for key in cls._default_config.keys():
                    if key in loaded_config:
                        cls._instance[key] = loaded_config[key]
                
                # Save the cleaned config
                cls.save()
            except Exception as e:
                print(f"Error loading config: {e}")
                print("Creating new config with defaults...")
                cls._instance = cls._default_config.copy()
                cls.save()
        else:
            cls._instance = cls._default_config.copy()
            cls.save()
    
    @classmethod
    def save(cls):
        """Save configuration to file"""
        try:
            with open(cls._config_file, 'w', encoding='utf-8') as f:
                json.dump(cls._instance, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return cls._instance.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any):
        """Set configuration value and save"""
        cls._instance[key] = value
        cls.save()
    
    @classmethod
    def get_data_dir(cls) -> Path:
        """Get the data directory path"""
        return cls._data_dir
    
    @classmethod
    def reset(cls):
        """Reset configuration to defaults"""
        cls._instance = cls._default_config.copy()
        cls.save()
