# Contributing to Camera Reactions

Thank you for considering contributing to Camera Reactions! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@reactions-app.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the behavior you observed** and what you expected
- **Include system information**: OS version, Python version, webcam model
- **Include log files** from `logs/` directory if available

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the proposed functionality
- **Explain why this enhancement would be useful** to most users
- **List any alternatives** you've considered
- **Include mockups or examples** if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (see below)
3. **Add tests** for any new functionality
4. **Ensure all tests pass** (`pytest tests/`)
5. **Update documentation** as needed
6. **Write a clear commit message** (see commit message guidelines)

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/reactions-app.git
cd reactions-app

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Group imports (standard library, third-party, local)
- **Docstrings**: Google style docstrings for all public functions/classes
- **Type hints**: Required for all function signatures

### Code Formatting

```bash
# Format code with black
black src/

# Check with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

### Documentation Standards

- All public functions/classes must have docstrings
- Use Google-style docstrings
- Include type hints in signatures
- Add inline comments for complex logic

Example:
```python
def detect_gesture(frame: np.ndarray, confidence_threshold: float = 0.8) -> Optional[str]:
    """Detect hand gesture in the given frame.

    Args:
        frame: Input image as numpy array (BGR format)
        confidence_threshold: Minimum confidence score (0.0 to 1.0)

    Returns:
        Detected gesture name or None if no gesture detected

    Raises:
        ValueError: If frame is empty or invalid format
    """
    # Implementation
```

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_<module>.py`
- Name test functions `test_<functionality>`
- Use pytest fixtures for setup/teardown
- Aim for >80% code coverage

```python
import pytest
from src.gesture_detector import GestureDetector

@pytest.fixture
def detector():
    return GestureDetector(confidence_threshold=0.8)

def test_thumbs_up_detection(detector):
    # Arrange
    test_frame = load_test_image("thumbs_up.jpg")

    # Act
    gesture = detector.detect(test_frame)

    # Assert
    assert gesture == "thumbs_up"
    assert detector.last_confidence > 0.8
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Run specific test file
pytest tests/test_gesture_detector.py

# Run tests matching pattern
pytest -k "thumbs" tests/
```

## Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(gestures): add support for rock/paper/scissors gestures

Implemented new gesture detection for rock, paper, and scissors hand shapes.
Added corresponding animation effects and updated UI to enable/disable these gestures.

Closes #123
```

```
fix(virtual-camera): resolve camera not appearing in Teams

Fixed DirectShow registration issue that prevented virtual camera from being
detected in Microsoft Teams. Updated registry entries and added retry logic.

Fixes #456
```

## Adding New Gestures

To add a new gesture:

1. **Define gesture detection logic** in `src/gesture_detector.py`
2. **Create animation effect** in `src/effects/your_effect.py`
3. **Add configuration** to `src/config.py`
4. **Update UI** in `src/ui/main_window.py`
5. **Add tests** in `tests/test_gesture_detector.py`
6. **Update documentation** in `docs/GESTURES.md`

Example gesture implementation:

```python
# src/gesture_detector.py
class GestureDetector:
    def _detect_custom_gesture(self, hand_landmarks):
        """Detect your custom gesture."""
        # Landmark indices for MediaPipe hands
        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]

        # Your detection logic here
        distance = self._calculate_distance(thumb_tip, index_tip)

        if distance < threshold:
            return True, 0.95  # confidence
        return False, 0.0
```

## Adding New Animation Effects

Animation effects should inherit from `BaseEffect`:

```python
# src/effects/my_effect.py
from src.effects.base_effect import BaseEffect
import cv2
import numpy as np

class MyEffect(BaseEffect):
    """My custom animation effect."""

    def __init__(self, duration: float = 3.0):
        super().__init__(duration)
        self.initialize_resources()

    def initialize_resources(self):
        """Load any required assets (images, sprites, etc.)."""
        pass

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        """Render effect on the frame.

        Args:
            frame: Input video frame
            progress: Animation progress (0.0 to 1.0)

        Returns:
            Frame with effect applied
        """
        # Your rendering logic
        return frame

    def cleanup(self):
        """Clean up resources."""
        pass
```

## Performance Optimization

When contributing performance-critical code:

- **Profile before optimizing**: Use `cProfile` or `line_profiler`
- **Benchmark changes**: Run `scripts/benchmark.py` before and after
- **Consider vectorization**: Use NumPy operations instead of loops
- **GPU acceleration**: Use CUDA/OpenCL where applicable
- **Memory efficiency**: Avoid unnecessary copies, use in-place operations

## Documentation

### Updating Documentation

- API documentation: `docs/API.md`
- Architecture: `docs/ARCHITECTURE.md`
- User guides: `docs/` directory
- Inline code documentation: Docstrings

### Building Documentation

```bash
# Generate API documentation
pdoc --html --output-dir docs/api src/

# Build user documentation (if using Sphinx)
cd docs/
make html
```

## Release Process

Releases are handled by maintainers:

1. Update version in `setup.py` and `src/__version__.py`
2. Update `CHANGELOG.md` with release notes
3. Create git tag: `git tag -a v1.2.0 -m "Release v1.2.0"`
4. Push tag: `git push origin v1.2.0`
5. GitHub Actions builds and publishes release

## Getting Help

- **Questions**: Use [GitHub Discussions](https://github.com/yourusername/reactions-app/discussions)
- **Bugs**: File an [issue](https://github.com/yourusername/reactions-app/issues)
- **Chat**: Join our [Discord server](https://discord.gg/reactions-app)
- **Email**: dev@reactions-app.com

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes

Thank you for contributing to Camera Reactions! 🎉
