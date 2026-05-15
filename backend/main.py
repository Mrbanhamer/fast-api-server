from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import user as user_router
from routes.tasks import router as task_router

app = FastAPI()

# Allow the Vite dev server (port 5173) and any other origin in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(user_router, prefix="/user", tags=["users"])

@app.get("/api/status")
async def get_status():
    return {"status": "online", "message": "Backend is reachable"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')