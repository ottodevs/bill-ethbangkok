# Frame Integration Specification

## Frame Views

### 1. Welcome View
```html
<meta property="fc:frame" content="vNext" />
<meta property="fc:frame:image" content="${FRAME_HOST}/api/images/welcome" />
<meta property="fc:frame:button:1" content="Start Earning 8% APR" />
<meta property="fc:frame:button:2" content="Learn More" />
```
s
### 2. Deposit View
```html
<meta property="fc:frame" content="vNext" />
<meta property="fc:frame:image" content="${FRAME_HOST}/api/images/deposit" />
<meta property="fc:frame:input:text" content="Enter amount to deposit" />
<meta property="fc:frame:button:1" content="Deposit" action="tx" />
<meta property="fc:frame:button:2" content="Back" />
```

### 3. Position View
```html
<meta property="fc:frame" content="vNext" />
<meta property="fc:frame:image" content="${FRAME_HOST}/api/images/position" />
<meta property="fc:frame:button:1" content="Withdraw" />
<meta property="fc:frame:button:2" content="Add Funds" />
<meta property="fc:frame:button:3" content="View Stats" />
```

## Frame Flow
1. User encounters Bill in a Farcaster cast
2. Clicks "Start Earning" to begin
3. Views current APR and pool stats
4. Enters deposit amount
5. Confirms transaction
6. Views position and earnings

## Implementation Details

### Transaction Handling
```typescript
type WalletAction = {
  chainId: "eip155:8453", // Base
  method: "eth_sendTransaction",
  params: {
    abi: [...], // Contract ABI
    to: "0x...", // Bill contract
    value: "0", // For ERC20 approvals
    data: "0x..." // Encoded transaction data
  }
};
```

## Project Structure

```bash
bill/
├── src/
│   ├── frame/
│   │   ├── views/
│   │   │   ├── welcome.tsx
│   │   │   ├── deposit.tsx
│   │   │   └── position.tsx
│   │   ├── components/
│   │   │   ├── APRDisplay.tsx
│   │   │   ├── PositionCard.tsx
│   │   │   └── TokenInput.tsx
│   │   └── api/
│   │       ├── images/
│   │       │   └── [...route].ts
│   │       └── tx/
│   │           └── [...route].ts
│   ├── agent/
│   │   ├── strategy/
│   │   │   ├── yield.ts
│   │   │   └── rebalance.ts
│   │   └── integration/
│   │       ├── cowswap.ts
│   │       └── base.ts
│   └── config/
│       └── constants.ts
├── frame/
│   └── app/
│       ├── page.tsx
│       └── api/
│           └── frame/
│               └── route.ts
└── docker/
    └── docker-compose.yml
```

                        ```bash
src/
├── config/
│   ├── __init__.py
│   ├── constants.py      # Constantes del sistema
│   └── settings.py       # Clase OptimusConfig y funciones relacionadas
├── chain/
│   ├── __init__.py
│   ├── base.py          # Configuración específica de Base
│   └── wallet.py        # Gestión de wallets y safes
├── service/
│   ├── __init__.py
│   ├── deployment.py    # Lógica de despliegue
│   └── funding.py       # Gestión de fondos
└── utils/
    ├── __init__.py
    ├── formatting.py    # Funciones de formato
    └── web3_utils.py    # Utilidades Web3
```