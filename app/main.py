import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from app.api.endpoints import chat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Starting Hamzaa Chat Application...")

app = FastAPI(title="Hamzaa Chat", debug=True)

# Compute the absolute path to the 'static' directory.
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")

# Mount the static folder using the absolute path.
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include chat endpoint router
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

# Root endpoint serves our main HTML page using HTMLResponse.
@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = os.path.join(static_dir, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
