"""Setup script for Camera Reactions application."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version from version file
version_file = Path(__file__).parent / "src" / "__version__.py"
version = {}
if version_file.exists():
    exec(version_file.read_text(), version)
else:
    version["__version__"] = "1.0.0"

setup(
    name="camera-reactions",
    version=version["__version__"],
    author="Camera Reactions Team",
    author_email="dev@reactions-app.com",
    description="Add gesture-controlled animated effects to your video calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reactions-app",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/reactions-app/issues",
        "Source": "https://github.com/yourusername/reactions-app",
        "Documentation": "https://github.com/yourusername/reactions-app/docs",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "Topic :: Communications :: Conferencing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mediapipe>=0.10.8",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "pyvirtualcam>=0.11.0",
        "PyQt5>=5.15.0",
        "moderngl>=5.8.0",
        "pygame>=2.5.0",
        "pyyaml>=6.0.0",
        "colorlog>=6.8.0",
        "numba>=0.58.0",
        "pywin32>=306; sys_platform == 'win32'",
        "winshell>=0.6; sys_platform == 'win32'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.7.0",
        ],
        "gpu": [
            "onnxruntime-gpu>=1.16.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "camera-reactions=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "config/*.yaml"],
    },
    zip_safe=False,
    keywords="camera reactions gestures video effects virtual-camera",
)
