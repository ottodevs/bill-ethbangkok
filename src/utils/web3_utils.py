# -*- coding: utf-8 -*-
"""Web3 utilities."""

import sys
import json
from typing import Optional, Dict, Any
import requests
from web3 import Web3
from web3.types import Wei
from halo import Halo
from eth_utils import to_wei

def debug_rpc_response(response: requests.Response) -> None:
    """Debug RPC response."""
    print("\n=== RPC Response Debug ===")
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("\nContent Type:", response.headers.get('content-type', 'Not specified'))
    
    # Try to parse as JSON first
    try:
        json_response = response.json()
        print("\nJSON Response:")
        print(json.dumps(json_response, indent=2))
    except json.JSONDecodeError:
        # If not JSON, show first 500 chars of text
        print("\nNon-JSON Response (first 500 chars):")
        print(response.text[:500])
    print("=== End Debug ===\n")

def check_rpc(rpc_url: str) -> None:
    """Check RPC endpoint validity."""
    spinner = Halo(text="Checking RPC...", spinner="dots")
    spinner.start()

    # 1. First try a basic eth_blockNumber call
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bill-yield-agent/1.0.0"
    }

    try:
        print(f"\nTesting RPC endpoint: {rpc_url}")
        response = requests.post(rpc_url, json=payload, headers=headers)
        
        # If response is not JSON, something's wrong
        if 'application/json' not in response.headers.get('content-type', ''):
            print("Warning: Response is not JSON")
            debug_rpc_response(response)
            spinner.fail("RPC returned non-JSON response")
            sys.exit(1)

        # Try to parse response
        try:
            result = response.json()
            if 'error' in result:
                print(f"RPC Error: {result['error']}")
                spinner.fail("RPC returned error")
                sys.exit(1)
            if 'result' not in result:
                print("RPC Response missing 'result' field:")
                print(json.dumps(result, indent=2))
                spinner.fail("Invalid RPC response format")
                sys.exit(1)
                
            # If we got here, basic RPC call worked
            block_number = int(result['result'], 16)
            print(f"Current block number: {block_number}")
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {str(e)}")
            debug_rpc_response(response)
            spinner.fail("Invalid JSON response")
            sys.exit(1)

        # 2. Now verify chain ID
        payload['method'] = "eth_chainId"
        response = requests.post(rpc_url, json=payload, headers=headers)
        result = response.json()
        
        if 'result' in result:
            chain_id = int(result['result'], 16)
            if chain_id != 8453:
                spinner.fail(f"Wrong network. Expected Base (8453), got chain ID: {chain_id}")
                sys.exit(1)
            
            spinner.succeed(f"RPC checks passed. Connected to Base network (Chain ID: {chain_id})")
            return
        else:
            spinner.fail("Could not verify chain ID")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        spinner.fail("Failed to connect to RPC")
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