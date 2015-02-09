class TodoException(Exception):
    def __init__(self, message):
        super(TodoException, self).__init__(message)
