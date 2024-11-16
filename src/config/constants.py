"""System constants."""
from pathlib import Path
from termcolor import colored

# Basic Configuration
BILL_HOME = Path.cwd() / ".bill"
WARNING_ICON = colored('\u26A0', 'yellow')

# Fund Configuration (in wei)
SUGGESTED_TOP_UP_DEFAULT = 1_000_000_000_000_000  # 0.001 ETH
MASTER_WALLET_MINIMUM_BALANCE = 6_001_000_000_000_000  # ~0.006 ETH
SAFETY_MARGIN = 100_000_000_000_000  # 0.0001 ETH

# Chain Configuration
CHAIN_ID_TO_METADATA = {
    8453: {  # Base only for MVP
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

# Service Configuration
DEFAULT_MIN_SWAP_AMOUNT_THRESHOLD = 15
DEFAULT_CHAINS = ["base"]
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
