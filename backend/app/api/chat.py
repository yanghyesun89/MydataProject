from fastapi import APIRouter
from service.chatService import ChatService
from data.reqChat import ReqChat
from data.resChat import ResChat, ResChatAnswer
from exception.exception import ValidException, ServerException

router = APIRouter()

# LLM & RAG 생성 초기화
chatService = ChatService()

# 질문 응답 API
@router.post("/chat")
async def postChat(reqData: ReqChat):
    #요청 값 확인
    if not reqData.message:
        raise ValidException("message")
    
    #질문&대답
    try:
      response = ResChatAnswer(answer = chatService.question(query=reqData.message))
      return ResChat(code=200, data=response)
    except:
        raise ServerException()