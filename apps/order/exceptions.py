class UIDNotFound(Exception):
    def __init__(self):
        super().__init__("Driver with this UID was not found")
