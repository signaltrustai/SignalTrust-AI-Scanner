#!/usr/bin/env python3
"""
SignalTrust AI Scanner - Python Startup Script
This is an alternative entry point that works on all platforms.
"""

import os
import sys
import subprocess


def main():
    """Main startup function."""
    print("=" * 60)
    print("SignalTrust AI Scanner - Starting...")
    print("=" * 60)
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
            # Only show output if there's an error
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("Dependencies checked.")
            else:
                print("Warning: Could not install some dependencies.")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"Warning: Could not check dependencies: {e}")
        print()
    
    # Run the scanner with any provided arguments
    print("Starting SignalTrust AI Scanner...")
    print()
    
    # Import and run the scanner
    try:
        # Add current directory to path if needed
        if os.path.dirname(__file__) not in sys.path:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the scanner module
        import scanner
        
        # Run the main function
        return scanner.main()
        
    except Exception as e:
        print(f"Error: Failed to start scanner: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    print()
    print("=" * 60)
    print("SignalTrust AI Scanner - Finished")
    print("=" * 60)
    sys.exit(exit_code)
