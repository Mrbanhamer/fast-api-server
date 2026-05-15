import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup } from '../api'
import styles from './Auth.module.css'

export default function Signup() {
  const [form, setForm] = useState({ name: '', last_name: '', email: '', password: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await signup(form.name, form.last_name, form.email, form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>Skapa konto</h1>

        {error && <p className={styles.error}>{error}</p>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <label className={styles.label}>
            Förnamn
            <input
              type="text"
              name="name"
              className={styles.input}
              value={form.name}
              onChange={handleChange}
              required
              autoFocus
            />
          </label>

          <label className={styles.label}>
            Efternamn
            <input
              type="text"
              name="last_name"
              className={styles.input}
              value={form.last_name}
              onChange={handleChange}
              required
            />
          </label>

          <label className={styles.label}>
            E-post
            <input
              type="email"
              name="email"
              className={styles.input}
              value={form.email}
              onChange={handleChange}
              required
            />
          </label>

          <label className={styles.label}>
            Lösenord
            <input
              type="password"
              name="password"
              className={styles.input}
              value={form.password}
              onChange={handleChange}
              required
              minLength={6}
            />
          </label>

          <button type="submit" className={styles.btn} disabled={loading}>
            {loading ? 'Skapar konto...' : 'Registrera dig'}
          </button>
        </form>

        <p className={styles.switch}>
          Har du redan ett konto? <Link to="/login">Logga in</Link>
        </p>
      </div>
    </div>
  )
}
