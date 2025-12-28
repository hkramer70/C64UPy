import requests
from typing import Optional
from pathlib import Path

from C64UConfig import config
from C64UApi import Api
from C64UModel import Version

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
    # POST: Run a given PRG file on the C64U
    #
    #   fname - specifies the path to the prg file
    # 
    def runPrg(self, fname: str) -> bool:
        api = Api.RUN_PRG
        try:
            url = api.restPath()
            print(url)
            prgPath = Path(fname)

            with prgPath.open("rb") as f:
                files = {
                    "file": (prgPath.name, f, "application/octet-stream")
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

# testInit()
# testVersion()