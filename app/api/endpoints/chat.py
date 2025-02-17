from fastapi import APIRouter, HTTPException
from app.models.chat_model import ChatRequest, ChatResponse
from app.services.rag_service import generate_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = await generate_response(request.query)
        return ChatResponse(answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
