# Fullstack Task Manager
# Leonard de Mare

Ett fullstack task manager-projekt med FastAPI backend och React + Vite frontend.

---

## Tech Stack
- **Backend:** Python, FastAPI, MySQL
- **Frontend:** React 18, Vite, React Router v6
- **Auth:** Cookie-baserade sessions (UUID tickets)

---

## Starta projektet

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Servern startar på `http://127.0.0.1:8000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Öppna `http://localhost:5173` i webbläsaren.

> Vite proxar automatiskt `/user/*` och `/tasks/*` till backend på port 8000.

---

## API Endpoints

### Användare
| Metod | URL | Beskrivning |
|-------|-----|-------------|
| POST | `/user/login` | Logga in |
| POST | `/user/signup` | Skapa konto |
| GET | `/user/me` | Hämta inloggad användare |
| GET | `/user/logout` | Logga ut |

### Uppgifter (kräver inloggning)
| Metod | URL | Beskrivning |
|-------|-----|-------------|
| POST | `/tasks/` | Skapa uppgift |
| GET | `/tasks/` | Hämta alla uppgifter |
| GET | `/tasks/{id}` | Hämta en uppgift |
| PUT | `/tasks/{id}` | Uppdatera uppgift |
| DELETE | `/tasks/{id}` | Ta bort uppgift |