# -*- coding: utf-8 -*-
"""Wallet setup and management."""

import sys
import getpass
import time
from typing import Optional, Tuple, Any

from halo import Halo
from operate.account.user import UserAccount
from operate.cli import OperateApp
from operate.types import LedgerType, ChainType

from src.config.constants import BILL_HOME
from src.utils.formatting import print_box, print_section, wei_to_token

def ask_confirm_password() -> str:
    """Ask and confirm password."""
    password = getpass.getpass("Please enter a password: ")
    confirm_password = getpass.getpass("Please confirm your password: ")

    if password == confirm_password:
        return password
    else:
        print("Passwords do not match. Terminating.")
        sys.exit(1)

def handle_password_migration(operate: OperateApp, config: Any) -> Optional[str]:
    """Handle password migration."""
    if not config.password_migrated:
        print("Add password...")
        old_password, new_password = "12345", ask_confirm_password()
        operate.user_account.update(old_password, new_password)
        if operate.wallet_manager.exists(LedgerType.ETHEREUM):
            operate.password = old_password
            wallet = operate.wallet_manager.load(LedgerType.ETHEREUM)
            wallet.crypto.dump(str(wallet.key_path), password=new_password)
            wallet.password = new_password
            wallet.store()

        config.password_migrated = True
        config.store()
        return new_password
    return None

def setup_wallet(config: Any) -> Optional[Any]:
    """Setup wallet and account."""
    print_section("Set up local user account")
    operate = OperateApp(home=BILL_HOME)
    operate.setup()

    if operate.user_account is None:
        print("Creating a new local user account...")
        password = ask_confirm_password()
        UserAccount.new(
            password=password,
            path=operate._path / "user.json",
        )
        config.password_migrated = True
        config.store()
    else:
        password = handle_password_migration(operate, config)
        if password is None:
            password = getpass.getpass("Enter local user account password: ")
        if not operate.user_account.is_valid(password=password):
            print("Invalid password!")
            sys.exit(1)

    operate.password = password
    if not operate.wallet_manager.exists(ledger_type=LedgerType.ETHEREUM):
        print("Creating the main wallet...")
        wallet, mnemonic = operate.wallet_manager.create(ledger_type=LedgerType.ETHEREUM)
        wallet.password = password
        print()
        print_box(f"Please save the mnemonic phrase for the main wallet:\n{', '.join(mnemonic)}", 0, '-')
        input("Press enter to continue...")
    else:
        wallet = operate.wallet_manager.load(ledger_type=LedgerType.ETHEREUM)

    return wallet
