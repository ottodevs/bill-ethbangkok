# -*- coding: utf-8 -*-
"""Base chain configuration and setup."""

import sys
import time
from typing import Optional, Dict, Any, cast
from web3 import Web3
from web3.types import Wei
from halo import Halo
from eth_utils import to_wei

from src.utils.formatting import wei_to_token, print_section
from src.config.constants import (
    CHAIN_ID_TO_METADATA,
    SUGGESTED_TOP_UP_DEFAULT,
    SAFETY_MARGIN
)
from src.utils.web3_utils import check_rpc
from src.config.settings import Config
from src.chain.wallet import Wallet

class ChainConfig:
    def __init__(self, rpc_url: str, chain_id: int):
        self.rpc_url = rpc_url
        self.chain_id = chain_id
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

def calculate_fund_requirement(rpc: str, fee_history_blocks: int, gas_amount: int, 
                             fee_history_percentile: int = 50) -> Optional[int]:
    """Calculate funding requirements for a chain."""
    if rpc is None:
        return None
    
    web3 = Web3(Web3.HTTPProvider(rpc))
    block_number = web3.eth.block_number
    fee_history = web3.eth.fee_history(
        fee_history_blocks, block_number, [fee_history_percentile]
    )

    if fee_history is None:
        return None
    
    base_fees = fee_history.get('baseFeePerGas')
    if base_fees is None:
        return None

    priority_fees = [reward[0] for reward in fee_history.get('reward', []) if reward]
    if not priority_fees:
        return None
    
    average_base_fee = sum(base_fees) / len(base_fees)
    average_priority_fee = sum(priority_fees) / len(priority_fees)
    average_gas_price = average_base_fee + average_priority_fee

    fund_requirement = int((average_gas_price * gas_amount) + SAFETY_MARGIN)
    return fund_requirement

def fetch_agent_fund_requirement(rpc: str, fee_history_blocks: int = 20) -> int:
    """Calculate agent funding requirements."""
    gas_amount = 5_000_000  # Base chain gas amount
    return calculate_fund_requirement(rpc, fee_history_blocks, gas_amount)

def verify_funding(web3: Web3, address: str, required_amount: int) -> bool:
    """Verify if address has required funding."""
    balance = web3.eth.get_balance(address)
    return balance >= required_amount

def setup_base_chain(config: Config, wallet: Wallet) -> Optional[ChainConfig]:
    """Setup Base chain configuration."""
    try:
        # Verificar RPC
        if not config.base_rpc:
            raise Exception("Base RPC URL not configured")
            
        chain_config = ChainConfig(
            rpc_url=config.base_rpc,
            chain_id=8453  # Base chain ID
        )
        
        # Verificar conexión
        if not chain_config.web3.is_connected():
            raise Exception("Cannot connect to Base RPC")
            
        # Verificar balance
        balance = chain_config.web3.eth.get_balance(wallet.account.address)
        if balance == 0:
            print(f"Warning: Wallet {wallet.account.address} has no balance on Base")
            
        return chain_config
        
    except Exception as e:
        print(f"Error setting up Base chain: {str(e)}")
        return None
