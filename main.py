from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from routes.users import user
from utils.hash_password import verify_password

app = FastAPI()

@app.get('/index', response_class=HTMLResponse)
async def get_login():
    try:
        with open('front_end/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)
    
@app.post('/index')
async def login(stored_hash, stored_salt, provided_password):
    if verify_password(stored_hash, stored_salt, provided_password):
        pass




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')