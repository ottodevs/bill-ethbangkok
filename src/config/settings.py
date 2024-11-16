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

def load_config() -> Optional[OptimusConfig]:
    """Load configuration from environment and files."""
    # Ensure .bill directory exists
    BILL_HOME.mkdir(parents=True, exist_ok=True)
    
    path = BILL_HOME / "local_config.json"
    
    # If config exists, load it
    if path.exists():
        config = OptimusConfig.load(path)
    else:
        # Create new config
        config = OptimusConfig(
            path=path,
            allowed_chains=["base"],
            min_swap_amount_threshold=15,
            password_migrated=False,
            use_staking=False
        )

    print_section("API Key Configuration")

    # Get Base RPC URL
    if config.base_rpc is None:
        config.base_rpc = input("Please enter a Base RPC URL: ")
        from src.utils.web3_utils import check_rpc
        check_rpc(config.base_rpc)

    # Get Tenderly API Key
    if config.tenderly_access_key is None:
        config.tenderly_access_key = input(
            "Please enter your Tenderly API Key. Get one at https://dashboard.tenderly.co/: "
        )

    # Get Tenderly account and project if not set
    if config.tenderly_account_slug is None:
        config.tenderly_account_slug = input("Please enter your Tenderly account slug: ")
    
    if config.tenderly_project_slug is None:
        config.tenderly_project_slug = input("Please enter your Tenderly project slug: ")

    # Save configuration
    try:
        config.store()
    except Exception as e:
        print(f"Error saving configuration: {str(e)}")
        return None

    return config

    if config.allowed_chains is None:
        config.allowed_chains = ["base"]

    config.store()
    return config
