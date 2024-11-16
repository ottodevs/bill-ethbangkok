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

def setup_base_chain(config: Any, wallet: Any) -> Optional[Dict[str, Any]]:
    """Setup Base chain configuration."""
    try:
        chain_metadata = CHAIN_ID_TO_METADATA[8453]  # Base chain ID
        chain_type = "base"
        
        print("[Base] Setting up Base chain configuration...")
        
        # Setup web3 and verify RPC
        web3 = Web3(Web3.HTTPProvider(config.base_rpc))
        if not web3.is_connected():
            print("[Base] Failed to connect to Base RPC")
            return None

        # Verify chain ID
        chain_id = web3.eth.chain_id
        if chain_id != 8453:
            print(f"[Base] Wrong network. Expected Base (8453), got chain ID: {chain_id}")
            return None

        # Calculate funding requirements
        try:
            agent_fund_requirement = fetch_agent_fund_requirement(config.base_rpc)
            if agent_fund_requirement is None:
                print("[Base] Using default fund requirement")
                agent_fund_requirement = SUGGESTED_TOP_UP_DEFAULT * 5
        except Exception as e:
            print(f"[Base] Error calculating fund requirement: {str(e)}")
            print("[Base] Using default fund requirement")
            agent_fund_requirement = SUGGESTED_TOP_UP_DEFAULT * 5

        # Check wallet funding
        required_balance = agent_fund_requirement + SAFETY_MARGIN
        address = wallet.crypto.address
        
        print(f"[Base] Please make sure main wallet {address} has at least {wei_to_token(required_balance, 'ETH')}")
        
        spinner = Halo(text="[Base] Waiting for funds...", spinner="dots")
        spinner.start()

        try:
            while not verify_funding(web3, address, required_balance):
                time.sleep(1)
        except Exception as e:
            spinner.fail(f"[Base] Error verifying funding: {str(e)}")
            return None

        spinner.succeed(f"[Base] Main wallet updated balance: {wei_to_token(web3.eth.get_balance(address), 'ETH')}")

        # Create safe if it doesn't exist
        try:
            if not wallet.safes.get(chain_type):
                print("[Base] Creating Safe")
                wallet.create_safe(
                    chain_type=chain_type,
                    rpc=config.base_rpc,
                )
        except Exception as e:
            print(f"[Base] Error creating safe: {str(e)}")
            return None

        return {
            "chain_id": 8453,
            "metadata": chain_metadata,
            "agent_fund_requirement": agent_fund_requirement,
            "safe_address": wallet.safes.get(chain_type)
        }

    except Exception as e:
        print(f"[Base] Error in setup_base_chain: {str(e)}")
        return None
