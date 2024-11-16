"""Formatting utilities for the Bill Payment Agent."""

from typing import List
from termcolor import colored

def print_title(text: str) -> None:
    """Print a title."""
    print()
    print_box(text, 4, '=')

def print_section(text: str) -> None:
    """Print a section header."""
    print_box(text, 1, '-')

def print_box(text: str, margin: int = 1, character: str = '=') -> None:
    """Print text centered within a box."""
    lines = text.split('\n')
    text_length = max(len(line) for line in lines)
    length = text_length + 2 * margin

    border = character * length
    margin_str = ' ' * margin

    print(border)
    for line in lines:
        print(f"{margin_str}{line}{margin_str}")
    print(border)
    print()

def format_eth_amount(wei_amount: int, decimals: int = 6) -> str:
    """Format ETH amount with proper decimals."""
    eth = wei_amount / 1e18
    return f"{eth:.{decimals}f} ETH"

def format_frame_message(title: str, amount: str, status: str) -> str:
    """Format message for Farcaster Frame."""
    return f"{title}\nAmount: {amount}\nStatus: {status}"

def wei_to_unit(wei: int) -> float:
    """Convert Wei to unit."""
    return wei / 1e18

def wei_to_token(wei: int, token: str = "ETH") -> str:
    """Convert Wei to token string."""
    return f"{wei_to_unit(wei):.6f} {token}"