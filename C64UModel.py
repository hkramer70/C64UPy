from dataclasses import dataclass
from enum import Enum
# from typing import Optional

# Version
#
# GET /v1/version
#
# Result:
# {
#     "version": "0.1",
#     "errors": []
# }
#
@dataclass
class Version:
    version: str
    errors: list

class ImageType(str, Enum):
    D64="d64"
    G64="g64"
    D71="d71"
    G71="g71"
    D81="d81"

class MountMode(str, Enum):
    RW="readwrite"
    RO="readonly"
    UNLINKED="unlinked"

class Drive(str, Enum):
    A="a"
    B="b"
    SOFTIEC="softiec"
