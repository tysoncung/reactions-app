"""Laser beams animation effect."""

import cv2
import numpy as np
import random
from .base_effect import BaseEffect


class LasersEffect(BaseEffect):
    """Laser beams shooting effect."""

    def __init__(self, duration: float = 2.0, num_beams: int = 5):
        super().__init__(duration)
        self.num_beams = num_beams
        self.beams = [
            {
                'start_x': random.uniform(0.3, 0.7),
                'start_y': random.uniform(0.4, 0.6),
                'angle': random.uniform(0, 360),
                'length': random.uniform(0.3, 0.6),
                'color': (random.randint(0, 255), random.randint(0, 255), 255)
            }
            for _ in range(num_beams)
        ]

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        height, width = frame.shape[:2]
        overlay = frame.copy()

        alpha = 0.6 if progress < 0.5 else 0.6 * (1.0 - (progress - 0.5) / 0.5)

        for beam in self.beams:
            sx = int(beam['start_x'] * width)
            sy = int(beam['start_y'] * height)

            length = int(beam['length'] * max(width, height) * progress)
            angle_rad = np.radians(beam['angle'])

            ex = int(sx + length * np.cos(angle_rad))
            ey = int(sy + length * np.sin(angle_rad))

            cv2.line(overlay, (sx, sy), (ex, ey), beam['color'], 3)

        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        return frame
