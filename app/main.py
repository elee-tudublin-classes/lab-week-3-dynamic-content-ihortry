# Import dependencies
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime 
from contextlib import asynccontextmanager
import httpx
from starlette.config import Config
import json

# Load environment variables from .env
config = Config(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

# Create app instance
app = FastAPI(lifespan=lifespan)

# Set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# Handle HTTP GET requests for the site root /
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    serverTime = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "serverTime": serverTime})

@app.get("/apod", response_class=HTMLResponse)
async def index(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get(config("NASA_APOD_URL") + config("NASA_API_KEY"))
    return templates.TemplateResponse("apod.html", {"request": request, "obj": response.json()})
@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):

    requests_client = request.app.requests_client


    response = await requests_client.get(config("ADVICE_URL"))

    return templates.TemplateResponse("advice.html", {"request": request, "data": response.json() })

@app.get("/params", response_class=HTMLResponse)
async def params(request: Request, name: str | None = ""):
    return templates.TemplateResponse("params.html", {"request": request, "name": name})

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)
