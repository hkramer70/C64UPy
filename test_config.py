import pytest
from pathlib import Path
from C64UConfig import Config

def test_config_defaults():
    """Test that Config has correct default values."""
    # Since it requires a file, we can't test defaults directly without mocking
    # But defaults are class attributes
    assert Config.host == "http://c64u"
    assert Config.timeout == 10
    assert Config.apiVersion == "/v1"

def test_config_load_valid_file(tmp_path):
    """Test loading a valid config file."""
    config_file = tmp_path / "test_config.ini"
    config_file.write_text("""# Comment
host = http://test
timeout = 20
apiVersion = /v2
""")

    config = Config(config_file)
    assert config.host == "http://test"
    assert config.timeout == 20
    assert config.apiVersion == "/v2"

def test_config_type_conversion(tmp_path):
    """Test type conversion in config loading."""
    config_file = tmp_path / "test_config.ini"
    config_file.write_text("""
timeout = 30
enabled = true
disabled = false
pi = 3.14
name = test
""")

    config = Config(config_file)
    assert config.timeout == 30
    assert config.enabled is True
    assert config.disabled is False
    assert config.pi == 3.14
    assert config.name == "test"

def test_config_missing_file():
    """Test that missing config file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        Config(Path("nonexistent.ini"))

def test_config_invalid_line(tmp_path):
    """Test that invalid line (no =) raises ValueError."""
    config_file = tmp_path / "test_config.ini"
    config_file.write_text("invalid line without equals")

    with pytest.raises(ValueError):
        Config(config_file)

def test_config_comments_and_empty_lines(tmp_path):
    """Test that comments and empty lines are ignored."""
    config_file = tmp_path / "test_config.ini"
    config_file.write_text("""
# This is a comment
host = http://example

# Another comment

timeout = 15
""")

    config = Config(config_file)
    assert config.host == "http://example"
    assert config.timeout == 15