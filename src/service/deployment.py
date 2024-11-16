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

def deploy_service(config: Any, chain_config: Dict[str, Any], wallet: Any) -> None:
    """Deploy service."""
    from operate.cli import OperateApp
    from src.config.constants import BILL_HOME
    
    operate = OperateApp(home=BILL_HOME)
    manager = operate.service_manager()
    
    template = get_service_template(config)
    service = get_service(manager, template)
    
    # Deploy service onchain
    manager.deploy_service_onchain_from_safe_single_chain(
        hash=service.hash,
        chain_id="8453",  # Base chain
        fallback_staking_params={},  # Add staking params if needed
    )
    
    # Fund service
    manager.fund_service(
        hash=service.hash,
        chain_id="8453",
        safe_fund_treshold=None,
        safe_topup=None,
        agent_fund_threshold=chain_config.get("agent_fund_requirement", 0)
    )
    
    # Build and start service
    service.deployment.build(use_docker=True, force=True, chain_id="8453")
    docker_compose_path = service.path / "deployment" / "docker-compose.yaml"
    add_volumes(docker_compose_path, str(BILL_HOME), "/data")
    service.deployment.start(use_docker=True)
