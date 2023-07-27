class NotOwnerException(Exception):
    def __init__(self):
        self.context = {
            "status":401,
        }
        super().__init__("You don't have permission to acces this data")    

class InvalidIdException(Exception):
    def __init__(self):
        self.context = {
            "status":401,
        }
        super().__init__("The given id is not valid")            