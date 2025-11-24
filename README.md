# 🎭 Camera Reactions for Windows

> Bring Apple's Camera Reactions feature to Windows! Add gesture-controlled animated effects to your video calls with just your hands.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

![Demo](assets/demo.gif)

## ✨ Features

- **Real-time Hand Gesture Recognition** - Detects 6+ hand gestures using Google MediaPipe
- **Animated Visual Effects** - Beautiful 3D-style animations that overlay your video feed
- **Virtual Camera Integration** - Works seamlessly with Zoom, Teams, Meet, Discord, and more
- **Low Latency Performance** - Optimized for 30+ FPS even on modest hardware
- **Customizable Settings** - Enable/disable individual gestures, adjust sensitivity, preview effects
- **Privacy Focused** - All processing happens locally on your device

## 🎯 Supported Gestures

| Gesture | Effect | Description |
|---------|--------|-------------|
| 👍 Thumbs Up | Thumbs up animation | Single thumbs up gesture |
| 👎 Thumbs Down | Thumbs down animation | Single thumbs down gesture |
| 👍👍 Two Thumbs Up | Confetti & Fireworks | Both hands showing thumbs up |
| ✌️ Peace Sign | Floating Balloons | Two fingers up (V sign) |
| 💗 Heart Hands | Hearts animation | Hands forming heart shape |
| ✊ Raised Fist | Laser Beams | Closed fist raised up |

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Intel i5 or equivalent (supports AVX)
- **Webcam**: Any USB or built-in webcam (720p minimum)
- **GPU**: Optional - CUDA-capable GPU for better performance

### Software Dependencies
- Python 3.8 or higher
- DirectShow-compatible virtual camera driver

## 🚀 Quick Start

### Installation

#### Option 1: Installer (Recommended)
1. Download the latest installer from [Releases](https://github.com/yourusername/reactions-app/releases)
2. Run `CameraReactions-Setup.exe`
3. Follow the installation wizard
4. Launch from Start Menu

#### Option 2: From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/reactions-app.git
cd reactions-app

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install virtual camera driver
python scripts/install_virtual_camera.py

# Run the application
python src/main.py
```

### First Run Setup

1. **Start the Application**
   - Launch "Camera Reactions" from Start Menu or run `python src/main.py`

2. **Select Your Webcam**
   - Choose your physical webcam from the dropdown

3. **Configure Video Apps**
   - In Zoom/Teams/Meet, select "Camera Reactions Virtual Camera" as your camera source

4. **Test Gestures**
   - Use the preview window to test each gesture
   - Adjust sensitivity if needed (Settings → Gesture Sensitivity)

5. **Start Your Call**
   - Perform gestures in front of your camera to trigger effects!

## 📖 Usage Guide

### Basic Usage

1. **Launch the app** before starting your video call
2. **Select the virtual camera** in your video conferencing app:
   - **Zoom**: Settings → Video → Camera → "Camera Reactions Virtual Camera"
   - **Teams**: Settings → Devices → Camera → "Camera Reactions Virtual Camera"
   - **Google Meet**: Settings → Video → Camera → "Camera Reactions Virtual Camera"
   - **Discord**: User Settings → Voice & Video → Camera → "Camera Reactions Virtual Camera"

3. **Perform gestures** in front of your webcam to trigger effects

### Configuration

Access settings via the system tray icon or main window:

- **Gesture Sensitivity**: Adjust detection threshold (50-95% confidence)
- **Effect Duration**: How long animations play (1-5 seconds)
- **Enable/Disable Gestures**: Toggle individual gestures on/off
- **Camera Settings**: Resolution, FPS, brightness/contrast
- **Hotkeys**: Optional keyboard shortcuts to trigger effects manually

### Tips for Best Results

- **Lighting**: Ensure good, even lighting on your hands
- **Distance**: Keep hands 1-2 feet from camera
- **Background**: Solid backgrounds work best for hand detection
- **Hold Gesture**: Hold each gesture for 1-2 seconds for reliable detection
- **Single Person**: Works best with one person in frame

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│              (Settings, Preview, Tray Icon)             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                Main Application                         │
│         (Orchestration & State Management)              │
└─┬──────────────┬──────────────┬────────────────────────┘
  │              │              │
  ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌──────────────┐
│ Webcam  │  │ Gesture │  │  Animation   │
│ Capture │─▶│Detector │─▶│   Engine     │
│(OpenCV) │  │(MediaP.)│  │ (OpenGL/CV)  │
└─────────┘  └─────────┘  └──────┬───────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │Virtual Camera  │
                         │   Output       │
                         │  (DirectShow)  │
                         └────────────────┘
```

### Key Components

- **Gesture Detector** (`src/gesture_detector.py`) - MediaPipe-based hand tracking and gesture classification
- **Animation Engine** (`src/animation_engine.py`) - Renders effects with OpenGL/OpenCV
- **Virtual Camera** (`src/virtual_camera.py`) - DirectShow virtual camera driver interface
- **UI Manager** (`src/ui/main_window.py`) - PyQt5-based user interface
- **Config Manager** (`src/config.py`) - Settings persistence and management

## 🧪 Development

### Project Structure

```
reactions-app/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gesture_detector.py     # Hand gesture recognition
│   ├── animation_engine.py     # Effect rendering
│   ├── virtual_camera.py       # Virtual camera integration
│   ├── config.py               # Configuration management
│   ├── ui/
│   │   ├── main_window.py      # Main UI window
│   │   ├── settings_dialog.py  # Settings interface
│   │   └── preview_widget.py   # Camera preview
│   └── effects/
│       ├── hearts.py           # Heart animation
│       ├── confetti.py         # Confetti effect
│       ├── balloons.py         # Balloon effect
│       ├── thumbs.py           # Thumbs up/down
│       └── lasers.py           # Laser beam effect
├── assets/
│   ├── icons/                  # Application icons
│   ├── animations/             # Animation sprites/models
│   └── sounds/                 # Optional sound effects
├── tests/
│   ├── test_gesture_detector.py
│   ├── test_animation_engine.py
│   └── test_virtual_camera.py
├── docs/
│   ├── API.md                  # API documentation
│   ├── ARCHITECTURE.md         # Architecture details
│   └── GESTURES.md             # Gesture detection guide
├── scripts/
│   ├── install_virtual_camera.py
│   ├── build_installer.py
│   └── benchmark.py
├── .github/
│   ├── workflows/
│   │   ├── build.yml
│   │   └── test.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── requirements.txt
├── setup.py
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_gesture_detector.py
```

### Building from Source

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 src/
black src/

# Type checking
mypy src/

# Build installer
python scripts/build_installer.py
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google MediaPipe](https://google.github.io/mediapipe/) - Hand tracking and gesture recognition
- [OpenCV](https://opencv.org/) - Computer vision library
- [pyvirtualcam](https://github.com/letmaik/pyvirtualcam) - Virtual camera driver
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - User interface framework
- Inspired by [Apple's Camera Reactions](https://support.apple.com/en-au/105117#reactions)

## 🐛 Known Issues

- Virtual camera may not appear immediately in some apps (restart app to refresh)
- High CPU usage on systems without GPU acceleration (enable GPU in settings)
- Occasional false positives with complex hand backgrounds (improve lighting)

See [Issues](https://github.com/yourusername/reactions-app/issues) for full list and workarounds.

## 🗺️ Roadmap

- [ ] Additional gesture support (rock/paper/scissors, finger counting)
- [ ] Custom animation upload
- [ ] Multi-language support
- [ ] macOS and Linux ports
- [ ] Mobile app integration
- [ ] AI-based gesture customization
- [ ] Performance profiling dashboard

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/reactions-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/reactions-app/discussions)
- **Email**: support@reactions-app.com

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/reactions-app&type=Date)](https://star-history.com/#yourusername/reactions-app&Date)

---

Made with ❤️ by the Camera Reactions Team
