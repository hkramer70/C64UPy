import pytest
import requests
import requests_mock
from pathlib import Path
from C64UClient import Client
from C64UModel import Version, Drive, ImageType, MountMode

def test_client_init():
    """Test Client initialization."""
    client = Client()
    assert client is not None

def test_request_version_success():
    """Test successful version request."""
    client = Client()
    with requests_mock.Mocker() as m:
        m.get('http://c64u/v1/version', json={'version': '1.0.0', 'errors': []})
        result = client.requestVersion()
        assert result is not None
        assert result.version == '1.0.0'

def test_request_version_timeout():
    """Test version request timeout."""
    client = Client()
    with requests_mock.Mocker() as m:
        m.get('http://c64u/v1/version', exc=requests.exceptions.Timeout)
        result = client.requestVersion()
        assert result is None

def test_request_version_http_error():
    """Test version request HTTP error."""
    client = Client()
    with requests_mock.Mocker() as m:
        m.get('http://c64u/v1/version', status_code=500)
        result = client.requestVersion()
        assert result is None

def test_run_prg_success(tmp_path):
    """Test successful PRG run."""
    client = Client()
    prg_file = tmp_path / "test.prg"
    prg_file.write_bytes(b"fake prg data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/runners:run_prg', json={'success': True})
        result = client.runPrg(str(prg_file))
        assert result is True

def test_run_prg_with_errors(tmp_path):
    """Test PRG run with server errors."""
    client = Client()
    prg_file = tmp_path / "test.prg"
    prg_file.write_bytes(b"fake prg data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/runners:run_prg', json={'errors': ['some error']})
        with pytest.raises(RuntimeError):
            client.runPrg(str(prg_file))

def test_run_prg_timeout(tmp_path):
    """Test PRG run timeout."""
    client = Client()
    prg_file = tmp_path / "test.prg"
    prg_file.write_bytes(b"fake prg data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/runners:run_prg', exc=requests.exceptions.Timeout)
        result = client.runPrg(str(prg_file))
        assert result is False

def test_run_prg_http_error(tmp_path):
    """Test PRG run HTTP error."""
    client = Client()
    prg_file = tmp_path / "test.prg"
    prg_file.write_bytes(b"fake prg data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/runners:run_prg', status_code=400)
        result = client.runPrg(str(prg_file))
        assert result is False

def test_mount_image_success(tmp_path):
    """Test successful image mounting."""
    client = Client()
    img_file = tmp_path / "test.d64"
    img_file.write_bytes(b"fake image data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/drives/a:mount', json={'success': True})
        result = client.mountImage(str(img_file))
        assert result is True

def test_mount_image_with_params(tmp_path):
    """Test image mounting with custom parameters."""
    client = Client()
    img_file = tmp_path / "test.d64"
    img_file.write_bytes(b"fake image data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/drives/b:mount?type=d64&mode=readonly', json={'success': True})
        result = client.mountImage(str(img_file), Drive.B, ImageType.D64, MountMode.RO)
        assert result is True

def test_mount_image_with_errors(tmp_path):
    """Test image mounting with server errors."""
    client = Client()
    img_file = tmp_path / "test.d64"
    img_file.write_bytes(b"fake image data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/drives/a:mount', json={'errors': ['some error']})
        with pytest.raises(RuntimeError):
            client.mountImage(str(img_file))

def test_mount_image_timeout(tmp_path):
    """Test image mounting timeout."""
    client = Client()
    img_file = tmp_path / "test.d64"
    img_file.write_bytes(b"fake image data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/drives/a:mount', exc=requests.exceptions.Timeout)
        result = client.mountImage(str(img_file))
        assert result is False

def test_mount_image_http_error(tmp_path):
    """Test image mounting HTTP error."""
    client = Client()
    img_file = tmp_path / "test.d64"
    img_file.write_bytes(b"fake image data")

    with requests_mock.Mocker() as m:
        m.post('http://c64u/v1/drives/a:mount', status_code=400)
        result = client.mountImage(str(img_file))
        assert result is False