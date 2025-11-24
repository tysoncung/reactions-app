"""Build Windows installer for Camera Reactions.

This script creates an MSI installer using cx_Freeze or similar tool.
"""

import os
import sys
from pathlib import Path

def build_installer():
    """Build the Windows installer."""
    print("Building Camera Reactions installer...")

    # Check if PyInstaller is available
    try:
        import PyInstaller.__main__
    except ImportError:
        print("Error: PyInstaller not found. Install with: pip install pyinstaller")
        sys.exit(1)

    # Build executable
    PyInstaller.__main__.run([
        'src/main.py',
        '--name=CameraReactions',
        '--windowed',
        '--onefile',
        '--hidden-import=mediapipe',
        '--hidden-import=cv2',
    ])

    print("Build complete! Executable: dist/CameraReactions.exe")

if __name__ == "__main__":
    build_installer()
