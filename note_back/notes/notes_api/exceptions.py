class NotOwnerException(Exception):
    def __init__(self):
        self.context = {
            "status":401,
        }
        super().__init__("You don't have permission to acces this data")    