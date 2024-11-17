import { Button, Frog } from 'frog'
import { devtools } from 'frog/dev'
import { handle } from 'frog/next'
import { serveStatic } from 'frog/serve-static'
import { HomeView } from '../views/HomeView.js'
import { PaymentView } from '../views/PaymentView.js'
import { SuccessView } from '../views/SuccessView.js'
import { BalanceView } from '../views/BalanceView.js'
import { WithdrawalView } from '../views/WithdrawalView.js'

export const app = new Frog({
  assetsPath: '/',
  basePath: '/api',
  title: 'Bill',
})

app.frame('/', (c) => {
  const { buttonValue } = c
  
  if (buttonValue === 'dashboard') {
    return c.res({
      image: <BalanceView />,
      intents: [
        <Button value="earn">Deposit More</Button>,
        <Button value="withdraw">Withdraw</Button>,
        <Button value="back">Back</Button>
      ],
    })
  }
  
  if (buttonValue === 'withdraw') {
    return c.res({
      image: <WithdrawalView />,
      intents: [
        <Button value="confirm">Confirm Withdrawal</Button>,
        <Button value="back">Back</Button>
      ],
    })
  }
  
  if (buttonValue === 'check') {
    return c.res({
      image: <SuccessView />,
      intents: [
        <Button value="dashboard">Open Dashboard</Button>,
        <Button.Link href="https://blockscout.base.org/address/0x0000000000000000000000000000000000000000">View Activity</Button.Link>,
        <Button value="back">Back</Button>
      ],
    })
  }
  
  if (buttonValue === 'earn') {
    return c.res({
      image: <PaymentView />,
      intents: [
        <Button value="check">Check Balance & Start</Button>,
        <Button value="back">Back</Button>
      ],
    })
  }

  return c.res({
    image: <HomeView />,
    intents: [
      <Button value="earn">Start Earning 8% APR</Button>,
      <Button.Link href="https://docs.bill.finance/learn">Learn More</Button.Link>,
    ],
  })
})

// @ts-ignore
const isEdgeFunction = typeof EdgeFunction !== 'undefined'
const isProduction = isEdgeFunction || import.meta.env?.MODE !== 'development'
devtools(app, isProduction ? { assetsPath: '/.frog' } : { serveStatic })

export const GET = handle(app)
export const POST = handle(app)
