from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR)

class STATUS_CODES():
    def __init__(self) -> None:
        self.OK = HTTP_200_OK
        self.CREATED = HTTP_201_CREATED
        self.ACCEPTED = HTTP_202_ACCEPTED
        self.CLIENT_ERROR = HTTP_400_BAD_REQUEST
        self.AUTH_ERROR = HTTP_401_UNAUTHORIZED
        self.FORBIDDEN = HTTP_403_FORBIDDEN
        self.NOT_FOUND = HTTP_404_NOT_FOUND
        self.CONFLICT = HTTP_409_CONFLICT
        self.SERVER_ERROR = HTTP_500_INTERNAL_SERVER_ERROR
        
codes = STATUS_CODES()
    
