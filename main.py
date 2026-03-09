from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post('/index')
async def bye():
    return 'goodbye'

@app.get('/index', response_class=HTMLResponse)
async def hi():
    try:
        with open('front_end/index.h', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')