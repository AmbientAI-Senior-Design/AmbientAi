import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import EngagementProvider from './context/engagement-state.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <EngagementProvider>
      <App />
    </EngagementProvider>
  </React.StrictMode>,
)
