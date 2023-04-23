from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import requests, json

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", encoding='utf-8') as f:
        html = f.read()
    return html

@app.get("/findNews")
async def findNews(content: str):
    result = requests.get(f'http://models:1919/sreach?content={content}')
    return JSONResponse(content=json.loads(result.text), headers={"Access-Control-Allow-Origin": "*"})