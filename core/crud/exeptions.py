"""Contains the exeptions defined for the crud module"""

class NonCallableParam(Exception):
    """Raised when a non-callable param is detected"""
    def __init__(self, message="Non callable function passed to crud"):
        self.message = message
        Exception.__init__(self.message)
