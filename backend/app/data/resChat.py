from pydantic import BaseModel

class ResChatAnswer(BaseModel):
    answer: str
class ResChat(BaseModel):
    code: int
    data: ResChatAnswer

