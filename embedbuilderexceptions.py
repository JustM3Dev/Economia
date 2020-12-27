class ValueError(Exception):
    def __init__(self, msg='The given string can\'t be null!'):
        super().__init__(msg)