class TargetError(Exception):
    def __init__(self, msg='The given member can\'t be null!'):
        super().__init__(msg)

class MatchingMember(Exception):
    def __init__(self, msg='The given member already exist!'):
        super().__init__(msg)