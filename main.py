from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from user.users_properties import User
from routes.users import user
from utils.hash_password import verify_password

app = FastAPI()



# frontend directions
app.mount("/front_end", StaticFiles(directory="src/front_end"), name="front_end")

@app.get('/index', response_class=HTMLResponse)
async def get_login():
    try:
        # Using the relative path to your html file
        with open('src/front_end/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File not found</h1>", status_code=404)
    
    
@app.post('/index')
async def login(data: User, response: Response):
    # Here you would usually do your logic. 
    # For now, we just acknowledge the "profile" click.
    print(f"User clicked: {data.action}")
    
    # We return a success status. React will see this 'ok' 
    # and perform the redirect on the frontend.
    if data.action == 'profile':
        return RedirectResponse(url="/user/")




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')