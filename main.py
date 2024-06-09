import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from contextlib import asynccontextmanager
import httpx
from app.api.routers.users import user_router, login_router
from app.db.db_conn import get_db_conn
from app.db.models.users import Users
from app.db.model_options import ModelOptions

app = FastAPI()

# Load the templates directory
templates = Jinja2Templates(directory="C:app/templates")

# Mount the static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.db = await get_db_conn()
    app.state.models = {
        'users': Users(ModelOptions(db=app.state.db))
    }
    yield
    # Shutdown
    app.state.db.client.close()

app.router.lifespan_context = lifespan

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def post_register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:9000/api/users", json=user_data)
        if response.status_code == 200:
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse("register.html", {"request": request, "message": "User with this email already exists"})

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, email: str = Form(...), password: str = Form(...)):
    login_data = {"email": email, "password": password}
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:9000/api/login", json=login_data)
        if response.status_code == 200:
            return templates.TemplateResponse("index.html", {"request": request, "message": "Login successful"})
        else:
            return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid email or password"})

# Include the user and login routers
app.include_router(user_router, prefix="/api")
app.include_router(login_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
