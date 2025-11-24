"""Tests for gesture detector."""

import pytest
import numpy as np
from src.gesture_detector import GestureDetector


@pytest.fixture
def detector():
    """Create gesture detector instance."""
    return GestureDetector(confidence_threshold=0.8)


def test_detector_initialization(detector):
    """Test detector initializes correctly."""
    assert detector is not None
    assert detector.confidence_threshold == 0.8


def test_detect_no_hands():
    """Test detection with no hands in frame."""
    detector = GestureDetector()

    # Create blank frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    gesture = detector.detect(frame)
    assert gesture is None


def test_cleanup(detector):
    """Test cleanup releases resources."""
    detector.cleanup()
    # Should not raise exception
