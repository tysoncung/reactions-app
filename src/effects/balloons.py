"""Balloon animation effect - simplified implementation."""

import cv2
import numpy as np
import random
from .base_effect import BaseEffect


class BalloonsEffect(BaseEffect):
    """Rising balloons animation."""

    def __init__(self, duration: float = 3.0, num_balloons: int = 10):
        super().__init__(duration)
        self.num_balloons = num_balloons
        self.balloons = [
            {
                'x': random.uniform(0.1, 0.9),
                'y': random.uniform(0.7, 1.0),
                'size': random.randint(30, 60),
                'speed': random.uniform(0.2, 0.5),
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            }
            for _ in range(num_balloons)
        ]

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        height, width = frame.shape[:2]
        for balloon in self.balloons:
            y_pos = balloon['y'] - balloon['speed'] * progress
            if y_pos < 0:
                continue
            px, py = int(balloon['x'] * width), int(y_pos * height)
            if 0 <= px < width and 0 <= py < height:
                cv2.circle(frame, (px, py), balloon['size'], balloon['color'], -1)
                cv2.line(frame, (px, py + balloon['size']), (px, py + balloon['size'] + 20), (150, 150, 150), 2)
        return frame
