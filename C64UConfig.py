from pathlib import Path
import sys

#
# Configuration class for loading settings from an INI-style file.
#
# This class loads configuration values from a specified file path.
# It supports basic type conversion for values (bool, int, float, str).
# Default values are provided as class attributes and can be overridden by the config file.
#
class Config:
    host: str = "http://c64u"
    timeout: int = 10
    apiVersion: str = "/v1"

    def __init__(self, path: Path):
        self._load(path)

    def _load(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Config-Datei nicht gefunden: {path.name}. Setze Default-Werte.")

        with path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                line = line.strip()

                # Kommentare & leere Zeilen überspringen
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Ungültige Zeile {lineno}: {line}")

                key, value = map(str.strip, line.split("=", 1))
                setattr(self, key, self._convert(value))

    def _convert(self, value: str):
        """Einfache Typkonvertierung"""
        if value.lower() in ("true", "false"):
            return value.lower() == "true"

        if value.isdigit():
            return int(value)

        try:
            return float(value)
        except ValueError:
            return value

#
# Singleton instance of the config file
#
# config = Config(Path(__file__).parent / "config.ini")

def app_dir() -> Path:
    # Wenn per PyInstaller gebaut: Pfad zum EXE
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    # Normal im Source-Run: Projektordner (hier: Ordner von C64UConfig.py)
    return Path(__file__).resolve().parent

config = Config(app_dir() / "config.ini")
