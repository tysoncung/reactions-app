"""Configuration management for Camera Reactions.

Handles loading, saving, and accessing application settings.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for application settings."""

    DEFAULT_CONFIG = {
        "camera_width": 1280,
        "camera_height": 720,
        "camera_fps": 30,
        "camera_index": 0,
        "gesture_confidence": 0.8,
        "effect_duration": 3.0,
        "enabled_gestures": {
            "thumbs_up": True,
            "thumbs_down": True,
            "two_thumbs_up": True,
            "peace_sign": True,
            "heart_hands": True,
            "raised_fist": True,
        },
        "virtual_camera_name": "Camera Reactions Virtual Camera",
        "show_debug_overlay": False,
        "enable_gpu": True,
        "log_level": "INFO",
    }

    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file
        """
        self.config_file = Path(config_file)
        self.settings: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    loaded_config = json.load(f)
                    self.settings.update(loaded_config)
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("Config file not found, using defaults")
            self.save()  # Create default config file

    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value
        self.save()

    def is_gesture_enabled(self, gesture_name: str) -> bool:
        """Check if a gesture is enabled.

        Args:
            gesture_name: Name of the gesture

        Returns:
            True if gesture is enabled, False otherwise
        """
        enabled_gestures = self.get("enabled_gestures", {})
        return enabled_gestures.get(gesture_name, False)

    def enable_gesture(self, gesture_name: str, enabled: bool = True) -> None:
        """Enable or disable a gesture.

        Args:
            gesture_name: Name of the gesture
            enabled: Whether to enable the gesture
        """
        enabled_gestures = self.get("enabled_gestures", {})
        enabled_gestures[gesture_name] = enabled
        self.set("enabled_gestures", enabled_gestures)

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self.DEFAULT_CONFIG.copy()
        self.save()
        logger.info("Configuration reset to defaults")
