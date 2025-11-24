"""Main application entry point for Camera Reactions.

This module initializes and runs the Camera Reactions application,
coordinating between gesture detection, animation rendering, virtual
camera output, and the user interface.
"""

import sys
import logging
import signal
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

from config import Config
from gesture_detector import GestureDetector
from animation_engine import AnimationEngine
from virtual_camera import VirtualCamera
from ui.main_window import MainWindow


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/camera_reactions.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CameraReactionsApp:
    """Main application class coordinating all components."""

    def __init__(self):
        """Initialize the Camera Reactions application."""
        self.config = Config()
        self.gesture_detector: Optional[GestureDetector] = None
        self.animation_engine: Optional[AnimationEngine] = None
        self.virtual_camera: Optional[VirtualCamera] = None
        self.main_window: Optional[MainWindow] = None
        self.running = False

        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)

    def initialize_components(self) -> bool:
        """Initialize all application components.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing Camera Reactions...")

            # Initialize gesture detector
            self.gesture_detector = GestureDetector(
                confidence_threshold=self.config.get("gesture_confidence", 0.8)
            )
            logger.info("Gesture detector initialized")

            # Initialize animation engine
            self.animation_engine = AnimationEngine(
                effect_duration=self.config.get("effect_duration", 3.0)
            )
            logger.info("Animation engine initialized")

            # Initialize virtual camera
            self.virtual_camera = VirtualCamera(
                camera_name="Camera Reactions Virtual Camera",
                width=self.config.get("camera_width", 1280),
                height=self.config.get("camera_height", 720),
                fps=self.config.get("camera_fps", 30)
            )
            logger.info("Virtual camera initialized")

            return True

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}", exc_info=True)
            return False

    def start(self) -> None:
        """Start the camera reactions system."""
        if not self.initialize_components():
            QMessageBox.critical(
                None,
                "Initialization Error",
                "Failed to initialize Camera Reactions. Please check logs for details."
            )
            sys.exit(1)

        self.running = True
        logger.info("Camera Reactions started successfully")

    def stop(self) -> None:
        """Stop the camera reactions system and cleanup resources."""
        logger.info("Stopping Camera Reactions...")
        self.running = False

        if self.virtual_camera:
            self.virtual_camera.stop()

        if self.animation_engine:
            self.animation_engine.cleanup()

        if self.gesture_detector:
            self.gesture_detector.cleanup()

        logger.info("Camera Reactions stopped")

    def process_frame(self, frame):
        """Process a single video frame.

        Args:
            frame: Input video frame from webcam

        Returns:
            Processed frame with effects applied
        """
        if not self.running:
            return frame

        # Detect gesture
        gesture = self.gesture_detector.detect(frame)

        # Trigger animation if gesture detected
        if gesture and self.config.is_gesture_enabled(gesture):
            self.animation_engine.trigger_effect(gesture)
            logger.debug(f"Triggered effect for gesture: {gesture}")

        # Render animations on frame
        output_frame = self.animation_engine.render(frame)

        return output_frame


def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown."""
    logger.info("Received shutdown signal")
    QApplication.quit()


def main():
    """Application entry point."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Camera Reactions")
    app.setOrganizationName("Camera Reactions Team")

    # Create and start main application
    camera_app = CameraReactionsApp()

    try:
        # Create main window
        window = MainWindow(camera_app)
        camera_app.main_window = window
        window.show()

        # Start application
        camera_app.start()

        # Run Qt event loop
        exit_code = app.exec_()

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        QMessageBox.critical(
            None,
            "Application Error",
            f"An error occurred: {str(e)}\n\nPlease check logs for details."
        )
        exit_code = 1

    finally:
        # Cleanup
        camera_app.stop()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
