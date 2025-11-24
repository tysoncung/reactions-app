"""Virtual camera integration for feeding processed video to apps.

This module creates a virtual camera device that video conferencing
applications can use as a camera source.
"""

import logging
import threading
from typing import Optional
import cv2
import numpy as np

try:
    import pyvirtualcam
    VIRTUAL_CAM_AVAILABLE = True
except ImportError:
    VIRTUAL_CAM_AVAILABLE = False
    logging.warning("pyvirtualcam not available - virtual camera disabled")

logger = logging.getLogger(__name__)


class VirtualCamera:
    """Virtual camera for outputting processed video frames."""

    def __init__(
        self,
        camera_name: str = "Camera Reactions Virtual Camera",
        width: int = 1280,
        height: int = 720,
        fps: int = 30
    ):
        """Initialize virtual camera.

        Args:
            camera_name: Name of the virtual camera device
            width: Output width in pixels
            height: Output height in pixels
            fps: Frames per second
        """
        self.camera_name = camera_name
        self.width = width
        self.height = height
        self.fps = fps

        self.camera: Optional[pyvirtualcam.Camera] = None
        self.running = False
        self.frame_lock = threading.Lock()
        self.latest_frame: Optional[np.ndarray] = None

        if VIRTUAL_CAM_AVAILABLE:
            self._initialize_camera()
        else:
            logger.error("Virtual camera not available - install pyvirtualcam")

    def _initialize_camera(self) -> None:
        """Initialize the virtual camera device."""
        try:
            self.camera = pyvirtualcam.Camera(
                width=self.width,
                height=self.height,
                fps=self.fps,
                fmt=pyvirtualcam.PixelFormat.BGR
            )
            self.running = True
            logger.info(
                f"Virtual camera initialized: {self.camera_name} "
                f"({self.width}x{self.height} @ {self.fps}fps)"
            )
        except Exception as e:
            logger.error(f"Failed to initialize virtual camera: {e}")
            self.camera = None

    def send_frame(self, frame: np.ndarray) -> bool:
        """Send a frame to the virtual camera.

        Args:
            frame: BGR image to send

        Returns:
            True if frame sent successfully
        """
        if not self.running or not self.camera:
            return False

        try:
            # Resize frame if necessary
            if frame.shape[:2] != (self.height, self.width):
                frame = cv2.resize(frame, (self.width, self.height))

            # Send frame to virtual camera
            self.camera.send(frame)

            with self.frame_lock:
                self.latest_frame = frame

            return True

        except Exception as e:
            logger.error(f"Error sending frame to virtual camera: {e}")
            return False

    def get_latest_frame(self) -> Optional[np.ndarray]:
        """Get the latest frame sent to virtual camera.

        Returns:
            Latest frame or None
        """
        with self.frame_lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def is_running(self) -> bool:
        """Check if virtual camera is running.

        Returns:
            True if camera is active
        """
        return self.running and self.camera is not None

    def stop(self) -> None:
        """Stop the virtual camera."""
        if self.camera:
            self.running = False
            self.camera.close()
            self.camera = None
            logger.info("Virtual camera stopped")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
