export const SuccessView = () => (
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
        alignItems: 'center',
        justifyContent: 'center',
        width: '120px',
        height: '120px',
        borderRadius: '50%',
        background: '#2E7D32'
      }}
    >
      <div style={{ fontSize: '64px' }}>✓</div>
    </div>

    <div 
      style={{
        display: 'flex',
        fontSize: '64px',
        fontWeight: 'bold',
        textAlign: 'center'
      }}
    >
      Success
    </div>

    <div
      style={{
        display: 'flex',
        fontSize: '32px',
        color: '#9BA1A6',
        textAlign: 'center',
        maxWidth: '500px'
      }}
    >
      Bill is now active and working to generate your 8% APR.
    </div>
  </div>
)