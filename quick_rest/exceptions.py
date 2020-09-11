class TokenError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ServerError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ArgumentError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class FormatError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
