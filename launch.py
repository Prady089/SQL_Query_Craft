import subprocess
import sys
import time
import os

def main():
    # Ensure OPENAI_API_KEY is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        print("Set it with: $Env:OPENAI_API_KEY=\"your-key\"")
        sys.exit(1)
    
    print("Starting FastAPI backend on port 8000...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--port", "8000"],
        cwd=os.path.dirname(__file__) or ".",
    )
    
    # Give the API time to start
    time.sleep(3)
    
    print("Starting Gradio UI on port 7860...")
    ui_process = subprocess.Popen(
        [sys.executable, "chatbot_ui.py"],
        cwd=os.path.dirname(__file__) or ".",
    )
    
    print("\n" + "="*60)
    print("Both services started!")
    print("API: http://127.0.0.1:8000")
    print("UI:  http://127.0.0.1:7860")
    print("Press Ctrl+C to stop both services")
    print("="*60 + "\n")
    
    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        api_process.terminate()
        ui_process.terminate()
        api_process.wait()
        ui_process.wait()
        print("Done.")

if __name__ == "__main__":
    main()
