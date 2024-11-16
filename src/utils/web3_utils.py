"""Web3 utilities for the Bill Payment Agent."""

from web3 import Web3

def wei_to_eth(wei_amount: int) -> float:
    """Convert wei to ETH."""
    return float(Web3.from_wei(wei_amount, 'ether'))

def get_balance(rpc_url: str, address: str) -> float:
    """Get ETH balance for an address."""
    try:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        balance_wei = web3.eth.get_balance(address)
        return wei_to_eth(balance_wei)
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0.0