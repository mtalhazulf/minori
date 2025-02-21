from importlib import metadata

try:
    __version__ = metadata.version("minori-api")
except ImportError:
    __version__ = "0.dev"
