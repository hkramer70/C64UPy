from enum import Enum
from C64UConfig import config

#
# Enumeration of API endpoints for the C64 Ultimate service.
#
# Each member represents a specific API path and provides methods
# to get the HTTP method and full REST path.
#
class Api(str, Enum):
    VERSION = "/version"
    RUN_PRG = "/runners:run_prg"

    def method(self):
        match self:
            case Api.VERSION:
                return ApiMethod.GET
            case Api.RUN_PRG:
                return ApiMethod.POST

    def restPath(self):
        basename = config.host + config.apiVersion
        match self:
            case _:
                return basename + self

class ApiMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
