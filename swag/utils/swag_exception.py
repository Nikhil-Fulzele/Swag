class BaseSwagException(Exception):
    def __init__(self, message):
        self.message = message


class TableAlreadyExists(BaseSwagException):
    pass


class NoActvieDBConnection(BaseSwagException):
    pass


class PrimaryKeyAlreadyExistsException(BaseSwagException):
    pass


class ArgumentMissingException(BaseSwagException):
    pass
