from fastapi import FastAPI

app = FastAPI()

@app.post('/index')
async def bye():
    return 'goodbye'

@app.get('/index')
async def hi():
    return 'hello'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8000, log_level='info')