
class HttpServiceException(Exception):
    error:  str
    detail: str | None
    code:int = 400

    def __init__(self, error="HttpServiceException", code=400, detail:str | None=None) -> None:
        super().__init__()
        self.detail = detail
        self.error = error
        self.code = code
    
    def set_code(self, code):
      self.code = code
      return self

    def set_detail(self, detail):
        self.detail = detail
        return self

    def to_json(self):
        resutl = {"error": self.error}
        if self.detail is not None:
            resutl["detail"] = self.detail
        return resutl