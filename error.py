#############################
# 익셉션 클래스를 정의한 패키지 #
#############################

class InvalidUrlError(Exception):
    pass


class InvalidParameterError(Exception):
    pass


class APIUnavailableError(Exception):
    pass
