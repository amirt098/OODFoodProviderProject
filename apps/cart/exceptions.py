class UIDNotFound(Exception):
    def __init__(self):
        super().__init__("User with this UID does not found")
