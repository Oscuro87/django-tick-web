class TicketCreationException(Exception):
    def __init__(self, message):
        self.message = message
        super(TicketCreationException, self).__init__(message)

    def getMessage(self):
        return self.message