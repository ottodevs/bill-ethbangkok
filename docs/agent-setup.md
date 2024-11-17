# Optimus Agent Setup

## 1. Environment Requirements
```bash
# Check Python version
python --version  # Should be 3.10.x

# Install Poetry if not present
curl -sSL https://install.python-poetry.org | python3 -

# Verify Docker
docker --version
docker-compose --version
```

## 2. Initial Configuration
```bash
cd agents/optimus-quickstart
chmod +x run_service.sh

# You'll need:
# - ETH RPC URL
# - Optimism RPC URL
# - Base RPC URL
# - Tenderly API Key
# - Tenderly Account Slug
# - Tenderly Project Slug

./run_service.sh
```

## 3. Funding Requirements
- 0.08 ETH (Ethereum mainnet)
- 20 USDC (Ethereum mainnet)
- 0.04 ETH (Optimism)
- 0.04 ETH (Base)

## 4. Monitoring
```bash
# View logs
docker logs optimus_abci_0 --follow

# Check status
poetry run python report.py
```