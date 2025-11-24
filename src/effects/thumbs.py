"""Thumbs up/down animation effect."""

import cv2
import numpy as np
from .base_effect import BaseEffect


class ThumbsEffect(BaseEffect):
    """Thumbs up or down animation."""

    def __init__(self, duration: float = 2.0, direction: str = "up"):
        super().__init__(duration)
        self.direction = direction  # "up" or "down"

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        height, width = frame.shape[:2]

        # Scale and fade animation
        scale = 0.5 + progress * 0.5  # Grow from 50% to 100%
        alpha = 1.0 - progress  # Fade out

        # Position (center)
        cx, cy = width // 2, height // 2

        # Emoji size
        size = int(100 * scale)

        # Draw thumbs emoji (simplified as colored circle with text)
        color = (0, 255, 0) if self.direction == "up" else (0, 0, 255)
        overlay = frame.copy()
        cv2.circle(overlay, (cx, cy), size, color, -1)

        # Draw thumb symbol
        text = "👍" if self.direction == "up" else "👎"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(overlay, text, (cx - size//2, cy + size//2), font, size/50, (255, 255, 255), 2)

        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        return frame
