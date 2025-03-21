from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

# Import API routers
from server.api import player
from server.api import save

# Create FastAPI app
app = FastAPI(title="Pokemon Player State Tracker")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(player.router)
app.include_router(save.router)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Players page
@app.get("/players", response_class=HTMLResponse)
async def players_page(request: Request):
    return templates.TemplateResponse("players.html", {"request": request})

# Saves page
@app.get("/saves", response_class=HTMLResponse)
async def saves_page(request: Request):
    return templates.TemplateResponse("saves.html", {"request": request})

# Run the application
if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
