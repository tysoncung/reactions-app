# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release features
- Hand gesture recognition using MediaPipe
- Six gesture types support
- Virtual camera integration
- Real-time animation effects
- Settings UI with gesture customization
- System tray integration

## [1.0.0] - 2025-01-15

### Added
- 🎭 Core gesture detection system
  - Thumbs up/down recognition
  - Peace sign detection
  - Heart hands detection
  - Two thumbs up detection
  - Raised fist detection
- 🎨 Animation effects
  - Hearts animation
  - Confetti/fireworks effect
  - Balloon animation
  - Thumbs up/down graphics
  - Laser beam effects
- 📹 Virtual camera integration
  - DirectShow virtual camera driver
  - Multi-app support (Zoom, Teams, Meet, Discord)
  - HD video quality (720p/1080p)
- 🖥️ User interface
  - Main control window
  - Settings dialog
  - Live camera preview
  - System tray icon
  - Gesture enable/disable toggles
- ⚙️ Configuration system
  - JSON-based settings persistence
  - Gesture sensitivity adjustment
  - Effect duration customization
  - Camera selection
- 📊 Performance optimizations
  - Multi-threading for gesture detection
  - GPU acceleration support
  - Frame rate optimization (30+ FPS)
- 📝 Documentation
  - Comprehensive README
  - API documentation
  - Architecture guide
  - Gesture detection guide

### Technical
- MediaPipe Hands v0.10.8 integration
- OpenCV 4.8.1 for video processing
- PyQt5 for UI framework
- pyvirtualcam for virtual camera
- Python 3.8+ support

### Security
- All video processing done locally (no cloud)
- No telemetry or data collection
- Secure configuration file storage

## [0.9.0] - 2025-01-01 (Beta)

### Added
- Beta release for early testing
- Basic gesture detection (3 gestures)
- Simple animation effects
- Virtual camera proof-of-concept
- Command-line interface

### Known Issues
- Occasional gesture false positives
- High CPU usage on older systems
- Limited to 720p resolution

## [0.5.0] - 2024-12-15 (Alpha)

### Added
- Initial alpha release
- MediaPipe integration
- Basic thumbs up detection
- Simple overlay graphics
- Camera capture functionality

### Known Issues
- No virtual camera support yet
- Limited to single gesture
- Development-only UI

[Unreleased]: https://github.com/yourusername/reactions-app/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/reactions-app/releases/tag/v1.0.0
[0.9.0]: https://github.com/yourusername/reactions-app/releases/tag/v0.9.0
[0.5.0]: https://github.com/yourusername/reactions-app/releases/tag/v0.5.0
