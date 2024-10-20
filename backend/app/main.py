from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.main import api_router
from exception.exception import ValidException, ServerException

# FastAPI 초기화
app = FastAPI(
    title="OpenAI Server",
    version="1.0.0",
    description="문서 기반 OpenAI Server",
)

# api exception 초기화
@app.exception_handler(ValidException)
async def validationException(request: Request, exc: ValidException):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "msg": f"{exc.req} 값을 입력하세요."
        }
    )
@app.exception_handler(ServerException)
async def serverException(request: Request, exc: ServerException):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": "예기치 못한 서버 에러가 발생했습니다."
        }
    )

app.include_router(api_router)

# .py 파일 실행 (uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)