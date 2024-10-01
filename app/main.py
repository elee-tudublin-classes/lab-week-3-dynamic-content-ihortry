# import dependencies
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime 

import httpx
from contextlib import asynccontextmanager
import json
from starlette.config import Config

# Load environment variables from .env
config = Config(".env")

# Load API keys and URLs
NASA_APOD_URL = config("NASA_APOD_URL")
NASA_API_KEY = config("NASA_API_KEY")
ADVICE_URL = config("ADVICE_URL", default="https://api.adviceslip.com/advice")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()


# create app instance
app = FastAPI(lifespan=lifespan)


# set location for templates
templates = Jinja2Templates(directory="app/view_templates")
# response = await requests_client.get(config("NASA_APOD_URL") + config("NASA_API_KEY"))
# handle http get requests for the site root /
# return the index.html page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    serverTime: detetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    return templates.TemplateResponse("index.html", {"request": request, "serverTime": serverTime})

@app.get("/apod", response_class=HTMLResponse)
async def apod(request: Request):
    requests_client = request.app.requests_client
    response = await requests_client.get(config("NASA_ADOP_URL") + config("NASA_API_KEY")) 
    return templates.TemplateResponse("apod.html", {"request": request, "img": response.json()})

@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):

    requests_client = request.app.requests_client


    response = await requests_client.get(config("ADVICE_URL"))

    return templates.TemplateResponse("advice.html", {"request": request, "data": response.json() })

@app.get("/params", response_class=HTMLResponse)
async def params(request: Request, name : str | None = ""):
    return templates.TemplateResponse("params.html", {"request": request, "name":name})

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)



