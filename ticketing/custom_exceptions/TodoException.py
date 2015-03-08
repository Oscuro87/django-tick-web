class TodoException(Exception):
    def __init__(self, message="Pas encore implémenté!"):
        super(TodoException, self).__init__(message)
