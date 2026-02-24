import { useEffect, useState } from 'react'
import client from '../api/client'

export default function Exams() {
  const [subjects, setSubjects] = useState([])
  const [exams, setExams] = useState([])
  const [form, setForm] = useState({ subject_id: '', title: '', exam_date: '', target_hours: 1, priority: 3 })

  const load = async () => {
    const [subRes, examRes] = await Promise.all([client.get('/subjects'), client.get('/exams')])
    setSubjects(subRes.data)
    setExams(examRes.data)
    if (!form.subject_id && subRes.data.length) setForm((prev) => ({ ...prev, subject_id: subRes.data[0].id }))
  }

  useEffect(() => { load() }, [])

  const create = async (e) => {
    e.preventDefault()
    await client.post('/exams', { ...form, target_hours: Number(form.target_hours), priority: Number(form.priority) })
    setForm({ ...form, title: '', exam_date: '' })
    load()
  }

  const remove = async (id) => {
    await client.delete(`/exams/${id}`)
    load()
  }

  return (
    <div className="container">
      <h1>Exams</h1>
      <form onSubmit={create} className="form">
        <select value={form.subject_id} onChange={(e) => setForm({ ...form, subject_id: e.target.value })} required>
          {subjects.map((s) => <option value={s.id} key={s.id}>{s.name}</option>)}
        </select>
        <input placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        <input type="date" value={form.exam_date} onChange={(e) => setForm({ ...form, exam_date: e.target.value })} required />
        <input type="number" min="1" value={form.target_hours} onChange={(e) => setForm({ ...form, target_hours: e.target.value })} required />
        <input type="number" min="1" max="5" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} required />
        <button>Add Exam</button>
      </form>
      {exams.map((e) => (
        <div className="card row" key={e.id}><span>{e.title} ({e.exam_date}) - {e.target_hours}h p{e.priority}</span><button onClick={() => remove(e.id)}>Delete</button></div>
      ))}
    </div>
  )
}
