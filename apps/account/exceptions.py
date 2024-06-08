class BadRequest(Exception):
    pass


class UsernameNotFound(BadRequest):
    def __init__(self):
        super().__init__("The username provided is invalid")


class PasswordNotFound(BadRequest):
    def __init__(self):
        super().__init__("The username provided is invalid")


class NotFound(Exception):
    pass


class UIDNotFound(Exception):
    def __init__(self):
        super().__init__("User with this UID does not found")
