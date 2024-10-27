# app/utils/__init__.py
"""Utils module: Our magical toolbox! 🧰"""

from .haunted_logger import setup_logging

# Setup logging when the package is imported
setup_logging()

# Export only what we need
__all__ = ['setup_logging']