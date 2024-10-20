from pydantic import BaseModel

class ReqChat(BaseModel):
    message: str