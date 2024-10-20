from fastapi import APIRouter
from api import chat

api_router = APIRouter()

# 서버 ROOT API
@api_router.get("/")
async def root():
    return {"message": "welcome to chat"}

api_router.include_router(chat.router)