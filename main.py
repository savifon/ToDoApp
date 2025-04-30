from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from routers import auth, todos, admin, users

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
