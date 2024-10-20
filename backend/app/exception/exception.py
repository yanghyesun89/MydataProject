# 예외처리
class ValidException(Exception):
    def __init__(self, req: str):
        self.req = req

class ServerException(Exception):
    def __init__(self):
        pass