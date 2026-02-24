import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const logout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav className="nav">
      <div className="nav-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/subjects">Subjects</Link>
        <Link to="/exams">Exams</Link>
        <Link to="/plan">Plan</Link>
      </div>
      <button onClick={logout}>Logout</button>
    </nav>
  )
}
