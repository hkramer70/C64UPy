import pytest
from C64UApi import Api, ApiMethod

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