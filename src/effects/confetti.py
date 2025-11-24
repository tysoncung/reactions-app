"""Confetti and fireworks animation effect."""

import cv2
import numpy as np
import random
from .base_effect import BaseEffect


class ConfettiEffect(BaseEffect):
    """Confetti and fireworks celebration effect."""

    def __init__(self, duration: float = 3.0, num_particles: int = 100):
        """Initialize confetti effect.

        Args:
            duration: Effect duration
            num_particles: Number of confetti particles
        """
        super().__init__(duration)
        self.num_particles = num_particles
        self.particles = []
        self._initialize_particles()

    def _initialize_particles(self) -> None:
        """Initialize confetti particles."""
        colors = [
            (0, 0, 255),    # Red
            (0, 255, 0),    # Green
            (255, 0, 0),    # Blue
            (0, 255, 255),  # Yellow
            (255, 0, 255),  # Magenta
            (255, 255, 0),  # Cyan
        ]

        for _ in range(self.num_particles):
            self.particles.append({
                'x': random.uniform(0.2, 0.8),
                'y': random.uniform(0.3, 0.5),  # Start from middle-top
                'vx': random.uniform(-0.5, 0.5),  # Horizontal velocity
                'vy': random.uniform(-1.0, -0.3),  # Upward velocity
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-10, 10),
                'size': random.randint(5, 15),
                'color': random.choice(colors),
                'shape': random.choice(['rect', 'circle', 'star'])
            })

    def _draw_particle(
        self,
        frame: np.ndarray,
        x: int,
        y: int,
        size: int,
        color: tuple,
        rotation: float,
        shape: str,
        alpha: float = 1.0
    ) -> np.ndarray:
        """Draw a confetti particle.

        Args:
            frame: Input frame
            x, y: Particle position
            size: Particle size
            color: BGR color
            rotation: Rotation angle in degrees
            shape: Shape type ('rect', 'circle', 'star')
            alpha: Opacity

        Returns:
            Frame with particle drawn
        """
        overlay = frame.copy()

        if shape == 'circle':
            cv2.circle(overlay, (x, y), size // 2, color, -1)
        elif shape == 'rect':
            # Draw rotated rectangle
            pts = cv2.boxPoints(((x, y), (size, size // 2), rotation))
            pts = np.int0(pts)
            cv2.fillPoly(overlay, [pts], color)
        elif shape == 'star':
            # Simple star shape
            angle_step = 72  # 5-pointed star
            outer_r = size
            inner_r = size // 2
            pts = []
            for i in range(10):
                angle = rotation + i * angle_step / 2
                r = outer_r if i % 2 == 0 else inner_r
                px = x + int(r * np.cos(np.radians(angle)))
                py = y + int(r * np.sin(np.radians(angle)))
                pts.append([px, py])
            pts = np.array(pts, np.int32)
            cv2.fillPoly(overlay, [pts], color)

        # Apply alpha blending
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame

    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        """Render confetti effect.

        Args:
            frame: Input frame
            progress: Animation progress (0.0 to 1.0)

        Returns:
            Frame with confetti rendered
        """
        height, width = frame.shape[:2]
        gravity = 0.5  # Gravity effect

        for particle in self.particles:
            # Physics simulation
            t = progress * self.duration

            # Update position with gravity
            x = particle['x'] + particle['vx'] * t
            y = particle['y'] + particle['vy'] * t + 0.5 * gravity * t**2

            # Update rotation
            rotation = particle['rotation'] + particle['rotation_speed'] * progress * 360

            # Fade out at end
            if progress > 0.8:
                alpha = (1.0 - progress) / 0.2
            else:
                alpha = 1.0

            # Convert to pixel coordinates
            px = int(x * width)
            py = int(y * height)

            # Draw if on screen
            if 0 <= px < width and 0 <= py < height:
                frame = self._draw_particle(
                    frame, px, py,
                    particle['size'],
                    particle['color'],
                    rotation,
                    particle['shape'],
                    alpha
                )

        return frame

    def cleanup(self) -> None:
        """Clean up confetti effect."""
        self.particles.clear()
