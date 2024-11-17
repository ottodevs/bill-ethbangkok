from typing import Dict, Any
import json
import time
import os
from pathlib import Path
from halo import Halo
from web3 import Web3

from operate.services.service import Service
from operate.types import LedgerType, ChainType, OnChainState
from operate.ledger.profiles import OLAS, STAKING

from src.config.constants import (
    SUGGESTED_TOP_UP_DEFAULT,
    COST_OF_BOND,
    COST_OF_BOND_STAKING,
    BILL_HOME,
    BASE_CHAIN_CONFIG,
    CONTRACT_ADDRESSES,
    SAFETY_MARGIN,
    CHAIN_ID_TO_METADATA
)

class BillYieldService(Service):
    """Bill Yield Service implementation."""
    
    def __init__(self, **kwargs):
        """Initialize the service."""
        super().__init__()
        self.wallet = kwargs.get("wallet")
        self.chain_config = kwargs.get("chain_config")
        self.password = kwargs.get("password")
        self.config = kwargs
        
        # Chain specific configurations
        self.chain_id = str(BASE_CHAIN_CONFIG["chain_id"])
        self.token = BASE_CHAIN_CONFIG["token"]
        self.initial_funds_requirement = BASE_CHAIN_CONFIG["initialFundsRequirement"]
        self.operational_fund_req = BASE_CHAIN_CONFIG["operationalFundReq"]
        
        # Gas parameters
        self.max_priority_fee = kwargs.get("priority_fee", "")
        self.max_fee = kwargs.get("max_gas_price", "")

    def setup_environment(self):
        """Setup environment variables and configurations."""
        env_vars = {
            "CUSTOM_CHAIN_RPC": self.config.get("rpc_url"),
            "OPEN_AUTONOMY_SUBGRAPH_URL": "https://api.studio.thegraph.com/query/50957/bill-base/v0.0.1",
            "MAX_PRIORITY_FEE_PER_GAS": self.max_priority_fee,
            "MAX_FEE_PER_GAS": self.max_fee,
        }
        
        for key, value in env_vars.items():
            if value is not None:
                os.environ[key] = value

    def check_and_fund_wallet(self):
        """Check and fund wallet if needed."""
        chain_type = self.chain_config.ledger_config.chain
        ledger_api = self.wallet.ledger_api(
            chain_type=chain_type,
            rpc=self.chain_config.ledger_config.rpc,
        )
        
        # Get current balances
        balance = ledger_api.get_balance(self.wallet.crypto.address)
        print(f"[Base] Main wallet balance: {self.wei_to_token(balance)}")
        
        # Calculate required funds
        agent_fund_requirement = self.fetch_agent_fund_requirement()
        operational_fund_req = self.fetch_operator_fund_requirement()
        
        # Check if service exists
        service_exists = self._get_on_chain_state() != OnChainState.NON_EXISTENT
        
        if service_exists:
            agent_balance = ledger_api.get_balance(address=self.keys[0].address)
            if agent_balance < 0.3 * agent_fund_requirement:
                agent_fund_requirement = agent_fund_requirement - agent_balance
            else:
                agent_fund_requirement = 0

            operator_balance = ledger_api.get_balance(self.wallet.crypto.address)
            if operator_balance < 0.3 * operational_fund_req:
                operational_fund_req = operational_fund_req - operator_balance
            else:
                operational_fund_req = 0

        # Calculate total required balance
        safety_margin = 100_000_000_000_000
        required_balance = operational_fund_req + agent_fund_requirement + safety_margin
        
        return required_balance, service_exists

    def deploy_service(self):
        """Deploy the service on chain."""
        required_balance, service_exists = self.check_and_fund_wallet()
        
        if required_balance > 0:
            print(f"[Base] Please ensure wallet has at least {self.wei_to_token(required_balance)} ETH")
            spinner = Halo(text="[Base] Waiting for funds...", spinner="dots")
            spinner.start()
            
            while self.get_balance() < required_balance:
                time.sleep(1)
            
            spinner.succeed(f"[Base] Wallet funded with {self.wei_to_token(self.get_balance())} ETH")

        # Deploy service on chain
        self.deploy_service_onchain_from_safe_single_chain(
            hash=self.hash,
            chain_id=self.chain_id,
            fallback_staking_params=self.get_staking_params()
        )

        # Fund the service
        self.fund_service(
            hash=self.hash,
            chain_id=self.chain_id,
            agent_fund_threshold=self.fetch_agent_fund_requirement()
        )

    def start(self):
        """Start the service."""
        try:
            print("\nInitializing Bill Yield Service...")
            
            # Setup environment
            self.setup_environment()
            
            # Deploy service
            self.deploy_service()
            
            # Build and start containers
            self.deployment.build(use_docker=True, force=True, chain_id=self.chain_id)
            docker_compose_path = Path(BILL_HOME) / "deployment" / "docker-compose.yaml"
            self.add_volumes(docker_compose_path, str(BILL_HOME), "/data")
            self.deployment.start(use_docker=True)
            
            print("\nService initialized successfully")
            
        except Exception as e:
            print(f"Error starting service: {str(e)}")
            raise

    @staticmethod
    def wei_to_token(wei_amount: int, decimals: int = 18) -> str:
        """Convert wei to token amount."""
        return f"{wei_amount / 10**decimals:.6f} ETH"

    def get_staking_params(self) -> Dict[str, Any]:
        """Get staking parameters."""
        return {
            "agent_ids": [40],
            "service_registry": CONTRACT_ADDRESSES["service_registry"],
            "staking_token": CONTRACT_ADDRESSES["staking_token"],
            "service_registry_token_utility": CONTRACT_ADDRESSES["service_registry_token_utility"],
            "min_staking_deposit": 20000000000000000000,
            "activity_checker": CONTRACT_ADDRESSES["activity_checker"]
        }
