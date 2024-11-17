export const BalanceView = () => (
  <div
    style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100%',
      padding: '40px',
      gap: '24px',
      background: '#1C1C28',
      color: 'white',
    }}
  >
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '8px',
        width: '100%',
      }}
    >
      <div style={{ fontSize: '48px', fontWeight: 'bold' }}>
        Current Balance
      </div>
      <div style={{ fontSize: '72px', fontWeight: 'bold', color: '#007AFF' }}>
        $4,242
      </div>
      <div style={{ fontSize: '32px', color: '#9BA1A6' }}>
        Historical rewards: $24
      </div>
    </div>

    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        width: '100%',
        padding: '24px',
        background: 'rgba(255, 255, 255, 0.05)',
        borderRadius: '12px',
      }}
    >
      <div style={{ fontSize: '32px', color: '#9BA1A6' }}>Current Position</div>
      <div style={{ fontSize: '32px' }}>Pair: USDC-GHO</div>
      <div style={{ fontSize: '32px' }}>Protocol: ETH.GLOBILL</div>
      <div style={{ fontSize: '32px', color: '#4CAF50' }}>Current APR: 8.45%</div>
    </div>
  </div>
)
