from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post('/index')
async def bye():
    return 'goodbye'

@app.get('/index')
async def hi():
    return HTMLResponse('html-index/index.html')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')