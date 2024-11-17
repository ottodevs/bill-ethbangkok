"""Constants for the Bill Yield Agent."""
from pathlib import Path

# Fund requirements
SUGGESTED_TOP_UP_DEFAULT = 1_000_000_000_000_000
MASTER_WALLET_MINIMUM_BALANCE = 6_001_000_000_000_000
COST_OF_BOND = 1
COST_OF_BOND_STAKING = 2 * 10 ** 19
SAFETY_MARGIN = 100_000_000_000_000

# Paths
BILL_HOME = Path(".bill")

# Chain configurations
CHAIN_ID_TO_METADATA = {
    8453: {
        "name": "Base",
        "token": "ETH",
        "initialFundsRequirement": 0,
        "operationalFundReq": SUGGESTED_TOP_UP_DEFAULT * 5,
        "usdcRequired": False,
        "gasParams": {
            "MAX_PRIORITY_FEE_PER_GAS": "",
            "MAX_FEE_PER_GAS": "",
        }
    }
}

# Contract addresses on Base
CONTRACT_ADDRESSES = {
    "service_registry": "0x9338b5153AE39BB89f50468E608eD9d764B755fD",
    "staking_token": "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f",
    "service_registry_token_utility": "0xa45E64d13A30a51b91ae0eb182e88a40e9b18eD8",
    "activity_checker": "0x155547857680A6D51bebC5603397488988DEb1c8"
}

# Base chain specific config
BASE_CHAIN_CONFIG = CHAIN_ID_TO_METADATA[8453]

# Service parameters
DEFAULT_SERVICE_CONFIG = {
    "name": "Bill Yield Agent",
    "version": "v0.1.0",
    "description": "Automated yield farming agent for Base chain",
    "author": "Bill Team",
}

# Strategy parameters
STRATEGY_PARAMS = {
    "target_apr": 0.08,  # 8% APR objetivo
    "rebalance_threshold": 0.02,  # 2% diferencia para rebalanceo
    "max_position_size": 1000000,  # $1M max position
    "min_position_size": 1000,  # $1k min position
    "min_liquidity": 100000,  # $100k min pool liquidity
    "max_slippage": 0.005,  # 0.5% max slippage
}
