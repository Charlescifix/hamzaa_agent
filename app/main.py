import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api.endpoints import chat
from app.logger import setup_logging  # Import our logging setup

# Initialize logging at the start of your application
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Starting Hamzaa Chat Application...")

app = FastAPI(title="Hamzaa Chat", debug=True)


# List your allowed origins
origins = [
    "https://hamzaa.ca",  # Your website domain
    # Optionally add other domains or use "*" to allow all (not recommended for production)
]

# Add the CORS middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
