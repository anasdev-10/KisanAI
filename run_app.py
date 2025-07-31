import subprocess
import sys
import time
import os
from threading import Thread

def run_fastapi():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    # Change to src/backend directory and run FastAPI
    backend_dir = os.path.join(os.path.dirname(__file__), "src", "backend")
    subprocess.run([sys.executable, "-m", "uvicorn", "fast_api:app", "--host", "127.0.0.1", "--port", "8000", "--reload"], cwd=backend_dir)

def run_streamlit():
    """Run the Streamlit frontend"""
    print("🌱 Starting Streamlit frontend...")
    time.sleep(3)  # Wait for FastAPI to start
    # Change to src/frontend directory and run Streamlit
    frontend_dir = os.path.join(os.path.dirname(__file__), "src", "frontend")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"], cwd=frontend_dir)

def main():
    """Main function to run both servers"""
    print("🌱 KissanAI - Starting Application...")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        os.path.join("src", "backend", "fast_api.py"),
        os.path.join("src", "frontend", "streamlit_app.py"),
        os.path.join("src", "utils", "utils.py")
    ]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return
    
    # Start FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Start Streamlit in main thread
    run_streamlit()

if __name__ == "__main__":
    main() 