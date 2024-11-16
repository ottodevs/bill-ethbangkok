# Bill - Your 8% APR Yield Agent

ETHGlobal Bangkok project

Bill is an autonomous DeFi agent that aims to consistently deliver 8% APR on stablecoins through optimized yield farming strategies. Accessible through Farcaster Frames for a seamless user experience.

## Features
- 🎯 Consistent 8% APR target
- 🔄 Accepts any ERC-20 token
- 🔒 No vesting period
- 🏦 User-controlled wallets
- 🖼️ Farcaster Frame interface

## Tech Stack
- **Agent**: Autonolas (Optimus Quickstart)
- **DEX**: CowSwap (Programmatic Orders)
- **Interface**: Farcaster Frames
- **Analytics**: Blockscout, DeFiLlama
- **Chain**: Base

## Development

1. Initialize project and submodule
```bash
git clone https://github.com/ottodevs/bill-ethbangkok
cd bill-ethbangkok
git submodule add https://github.com/valory-xyz/optimus-quickstart agents/optimus-quickstart
```

2. Create Frame app
```bash
npx create-next-app frame --typescript --tailwind --app
```

3. Setup environment
```bash
cp agents/optimus-quickstart/.env.example .env
```

4. Configure development environment
```bash
# Using nix (recommended)
cp flake.nix .
mkdir .direnv
echo "use flake" > .envrc
direnv allow

# Or just
nix develop

# Verify Python version
python --version  # Should show 3.10.x
```

## Strategy
1. Accept any ERC-20 token deposit
2. Convert to stablecoin pair via CowSwap
3. Deploy to vetted yield opportunities:
   - Min TVL: $10M
   - Audited contracts
   - Auto-compound capability
   - High transaction volume (>95k)
4. Monitor and rebalance for consistent 8% APR

## Frame Interface
- Deposit funds
- Check current position
- View historical rewards
- Manage withdrawals
- Risk explanations
