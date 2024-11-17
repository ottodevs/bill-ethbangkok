# -*- coding: utf-8 -*-
"""Service deployment module."""

import json
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, cast

from operate.services.manage import ServiceManager
from operate.services.service import Service
from operate.types import (
    ServiceTemplate, 
    ConfigurationTemplate, 
    FundRequirementsTemplate,
    ChainType,
    OnChainState
)

from src.config.constants import (
    SUGGESTED_TOP_UP_DEFAULT,
    COST_OF_BOND,
    COST_OF_BOND_STAKING,
    BILL_HOME
)

from src.service.bill_service import BillYieldService
from src.config.settings import Config
from src.chain.wallet import Wallet
from src.chain.base import ChainConfig

def get_service_template(config: Any) -> ServiceTemplate:
    """Get the service template"""
    return ServiceTemplate({
        "name": "Bill Yield Agent",
        "hash": "bafybeidlfxklqbwrba5xdbigchkl5dcqcrlpzbrkem62jbzr5yghwe7tgu",
        "description": "Bill Yield Agent",
        "image": "https://gateway.autonolas.tech/ipfs/bafybeiaakdeconw7j5z76fgghfdjmsr6tzejotxcwnvmp3nroaw3glgyve",
        "service_version": 'v0.18.1',
        "home_chain_id": "8453",  # Base chain
        "configurations": {
            "8453": ConfigurationTemplate(
                {
                    "staking_program_id": "bill_alpha",
                    "rpc": config.base_rpc,
                    "nft": "bafybeiaakdeconw7j5z76fgghfdjmsr6tzejotxcwnvmp3nroaw3glgyve",
                    "cost_of_bond": COST_OF_BOND,
                    "threshold": 1,
                    "use_staking": False,
                    "fund_requirements": FundRequirementsTemplate(
                        {
                            "agent": SUGGESTED_TOP_UP_DEFAULT * 5,
                            "safe": 0,
                        }
                    ),
                }
            ),
        },
    })

def get_service(manager: ServiceManager, template: ServiceTemplate) -> Service:
    """Get or create service."""
    if len(manager.json) > 0:
        old_hash = manager.json[0]["hash"]
        if old_hash == template["hash"]:
            print(f'Loading service {template["hash"]}')
            service = manager.load_or_create(
                hash=template["hash"],
                service_template=template,
            )
        else:
            print(f"Updating service from {old_hash} to {template['hash']}")
            service = manager.update_service(
                old_hash=old_hash,
                new_hash=template["hash"],
                service_template=template,
            )
    else:
        print(f'Creating service {template["hash"]}')
        service = manager.load_or_create(
            hash=template["hash"],
            service_template=template,
        )

    return service

def add_volumes(docker_compose_path: Path, host_path: str, container_path: str) -> None:
    """Add volumes to the docker-compose."""
    import yaml
    
    with open(docker_compose_path, "r") as f:
        docker_compose = yaml.safe_load(f)

    docker_compose["services"]["bill_abci_0"]["volumes"].append(f"{host_path}:{container_path}:Z")

    with open(docker_compose_path, "w") as f:
        yaml.dump(docker_compose, f)

def deploy_service(config: Config, chain_config: ChainConfig, wallet: Wallet) -> None:
    """Deploy the service."""
    try:
        print("\nDeploying service...")
        
        # Verificar requisitos previos
        if not verify_prerequisites(config, chain_config):
            raise Exception("Failed to verify prerequisites")
            
        # Crear directorios necesarios
        service_path = Path.home() / ".bill" / "service"
        service_path.mkdir(parents=True, exist_ok=True)
        
        # Desplegar contratos
        if not deploy_contracts(config, chain_config, wallet):
            raise Exception("Failed to deploy contracts")
            
        # Inicializar servicio
        if not initialize_service(config, chain_config, wallet):
            raise Exception("Failed to initialize service")
            
        print("Service deployed successfully")
        
    except Exception as e:
        raise Exception(f"Error deploying service: {str(e)}")

def verify_prerequisites(config: Config, chain_config: ChainConfig) -> bool:
    """Verify all prerequisites are met."""
    # Implementar verificaciones
    return True

def deploy_contracts(config: Config, chain_config: ChainConfig, wallet: Wallet) -> bool:
    """Deploy smart contracts."""
    # Implementar despliegue
    return True

def initialize_service(config: Config, chain_config: ChainConfig, wallet: Wallet) -> bool:
    """Initialize the service."""
    # Implementar inicialización
    return True
