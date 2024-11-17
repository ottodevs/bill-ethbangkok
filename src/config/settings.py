# -*- coding: utf-8 -*-
"""Configuration settings."""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from dotenv import load_dotenv
from operate.resource import LocalResource, deserialize
from src.config.constants import BILL_HOME
from src.utils.formatting import print_section

@dataclass
class OptimusConfig(LocalResource):
    """Configuration class for the Bill yield agent."""
    path: Path
    base_rpc: Optional[str] = None
    tenderly_access_key: Optional[str] = None
    tenderly_account_slug: Optional[str] = None
    tenderly_project_slug: Optional[str] = None
    coingecko_api_key: Optional[str] = None
    min_swap_amount_threshold: Optional[int] = None
    password_migrated: Optional[bool] = None
    use_staking: Optional[bool] = None
    allowed_chains: Optional[List[str]] = None

    def store(self) -> None:
        """Store configuration to file."""
        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dictionary
        config_dict = {
            "path": str(self.path),
            "base_rpc": self.base_rpc,
            "tenderly_access_key": self.tenderly_access_key,
            "tenderly_account_slug": self.tenderly_account_slug,
            "tenderly_project_slug": self.tenderly_project_slug,
            "coingecko_api_key": self.coingecko_api_key,
            "min_swap_amount_threshold": self.min_swap_amount_threshold,
            "password_migrated": self.password_migrated,
            "use_staking": self.use_staking,
            "allowed_chains": self.allowed_chains
        }
        
        # Write to file
        with open(self.path, 'w') as f:
            json.dump(config_dict, f, indent=2)

class Config:
    def __init__(self, path: Path):
        self.path = path
        self._data: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load config from file if it exists."""
        if self.path.exists():
            with open(self.path, "r") as f:
                self._data = json.load(f)
    
    def store(self) -> None:
        """Store config to file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=4)
    
    def __getattr__(self, name: str) -> Any:
        """Get config value."""
        return self._data.get(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set config value."""
        if name in ["path", "_data"]:
            super().__setattr__(name, value)
        else:
            self._data[name] = value

def load_config() -> Optional[Config]:
    """Load configuration."""
    config_path = Path.home() / ".bill" / "config.json"
    return Config(config_path)

def save_config(config: Any) -> bool:
    """Save configuration to file."""
    try:
        config_file = Path(".bill") / "config" / "config.json"
        
        # Convertir el objeto config a dict
        config_dict = {k: v for k, v in config.__dict__.items()}
        
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=4)
        
        return True
    
    except Exception as e:
        print(f"Error saving configuration: {str(e)}")
        return False
