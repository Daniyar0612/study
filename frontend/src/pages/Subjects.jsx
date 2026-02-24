import { useEffect, useState } from 'react'
import client from '../api/client'

export default function Subjects() {
  const [subjects, setSubjects] = useState([])
  const [name, setName] = useState('')

  const load = async () => {
    const { data } = await client.get('/subjects')
    setSubjects(data)
  }

  useEffect(() => { load() }, [])

  const create = async (e) => {
    e.preventDefault()
    await client.post('/subjects', { name })
    setName('')
    load()
  }

  const remove = async (id) => {
    await client.delete(`/subjects/${id}`)
    load()
  }

  return (
    <div className="container">
      <h1>Subjects</h1>
      <form onSubmit={create} className="row">
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="New subject" required />
        <button>Add</button>
      </form>
      {subjects.map((s) => (
        <div className="card row" key={s.id}><span>{s.name}</span><button onClick={() => remove(s.id)}>Delete</button></div>
      ))}
    </div>
  )
}
