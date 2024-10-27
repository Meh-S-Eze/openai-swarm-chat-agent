import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def pytest_configure(config):
    """Configure pytest settings"""
    # Set asyncio mode
    config.addinivalue_line(
        "asyncio_mode",
        "strict"
    )
    
    # Set default fixture loop scope
    config.addinivalue_line(
        "asyncio_default_fixture_loop_scope",
        "function"
    )

    # Configure test markers
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async"
    )
