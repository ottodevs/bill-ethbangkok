export const PaymentView = () => (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        padding: '40px',
        gap: '32px',
        background: '#1C1C28',
        color: 'white',
      }}
    >
      <div
        style={{
          display: 'flex',
          fontSize: '64px',
          fontWeight: 'bold',
        }}
      >
        Payment request
      </div>
  
      <div
        style={{
          display: 'flex',
          fontSize: '32px',
          color: '#9BA1A6',
        }}
      >
        Send ETH to start earning 8% APR with Bill
      </div>
  
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '32px',
          background: '#25253A',
          borderRadius: '12px',
        }}
      >
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <div style={{ 
            display: 'flex',
            width: '48px', 
            height: '48px', 
            borderRadius: '50%', 
            background: '#3399ff' 
          }} />
          <span style={{ display: 'flex', fontSize: '32px' }}>Ethereum</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ display: 'flex', fontSize: '32px' }}>0.015</span>
          <span style={{ 
            display: 'flex',
            background: '#3D3D56', 
            padding: '8px 16px', 
            borderRadius: '8px',
            fontSize: '32px'
          }}>ETH</span>
        </div>
  
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <div style={{ 
            display: 'flex',
            width: '48px', 
            height: '48px', 
            borderRadius: '50%', 
            background: '#3399ff' 
          }} />
          <span style={{ display: 'flex', fontSize: '32px' }}>bill.eth</span>
        </div>
      </div>
    </div>
  )