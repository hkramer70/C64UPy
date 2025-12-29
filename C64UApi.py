from enum import Enum
from C64UConfig import config
import C64UModel

#
# Enumeration of API endpoints for the C64 Ultimate service.
#
# Each member represents a specific API path and provides methods
# to get the HTTP method and full REST path.
#
class Api(str, Enum):
    VERSION = "/version"
    RUN_PRG = "/runners:run_prg"
    MOUNT_IMG = "/drives/{drive}:mount"

    #
    # Private functions
    # 

    def _with_params(self, **kwargs) -> str:
        fixed = {
            k: (v.value if isinstance(v, Enum) else v)
            for k, v in kwargs.items()
        }
        return self.format(**fixed)

    #
    # Public API
    # 

    def method(self):
        match self:
            case Api.VERSION:
                return ApiMethod.GET
            case _:
                return ApiMethod.POST

    def restPath(self, drive: C64UModel.Drive = C64UModel.Drive.A):
        basename = config.host + config.apiVersion
        match self:
            case Api.MOUNT_IMG:
                return basename + self._with_params(drive=drive)
            case _:
                return basename + self

class ApiMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

#
# Lokale Tests
#

def testMountImg():
    a = Api.MOUNT_IMG
    print("a", a.restPath())
    print("b", a.restPath(C64UModel.Drive.B))
    print("softiec", a.restPath(C64UModel.Drive.SOFTIEC))

# testMountImg()