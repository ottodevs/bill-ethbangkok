#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bill Yield Agent Service Runner."""

import sys
from src.config.settings import load_config
from src.service.deployment import deploy_service
from src.chain.wallet import setup_wallet
from src.utils.formatting import print_title, print_section
from src.chain.base import setup_base_chain

def main() -> None:
    """Run the Bill yield agent service."""
    try:
        print_title("Bill Yield Agent")
        print("This script will assist you in setting up and running the Bill yield service.")
        print()

        # Load configuration
        config = load_config()
        if not config:
            print("Failed to load configuration")
            sys.exit(1)

        # Setup wallet and account
        wallet = setup_wallet(config)
        if not wallet:
            print("Failed to setup wallet")
            sys.exit(1)

        # Setup Base chain
        print("\nSetting up Base chain...")
        try:
            chain_config = setup_base_chain(config, wallet)
            if not chain_config:
                print("Failed to setup Base chain - check the logs above for details")
                sys.exit(1)
        except Exception as e:
            print(f"Error setting up Base chain: {str(e)}")
            sys.exit(1)

        # Deploy service
        deploy_service(config, chain_config, wallet)

        print_section("Service is running")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()