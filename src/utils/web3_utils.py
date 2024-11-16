# -*- coding: utf-8 -*-
"""Web3 utilities."""

import sys
from typing import Optional, Dict, Any
import requests
from web3 import Web3
from web3.types import Wei
from halo import Halo
from eth_utils import to_wei

def check_rpc(rpc_url: str) -> None:
    """Check RPC endpoint validity."""
    spinner = Halo(text="Checking RPC...", spinner="dots")
    spinner.start()

    try:
        # Setup web3
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Check basic connection
        if not web3.is_connected():
            spinner.fail("Could not connect to RPC")
            sys.exit(1)

        # Check chain ID (Base mainnet should be 8453)
        chain_id = web3.eth.chain_id
        if chain_id != 8453:
            spinner.fail(f"Wrong network. Expected Base (8453), got chain ID: {chain_id}")
            sys.exit(1)

        # Check if we can get the latest block
        latest_block = web3.eth.get_block('latest')
        if not latest_block:
            spinner.fail("Could not get latest block")
            sys.exit(1)

        spinner.succeed(f"RPC checks passed. Connected to Base network (Chain ID: {chain_id})")
        return

    except Exception as e:
        spinner.fail(f"Error checking RPC: {str(e)}")
        sys.exit(1)

def get_erc20_balance(web3: Web3, token_address: str, account_address: str) -> int:
    """Get ERC-20 token balance."""
    erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        }
    ]

    contract = web3.eth.contract(
        address=web3.to_checksum_address(token_address), 
        abi=erc20_abi
    )
    
    return contract.functions.balanceOf(
        web3.to_checksum_address(account_address)
    ).call()

def estimate_priority_fee(
    web3: Web3,
    block_number: int,
    default_priority_fee: Optional[int],
    fee_history_blocks: int,
    fee_history_percentile: int,
    priority_fee_increase_boundary: int,
) -> Optional[int]:
    """Estimate priority fee from base fee."""
    if default_priority_fee is not None:
        return default_priority_fee

    fee_history = web3.eth.fee_history(
        fee_history_blocks, block_number, [fee_history_percentile]
    )

    rewards = sorted([reward[0] for reward in fee_history.get("reward", []) if reward[0] > 0])
    if not rewards:
        return None

    percentage_increases = [
        ((j - i) / i) * 100 if i != 0 else 0 
        for i, j in zip(rewards[:-1], rewards[1:])
    ]
    
    if not percentage_increases:
        return rewards[len(rewards) // 2]

    highest_increase = max(percentage_increases)
    highest_increase_index = percentage_increases.index(highest_increase)

    values = rewards.copy()
    if (highest_increase > priority_fee_increase_boundary 
        and highest_increase_index >= len(values) // 2):
        values = values[highest_increase_index:]

    return values[len(values) // 2]