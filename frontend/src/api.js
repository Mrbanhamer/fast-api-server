// All API calls go through this module.
// During development, Vite proxies /user and /tasks to http://127.0.0.1:8000

const BASE = ''  // same-origin via Vite proxy

// --- Auth ---

export async function login(email, password) {
  const formData = new URLSearchParams()
  formData.append('username', email)   // FastAPI OAuth2 uses 'username' field
  formData.append('password', password)

  const res = await fetch(`${BASE}/user/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString(),
    credentials: 'include',
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Inloggning misslyckades')
  }
  return res.json()
}

export async function signup(name, last_name, email, password) {
  const formData = new URLSearchParams()
  formData.append('name', name)
  formData.append('last_name', last_name)
  formData.append('email', email)
  formData.append('password', password)

  const res = await fetch(`${BASE}/user/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString(),
    credentials: 'include',
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Registrering misslyckades')
  }
  return res.json()
}

export async function logout() {
  await fetch(`${BASE}/user/logout`, { credentials: 'include' })
}

export async function getMe() {
  const res = await fetch(`${BASE}/user/me`, { credentials: 'include' })
  if (!res.ok) throw new Error('Inte inloggad')
  return res.json()
}

// --- Tasks ---

export async function getTasks() {
  const res = await fetch(`${BASE}/tasks/`, { credentials: 'include' })
  if (!res.ok) throw new Error('Kunde inte hämta uppgifter')
  return res.json()
}

export async function createTask(title, description = '') {
  const res = await fetch(`${BASE}/tasks/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, completed: false }),
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Kunde inte skapa uppgift')
  return res.json()
}

export async function updateTask(id, title, description, completed) {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, completed }),
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Kunde inte uppdatera uppgift')
  return res.json()
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: 'DELETE',
    credentials: 'include',
  })
  if (!res.ok) throw new Error('Kunde inte ta bort uppgift')
  return res.json()
}
