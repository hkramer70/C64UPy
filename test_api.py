import pytest
from C64UApi import Api, ApiMethod
import C64UModel

def test_api_version_value():
    """Test that Api.VERSION has the correct value."""
    assert Api.VERSION == "/version"

def test_api_run_prg_value():
    """Test that Api.RUN_PRG has the correct value."""
    assert Api.RUN_PRG == "/runners:run_prg"

def test_api_version_method():
    """Test the method property for VERSION."""
    assert Api.VERSION.method() == ApiMethod.GET

def test_api_run_prg_method():
    """Test the method property for RUN_PRG."""
    assert Api.RUN_PRG.method() == ApiMethod.POST

def test_api_rest_path():
    """Test the restPath method."""
    path = Api.VERSION.restPath()
    assert "http://c64u/v1/version" == path  # Based on default config

def test_api_rest_path_mount_img():
    """Test the restPath method."""
    path = Api.MOUNT_IMG
    pathDefault = path.restPath()
    pathA = path.restPath(C64UModel.Drive.A)
    pathB = Api.MOUNT_IMG.restPath(C64UModel.Drive.B)
    pathSoft = Api.MOUNT_IMG.restPath(C64UModel.Drive.SOFTIEC)
    assert "http://c64u/v1/drives/a:mount" == pathDefault  # Based on default config
    assert "http://c64u/v1/drives/a:mount" == pathA  # Based on default config
    assert "http://c64u/v1/drives/b:mount" == pathB  # Based on default config
    assert "http://c64u/v1/drives/softiec:mount" == pathSoft

