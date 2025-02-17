from fastapi import APIRouter, HTTPException
from app.models.chat_model import ChatRequest, ChatResponse
from app.services.rag_service import generate_response
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Received query: {request.query}")
        response = await generate_response(request.query)
        logger.info(f"Response: {response}")
        return ChatResponse(answer=response)
    except Exception as e:
        logger.error("Error in chat endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
