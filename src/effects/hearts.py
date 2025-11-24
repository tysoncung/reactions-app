"""Hearts animation effect."""

import cv2
import numpy as np
import random
from .base_effect import BaseEffect


class HeartsEffect(BaseEffect):
    """Floating hearts animation."""

    def __init__(self, duration: float = 3.0, num_hearts: int = 20):
        """Initialize hearts effect.

        Args:
            duration: Effect duration
            num_hearts: Number of hearts to render
        """
        super().__init__(duration)
        self.num_hearts = num_hearts
        self.hearts = []
        self._initialize_hearts()

    def _initialize_hearts(self) -> None:
        """Initialize heart particles."""
        for _ in range(self.num_hearts):
            self.hearts.append({
                'x': random.random(),  # Normalized position (0-1)
                'y': random.random(),
                'size': random.randint(20, 60),
                'speed': random.uniform(0.3, 0.8),
                'phase': random.uniform(0, 2 * np.pi),  # For horizontal wobble
                'color': (random.randint(200, 255), random.randint(50, 150), random.randint(150, 255))
            })

    def _draw_heart(
        self,
        frame: np.ndarray,
        center_x: int,
        center_y: int,
        size: int,
        color: tuple,
        alpha: float = 1.0
    ) -> np.ndarray:
        """Draw a heart shape on the frame.

        Args:
            frame: Input frame
            center_x: Heart center X coordinate
            center_y: Heart center Y coordinate
            size: Heart size
            color: BGR color tuple
            alpha: Opacity (0.0 to 1.0)

        Returns:
            Frame with heart drawn
        """
        # Create overlay for alpha blending
        overlay = frame.copy()

        # Heart shape using Bezier curves approximation
        pts = []
        for angle in range(0, 360, 10):
            t = np.radians(angle)
            # Heart curve parametric equation
            x = 16 * np.sin(t)**3
            y = -(13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))

            # Scale and translate
            px = int(center_x + (x * size / 20))
            py = int(center_y + (y * size / 20))
            pts.append([px, py])

        pts = np.array(pts, np.int32)

        # Draw filled heart
        cv2.fillPoly(overlay, [pts], color)

        # Apply alpha blending
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        """Render hearts effect.

        Args:
            frame: Input frame
            progress: Animation progress (0.0 to 1.0)

        Returns:
            Frame with hearts rendered
        """
        height, width = frame.shape[:2]

        for heart in self.hearts:
            # Calculate position with upward movement and horizontal wobble
            y_pos = heart['y'] + heart['speed'] * progress
            x_wobble = 0.05 * np.sin(heart['phase'] + progress * 4 * np.pi)
            x_pos = heart['x'] + x_wobble

            # Wrap around if off screen
            if y_pos < 0:
                y_pos += 1.0

            # Convert to pixel coordinates
            px = int(x_pos * width)
            py = int((1.0 - y_pos) * height)  # Flip Y (0 at bottom)

            # Fade in/out
            if progress < 0.2:
                alpha = progress / 0.2
            elif progress > 0.8:
                alpha = (1.0 - progress) / 0.2
            else:
                alpha = 1.0

            # Draw heart if on screen
            if 0 <= px < width and 0 <= py < height:
                frame = self._draw_heart(
                    frame, px, py, heart['size'], heart['color'], alpha
                )

        return frame

    def cleanup(self) -> None:
        """Clean up hearts effect."""
        self.hearts.clear()
