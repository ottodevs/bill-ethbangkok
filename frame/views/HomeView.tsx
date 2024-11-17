export const HomeView = () => (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        justifyContent: 'center',
        padding: '40px',
        gap: '24px',
        background: 'white',
      }}
    >
      <div
        style={{
          display: 'flex',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: '#3399ff',
        }}
      />
      
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          color: 'black',
          fontSize: '64px',
          fontWeight: 'bold',
          textAlign: 'center',
          lineHeight: 1.2,
        }}
      >
        Hi! I'm Bill and I help you earn 8% APR
      </div>
  
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          color: '#666',
          fontSize: '32px',
          textAlign: 'center',
        }}
      >
        Your autonomous DeFi agent for stable yields
      </div>
    </div>
  )