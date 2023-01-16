"""Exception for raising on already running client."""


class AlreadyRunningClient(Exception):

    def __init__(self):
        super().__init__('Client is already running.')
