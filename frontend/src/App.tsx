import { Routes, Route } from 'react-router-dom'
import { Layout } from '@/components/Layout'
import { AuthPage } from '@/pages/AuthPage'
import { EngagementsPage } from '@/pages/EngagementsPage'
import { EngagementDetailPage } from '@/pages/EngagementDetailPage'

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route element={<Layout />}>
        <Route path="/" element={<EngagementsPage />} />
        <Route path="/engagements/:id" element={<EngagementDetailPage />} />
      </Route>
    </Routes>
  )
}

export default App
