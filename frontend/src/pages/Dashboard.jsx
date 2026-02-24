import { useEffect, useState } from 'react'
import client from '../api/client'

const weekStart = () => {
  const d = new Date(); const day = d.getDay(); const diff = (day + 6) % 7
  d.setDate(d.getDate() - diff)
  return d.toISOString().slice(0, 10)
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    client.get(`/dashboard/stats?week_start=${weekStart()}`).then((r) => setStats(r.data))
  }, [])

  if (!stats) return <div className="container">Loading...</div>

  return (
    <div className="container">
      <h1>Dashboard</h1>
      <div className="card">Total planned hours: {stats.total_planned_hours}</div>
      <div className="card">Completed hours: {stats.completed_hours}</div>
      <div className="card">Completion %: {stats.completion_percent}</div>
      <div className="card">Nearest exam: {stats.nearest_exam_title || '-'} {stats.nearest_exam_date || ''}</div>
    </div>
  )
}
