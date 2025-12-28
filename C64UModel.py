from dataclasses import dataclass
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
