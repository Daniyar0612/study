import { useEffect, useState } from 'react'
import client from '../api/client'
import PlanItemCard from '../components/PlanItemCard'

const todayStr = () => new Date().toISOString().slice(0, 10)
const weekStart = () => {
  const d = new Date(); const day = d.getDay(); const diff = (day + 6) % 7
  d.setDate(d.getDate() - diff)
  return d.toISOString().slice(0, 10)
}

export default function Plan() {
  const [todayItems, setTodayItems] = useState([])
  const [weekItems, setWeekItems] = useState([])

  const load = async () => {
    const [t, w] = await Promise.all([
      client.get(`/plan?date=${todayStr()}`),
      client.get(`/plan/week?start=${weekStart()}`)
    ])
    setTodayItems(t.data)
    setWeekItems(w.data)
  }

  useEffect(() => { load() }, [])

  const generate = async () => {
    await client.post('/plan/generate')
    load()
  }

  const toggle = async (item) => {
    await client.patch(`/plan/${item.id}`, { status: item.status === 'done' ? 'pending' : 'done' })
    load()
  }

  return (
    <div className="container">
      <h1>Plan</h1>
      <button onClick={generate}>Generate Plan</button>
      <h2>Today</h2>
      {todayItems.map((i) => <PlanItemCard key={i.id} item={i} onToggle={toggle} />)}
      <h2>This Week</h2>
      {weekItems.map((i) => <PlanItemCard key={i.id} item={i} onToggle={toggle} />)}
    </div>
  )
}
