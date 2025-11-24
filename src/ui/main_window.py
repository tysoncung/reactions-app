"""Main application window."""

import logging
from typing import Optional
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QCheckBox, QGroupBox,
    QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window for Camera Reactions."""

    def __init__(self, app):
        """Initialize main window.

        Args:
            app: CameraReactionsApp instance
        """
        super().__init__()
        self.app = app
        self.camera = None
        self.timer = QTimer()

        self.setWindowTitle("Camera Reactions")
        self.setGeometry(100, 100, 800, 600)

        self._create_ui()
        self._create_tray_icon()
        self._start_camera()

    def _create_ui(self) -> None:
        """Create the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(640, 480)
        self.preview_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.preview_label)

        # Controls
        controls_layout = QHBoxLayout()

        # Camera selection
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["Camera 0", "Camera 1"])
        controls_layout.addWidget(QLabel("Camera:"))
        controls_layout.addWidget(self.camera_combo)

        # Start/Stop button
        self.start_button = QPushButton("Stop")
        self.start_button.clicked.connect(self._toggle_camera)
        controls_layout.addWidget(self.start_button)

        layout.addLayout(controls_layout)

        # Gesture toggles
        gestures_group = QGroupBox("Enabled Gestures")
        gestures_layout = QVBoxLayout()

        self.gesture_checkboxes = {}
        gestures = [
            ("thumbs_up", "👍 Thumbs Up"),
            ("thumbs_down", "👎 Thumbs Down"),
            ("two_thumbs_up", "👍👍 Two Thumbs Up"),
            ("peace_sign", "✌️ Peace Sign"),
            ("heart_hands", "💗 Heart Hands"),
            ("raised_fist", "✊ Raised Fist"),
        ]

        for gesture_id, gesture_name in gestures:
            checkbox = QCheckBox(gesture_name)
            checkbox.setChecked(self.app.config.is_gesture_enabled(gesture_id))
            checkbox.stateChanged.connect(
                lambda state, gid=gesture_id: self._toggle_gesture(gid, state)
            )
            self.gesture_checkboxes[gesture_id] = checkbox
            gestures_layout.addWidget(checkbox)

        gestures_group.setLayout(gestures_layout)
        layout.addWidget(gestures_group)

    def _create_tray_icon(self) -> None:
        """Create system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon())  # Set app icon

        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _start_camera(self) -> None:
        """Start camera capture."""
        camera_index = self.app.config.get("camera_index", 0)
        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            logger.error(f"Failed to open camera {camera_index}")
            return

        # Set resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Start timer for frame updates
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(33)  # ~30 FPS

        logger.info("Camera started")

    def _update_frame(self) -> None:
        """Update preview frame."""
        if not self.camera or not self.camera.isOpened():
            return

        ret, frame = self.camera.read()
        if not ret:
            return

        # Process frame through app pipeline
        processed_frame = self.app.process_frame(frame)

        # Send to virtual camera
        if self.app.virtual_camera:
            self.app.virtual_camera.send_frame(processed_frame)

        # Update preview
        self._display_frame(processed_frame)

    def _display_frame(self, frame: np.ndarray) -> None:
        """Display frame in preview label.

        Args:
            frame: BGR image to display
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Scale to fit label
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.preview_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.preview_label.setPixmap(scaled_pixmap)

    def _toggle_camera(self) -> None:
        """Toggle camera on/off."""
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Start")
            logger.info("Camera stopped")
        else:
            self.timer.start(33)
            self.start_button.setText("Stop")
            logger.info("Camera started")

    def _toggle_gesture(self, gesture_id: str, state: int) -> None:
        """Toggle gesture enabled state.

        Args:
            gesture_id: Gesture identifier
            state: Checkbox state
        """
        enabled = state == Qt.Checked
        self.app.config.enable_gesture(gesture_id, enabled)
        logger.debug(f"Gesture {gesture_id} {'enabled' if enabled else 'disabled'}")

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.camera:
            self.camera.release()
        self.timer.stop()
        event.accept()
