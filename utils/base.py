class AppException(Exception):
    def __init__(self, detail:str = "An error occoured"):
        self.detail = detail

