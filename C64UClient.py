import requests
from typing import Optional
from pathlib import Path

from C64UConfig import config
from C64UApi import Api
from C64UModel import Version, ImageType, MountMode, Drive

#
# Client class for interacting with the C64 Ultimate REST API.
#
# Provides methods to send requests to various API endpoints,
# handling HTTP communication and response parsing.
#
class Client:

    def __init__(self):
        pass
    
    # Private methods

    # Public API

    #
    # About        ----------------------------------------------------
    #

    #
    # GET: Returns the current version of the REST API
    #
    def requestVersion(self) -> Optional[Version]:
        api = Api.VERSION
        try:
            url = api.restPath()
            r = requests.get(url, timeout=config.timeout)
            r.raise_for_status()
            obj = Version(**r.json())
            return obj
        
        except requests.exceptions.Timeout:
            print("C64U antwortet nicht")
        
        except requests.exceptions.RequestException as e:
            print("HTTP Fehler:", e)
        
        return None

    #
    # Runners      ----------------------------------------------------
    #

    #
    # POST: Upload the given PRG file to the C64U and start it 
    #
    #   fname - specifies the path to the prg file binary
    # 
    def runPrg(self, fname: str) -> bool:
        api = Api.RUN_PRG
        try:
            url = api.restPath()
            print(url)
            path = Path(fname)

            with path.open("rb") as f:
                files = {
                    "file": (path.name, f, "application/octet-stream")
                }

                r = requests.post(url, files=files, timeout=config.timeout)
                r.raise_for_status()
            
            data = r.json()
            if data.get("errors"):
                raise RuntimeError(f"Ultimate meldet Fehler: { data['errors'] }")
    
            return True
        
        except requests.exceptions.Timeout:
            print("C64U antwortet nicht")
        
        except requests.exceptions.RequestException as e:
            print("HTTP Fehler:", e)
        
        return False

    #
    # POST: Mount a disk image that is sent along as an attachment onto drive 
    # specified in the path
    #
    #   fname - specifies the path to the prg file
    #   drive - specifies the drive to mount (only A works actually)
    # imgType - specifies the type of the image (D64, D71, D81 etc.)
    #    mode - specifies the mounting mode: readwrite, readonly or unlinked
    # 
    def mountImage(self, 
                   fname: str, 
                   drive: Drive = Drive.A, 
                   imgType: ImageType = ImageType.D64, 
                   mode: MountMode = MountMode.RW) -> bool:
        api = Api.MOUNT_IMG
        try:
            url = api.restPath(drive)
            path = Path(fname)
            queryParams = {
                "type": imgType.value, 
                "mode": mode.value
            } 

            with path.open("rb") as f:
                files = {
                    "file": (path.name, f, "application/octet-stream")
                }

                r = requests.post(url, params=queryParams, files=files, timeout=config.timeout)
                r.raise_for_status()
            
            data = r.json()
            if data.get("errors"):
                raise RuntimeError(f"Ultimate meldet Fehler: { data['errors'] }")
    
            return True
        
        except requests.exceptions.Timeout:
            print("C64U antwortet nicht")
        
        except requests.exceptions.RequestException as e:
            print("HTTP Fehler:", e)
        
        return False
    

#
# Tests
#

def testInit():
    print("TEST: testInit")
    c1 = Client()
    print("TEST DONE: testInit")

def testVersion():
    print("TEST: testVersion")
    client = Client()
    result = client.requestVersion()

    if result == None: 
        print("Result Failure")
    else:
        print("Result: ", result.version)

    print("TEST DONE: testVersion")

def testImgMount():
    print("TEST: testImgMount")
    client = Client()
    #result = client.mountImage("atlantis.D64", Drive.B, ImageType.D64, MountMode.RW)
    result = client.mountImage("atlantis.D64")

    print(f"Result: {result}")
    print("TEST DONE: testImgMount")


# testInit()
# testVersion()
# testImgMount()