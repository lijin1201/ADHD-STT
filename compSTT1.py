from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# Serve static files (e.g., audio)
app.mount("/static", StaticFiles(directory="static"), name="static")
audio_dir = "static/audios"
files = sorted([f for f in os.listdir(audio_dir) if f.endswith((".wav", ".mp3", ".webm",".m4a"))])
file_list_html = "".join(
    f"<tr data-file='{f}'>"
    f"<td>{f}<br><button class='playBtn'>▶️ Play & Send</button> <button class='recordBtn'>🎤 Record & Send</button></td>"
    f"<td class='server1-result'>[Server 1 Result]</td>"
    f"<td class='server2-result'>[Server 2 Result]</td></tr>"
    for f in files
)

# @app.get("/", response_class=HTMLResponse)
# async def index():
#     audio_dir = "static/audios"
#     files = [f for f in os.listdir(audio_dir) if f.endswith((".wav", ".mp3", ".webm"))]
#     file_list_html = "".join(
#         f"<tr data-file='{f}'>"
#         f"<td>{f}<br><button class='playBtn'>▶️ Play & Send</button> <button class='recordBtn'>🎤 Record & Send</button></td>"
#         f"<td class='server1-result'>[Server 1 Result]</td>"
#         f"<td class='server2-result'>[Server 2 Result]</td></tr>"
#         for f in files
#     )
#     return f"""
    
#     """

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("comp-index.html", {"request": request, "file_list_html": file_list_html})