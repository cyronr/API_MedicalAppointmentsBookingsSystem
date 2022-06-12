class ParsingError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class NotFound(Exception):
    def __int__(self, msg: str) -> None:
        self.msg = msg
        super().__int__(msg)


class UserAlreadyExists(Exception):
    def __int__(self, msg: str) -> None:
        self.msg = msg
        super().__int__(msg)