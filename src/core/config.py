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
        "theme": "light",
        "font_size": 12,
        "accent_color": "#007AFF",
        "graph_color_palette": "viridis",
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
                    cls._instance = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in cls._default_config.items():
                    if key not in cls._instance:
                        cls._instance[key] = value
            except Exception as e:
                print(f"Error loading config: {e}")
                cls._instance = cls._default_config.copy()
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
