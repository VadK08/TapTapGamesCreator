
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_CREATOR_BOT_TOKEN")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TokenRequest(BaseModel):
    token: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/auth")
async def check_token(data: TokenRequest):
    url = f"https://api.telegram.org/bot{data.token}/getMe"
    r = requests.get(url)
    return {"ok": r.status_code == 200 and r.json().get("ok")}

@app.get("/constructor", response_class=HTMLResponse)
async def constructor(request: Request):
    return templates.TemplateResponse("constructor.html", {"request": request})
