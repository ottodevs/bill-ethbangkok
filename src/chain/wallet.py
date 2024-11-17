# -*- coding: utf-8 -*-
"""Wallet setup and management."""

import sys
import getpass
import json
from pathlib import Path
from typing import Optional, Tuple, List
from eth_account import Account
from web3 import Web3

from src.config.settings import Config

class Wallet:
    """Wallet class for managing accounts and keys."""
    
    def __init__(self, private_key: str, address: str):
        self.account = Account.from_key(private_key)
        self.address = address
        self._password: Optional[str] = None
    
    @property
    def password(self) -> Optional[str]:
        return self._password
    
    @password.setter
    def password(self, value: str) -> None:
        self._password = value

    @classmethod
    def new(cls, password: str, path: Path) -> Tuple["Wallet", List[str]]:
        """Create a new wallet with mnemonic."""
        # Backport support on aea
        account = Account()
        account.enable_unaudited_hdwallet_features()
        crypto = account.create()
        
        # Store encrypted wallet
        keystore = Account.encrypt(
            private_key=crypto.key,
            password=password
        )
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(keystore, f, indent=2)
            
        return cls(crypto.key.hex(), crypto.address), []  # Empty mnemonic list for now

def setup_wallet(config: Config) -> Optional[Wallet]:
    """Setup wallet."""
    try:
        wallet_path = Path.home() / ".bill" / "wallet.json"
        
        if not wallet_path.exists():
            print("\nCreating new wallet...")
            wallet, _ = Wallet.new(config.password, wallet_path)
            print(f"Wallet created successfully at {wallet_path}")
            return wallet
        else:
            print("\nLoading existing wallet...")
            with open(wallet_path, "r") as f:
                keystore = json.load(f)
            private_key = Account.decrypt(keystore, config.password)
            account = Account.from_key(private_key)
            wallet = Wallet(private_key.hex(), account.address)
            print(f"Wallet loaded successfully from {wallet_path}")
            return wallet
            
    except Exception as e:
        print(f"Error setting up wallet: {str(e)}")
        return None
