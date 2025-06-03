"""
Setup script for Audio Q&A Assistant
"""
import os
import sys
import subprocess

def setup_environment():
    """Set up the development environment"""
    print("Audio Q&A Assistant Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Install requirements
    print("\n1. Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        print("  Please install manually: pip install -r requirements.txt")
    
    # Create necessary directories
    print("\n2. Creating directory structure...")
    directories = ["audio", "ai", "ui", "logs", "cache"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Directories created")
    
    # Create __init__.py files
    for directory in ["audio", "ai", "ui"]:
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file):
            open(init_file, 'a').close()
    print("✓ Package files created")
    
    # Check for API key
    print("\n3. Checking OpenAI API configuration...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠ Warning: OPENAI_API_KEY not found in environment variables")
        print("  You'll need to set this for the LLM features to work")
        print("  Options:")
        print("  1. Set environment variable: export OPENAI_API_KEY='your-key-here'")
        print("  2. Create a .env file with: OPENAI_API_KEY=your-key-here")
        print("  3. Edit ai/llm_handler.py and set the API key directly")
    else:
        print("✓ OpenAI API key found")
    
    # Test audio
    print("\n4. Testing audio configuration...")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        p.terminate()
        print("✓ Audio system working")
    except Exception as e:
        print("✗ Audio system error:", str(e))
        print("  Make sure you have a microphone connected")
        print("  On Linux: sudo apt-get install portaudio19-dev")
        print("  On Mac: brew install portaudio")
    
    print("\n" + "=" * 50)
    print("Setup complete! Run 'python main.py' to start the application")

if __name__ == "__main__":
    setup_environment()
