from pathlib import Path

def ensure_test_structure():
    """Create necessary directories and __init__ files for testing"""
    base_dirs = [
        "frontend",
        "frontend/components",
        "frontend/components/chat",
        "frontend/components/utils",
        "frontend/tests",
        "frontend/tests/integration",
        "frontend/tests/utils",
    ]
    
    for dir_path in base_dirs:
        path = Path(dir_path)
        path.mkdir(parents=True, exist_ok=True)
        init_file = path / "__init__.py"
        init_file.touch(exist_ok=True)

if __name__ == "__main__":
    ensure_test_structure()
