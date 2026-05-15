import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMe, getTasks, createTask, updateTask, deleteTask, logout } from '../api'
import styles from './Dashboard.module.css'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [tasks, setTasks] = useState([])
  const [newTitle, setNewTitle] = useState('')
  const [newDesc, setNewDesc] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  // Load user + tasks on mount
  useEffect(() => {
    async function load() {
      try {
        const [userData, taskData] = await Promise.all([getMe(), getTasks()])
        setUser(userData)
        setTasks(Array.isArray(taskData) ? taskData : [])
      } catch {
        navigate('/login')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [navigate])

  const handleAddTask = async (e) => {
    e.preventDefault()
    if (!newTitle.trim()) return
    setError(null)
    try {
      await createTask(newTitle.trim(), newDesc.trim())
      setNewTitle('')
      setNewDesc('')
      const updated = await getTasks()
      setTasks(Array.isArray(updated) ? updated : [])
    } catch (err) {
      setError(err.message)
    }
  }

  const handleToggle = async (task) => {
    try {
      await updateTask(task.id, task.title, task.description ?? '', !task.completed)
      setTasks((prev) =>
        prev.map((t) => (t.id === task.id ? { ...t, completed: !t.completed } : t))
      )
    } catch (err) {
      setError(err.message)
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteTask(id)
      setTasks((prev) => prev.filter((t) => t.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (loading) return <div className={styles.loading}>Laddar...</div>

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.headerTitle}>
            Välkommen, {user?.name} {user?.last_name}
          </h1>
          <p className={styles.headerEmail}>{user?.email}</p>
        </div>
        <button className={styles.logoutBtn} onClick={handleLogout}>
          Logga ut
        </button>
      </header>

      <main className={styles.main}>
        {error && <p className={styles.error}>{error}</p>}

        {/* Add task form */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Lägg till uppgift</h2>
          <form onSubmit={handleAddTask} className={styles.addForm}>
            <input
              type="text"
              placeholder="Titel *"
              className={styles.input}
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Beskrivning (valfri)"
              className={styles.input}
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
            />
            <button type="submit" className={styles.addBtn}>
              + Lägg till
            </button>
          </form>
        </section>

        {/* Task list */}
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>
            Mina uppgifter{' '}
            <span className={styles.taskCount}>({tasks.length})</span>
          </h2>

          {tasks.length === 0 ? (
            <p className={styles.empty}>Inga uppgifter ännu. Lägg till en ovan!</p>
          ) : (
            <ul className={styles.taskList}>
              {tasks.map((task) => (
                <li key={task.id} className={`${styles.taskItem} ${task.completed ? styles.done : ''}`}>
                  <input
                    type="checkbox"
                    className={styles.checkbox}
                    checked={task.completed}
                    onChange={() => handleToggle(task)}
                  />
                  <div className={styles.taskContent}>
                    <span className={styles.taskTitle}>{task.title}</span>
                    {task.description && (
                      <span className={styles.taskDesc}>{task.description}</span>
                    )}
                  </div>
                  <button
                    className={styles.deleteBtn}
                    onClick={() => handleDelete(task.id)}
                    aria-label="Ta bort uppgift"
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  )
}
