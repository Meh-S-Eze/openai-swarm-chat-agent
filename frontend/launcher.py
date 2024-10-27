import subprocess
import sys
import time
from pathlib import Path

def launch_services():
    """Launch both backend and frontend services"""
    
    # Get the project root directory
    root_dir = Path(__file__).parent.parent
    
    try:
        # Start the backend service
        print("Starting backend service...")
        backend = subprocess.Popen(
            [sys.executable, "examples/support_bot/customer_service.py"],
            cwd=root_dir
        )
        
        # Wait a moment for backend to initialize
        time.sleep(2)
        
        # Start the frontend service
        print("Starting frontend service...")
        frontend = subprocess.Popen(
            [sys.executable, "frontend/run.py"],
            cwd=root_dir
        )
        
        # Keep the script running
        backend.wait()
        frontend.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down services...")
        frontend.terminate()
        backend.terminate()
        sys.exit(0)

if __name__ == "__main__":
    launch_services()
