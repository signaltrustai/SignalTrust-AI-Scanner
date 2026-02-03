#!/usr/bin/env python3
"""
SignalTrust AI Market Scanner - Python Startup Script
Launches the web application
"""

import os
import sys
import subprocess


def main():
    """Main startup function."""
    print("=" * 70)
    print("SignalTrust AI Market Scanner - Starting...")
    print("=" * 70)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"Using Python {sys.version.split()[0]}")
    print()
    
    # Check if requirements.txt exists and install dependencies
    if os.path.exists("requirements.txt"):
        print("Checking dependencies...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Dependencies installed.")
            else:
                print("Warning: Could not install some dependencies.")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"Warning: Could not check dependencies: {e}")
        print()
    
    print("Starting SignalTrust AI Market Scanner Web Application...")
    print("Access the application at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print()
    
    # Run the web application
    try:
        # Add current directory to path if needed
        if os.path.dirname(__file__) not in sys.path:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import and run the app
        import app
        app.main()
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        return 0
    except Exception as e:
        print(f"Error: Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
