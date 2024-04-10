class ItemDoesNotExistException(Exception):
    def __init__(self, error_code: str = None, params: dict = None):
        self.error_code = error_code or "item_does_not_exist"
        self.params = params or {}

    def __str__(self):
        return f"Item does not exist: {self.error_code} {self.params}"


class BadRequestException(Exception):
    def __init__(self, error_code: str = None, params: dict = None):
        self.error_code = error_code or "bad_request"
        self.params = params or {}

    def __str__(self):
        return f"Bad request: {self.error_code} {self.params}"
