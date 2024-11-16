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

def print_box(text: str, padding: int = 1, border: str = '*') -> None:
    """Print text in a box."""
    lines = text.split('\n')
    width = max(len(line) for line in lines)
    box_width = width + 2 * padding + 2

    print(border * box_width)
    for line in lines:
        print(f"{border}{' ' * padding}{line:<{width}}{' ' * padding}{border}")
    print(border * box_width)

def format_eth_amount(wei_amount: int, decimals: int = 6) -> str:
    """Format ETH amount with proper decimals."""
    eth = wei_amount / 1e18
    return f"{eth:.{decimals}f} ETH"

def format_frame_message(title: str, amount: str, status: str) -> str:
    """Format message for Farcaster Frame."""
    return f"{title}\nAmount: {amount}\nStatus: {status}"