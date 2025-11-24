"""Base class for animation effects."""

from abc import ABC, abstractmethod
import numpy as np


class BaseEffect(ABC):
    """Abstract base class for visual effects."""

    def __init__(self, duration: float = 3.0):
        """Initialize effect.

        Args:
            duration: Effect duration in seconds
        """
        self.duration = duration

    @abstractmethod
    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        """Render effect on frame.

        Args:
            frame: Input BGR image
            progress: Animation progress from 0.0 to 1.0

        Returns:
            Frame with effect rendered
        """
        pass

    def cleanup(self) -> None:
        """Clean up resources. Override if needed."""
        pass
