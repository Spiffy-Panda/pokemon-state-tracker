from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn

# Create FastAPI app
app = FastAPI(title="Pokemon Player State Tracker")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return {"message": "Pokemon Player State Tracker API is running"}

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
