"""Animation engine for rendering visual effects.

This module manages and renders animated effects like hearts, confetti,
balloons, etc. on video frames.
"""

import logging
import time
from typing import Dict, Optional
import cv2
import numpy as np
from pathlib import Path

from effects.hearts import HeartsEffect
from effects.confetti import ConfettiEffect
from effects.balloons import BalloonsEffect
from effects.thumbs import ThumbsEffect
from effects.lasers import LasersEffect

logger = logging.getLogger(__name__)


class AnimationEngine:
    """Manages and renders animation effects on video frames."""

    def __init__(self, effect_duration: float = 3.0):
        """Initialize animation engine.

        Args:
            effect_duration: Default duration for effects in seconds
        """
        self.effect_duration = effect_duration
        self.active_effects: Dict[str, Dict] = {}

        # Initialize effect renderers
        self.effect_renderers = {
            "thumbs_up": ThumbsEffect(direction="up"),
            "thumbs_down": ThumbsEffect(direction="down"),
            "two_thumbs_up": ConfettiEffect(),
            "peace_sign": BalloonsEffect(),
            "heart_hands": HeartsEffect(),
            "raised_fist": LasersEffect(),
        }

        logger.info("AnimationEngine initialized")

    def trigger_effect(self, gesture_name: str, duration: Optional[float] = None) -> None:
        """Trigger an animation effect for a gesture.

        Args:
            gesture_name: Name of the gesture
            duration: Effect duration (uses default if None)
        """
        if gesture_name not in self.effect_renderers:
            logger.warning(f"Unknown gesture: {gesture_name}")
            return

        # Don't restart if effect is already active
        if gesture_name in self.active_effects:
            return

        effect_duration = duration or self.effect_duration

        self.active_effects[gesture_name] = {
            "start_time": time.time(),
            "duration": effect_duration,
            "renderer": self.effect_renderers[gesture_name]
        }

        logger.debug(f"Triggered effect for {gesture_name} (duration={effect_duration}s)")

    def render(self, frame: np.ndarray) -> np.ndarray:
        """Render all active effects on the frame.

        Args:
            frame: Input video frame

        Returns:
            Frame with effects rendered
        """
        current_time = time.time()
        output_frame = frame.copy()

        # Track effects to remove
        to_remove = []

        # Render each active effect
        for gesture_name, effect_data in self.active_effects.items():
            elapsed = current_time - effect_data["start_time"]
            duration = effect_data["duration"]

            if elapsed >= duration:
                to_remove.append(gesture_name)
                continue

            # Calculate progress (0.0 to 1.0)
            progress = elapsed / duration

            # Render effect
            renderer = effect_data["renderer"]
            output_frame = renderer.render(output_frame, progress)

        # Remove completed effects
        for gesture_name in to_remove:
            del self.active_effects[gesture_name]
            logger.debug(f"Effect completed: {gesture_name}")

        return output_frame

    def clear_effects(self) -> None:
        """Clear all active effects."""
        self.active_effects.clear()
        logger.debug("All effects cleared")

    def cleanup(self) -> None:
        """Clean up resources used by effects."""
        for renderer in self.effect_renderers.values():
            renderer.cleanup()
        self.active_effects.clear()
        logger.info("AnimationEngine cleanup complete")
