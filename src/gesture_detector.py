"""Hand gesture detection using MediaPipe.

This module implements real-time hand gesture recognition using Google's
MediaPipe Hands solution. It detects various hand gestures like thumbs up,
peace sign, heart hands, etc.
"""

import logging
from typing import Optional, Tuple
import cv2
import mediapipe as mp
import numpy as np

logger = logging.getLogger(__name__)


class GestureDetector:
    """Detects hand gestures in video frames using MediaPipe."""

    def __init__(self, confidence_threshold: float = 0.8):
        """Initialize gesture detector.

        Args:
            confidence_threshold: Minimum confidence for gesture detection (0.0-1.0)
        """
        self.confidence_threshold = confidence_threshold
        self.last_gesture: Optional[str] = None
        self.last_confidence: float = 0.0

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

        logger.info(f"GestureDetector initialized (threshold={confidence_threshold})")

    def detect(self, frame: np.ndarray) -> Optional[str]:
        """Detect gesture in the given frame.

        Args:
            frame: Input BGR image

        Returns:
            Detected gesture name or None
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            self.last_gesture = None
            return None

        # Analyze detected hands
        num_hands = len(results.multi_hand_landmarks)

        if num_hands == 1:
            gesture, confidence = self._detect_single_hand_gesture(
                results.multi_hand_landmarks[0]
            )
        elif num_hands == 2:
            gesture, confidence = self._detect_two_hand_gesture(
                results.multi_hand_landmarks[0],
                results.multi_hand_landmarks[1]
            )
        else:
            gesture, confidence = None, 0.0

        self.last_confidence = confidence

        if confidence >= self.confidence_threshold:
            self.last_gesture = gesture
            return gesture

        return None

    def _detect_single_hand_gesture(
        self, hand_landmarks
    ) -> Tuple[Optional[str], float]:
        """Detect gesture from a single hand.

        Args:
            hand_landmarks: MediaPipe hand landmarks

        Returns:
            Tuple of (gesture_name, confidence)
        """
        # Extract landmark positions
        landmarks = hand_landmarks.landmark

        # Thumbs up detection
        if self._is_thumbs_up(landmarks):
            return "thumbs_up", 0.9

        # Thumbs down detection
        if self._is_thumbs_down(landmarks):
            return "thumbs_down", 0.9

        # Peace sign detection
        if self._is_peace_sign(landmarks):
            return "peace_sign", 0.85

        # Raised fist detection
        if self._is_raised_fist(landmarks):
            return "raised_fist", 0.85

        return None, 0.0

    def _detect_two_hand_gesture(
        self, left_hand, right_hand
    ) -> Tuple[Optional[str], float]:
        """Detect gesture requiring two hands.

        Args:
            left_hand: Left hand landmarks
            right_hand: Right hand landmarks

        Returns:
            Tuple of (gesture_name, confidence)
        """
        # Two thumbs up detection
        left_landmarks = left_hand.landmark
        right_landmarks = right_hand.landmark

        if self._is_thumbs_up(left_landmarks) and self._is_thumbs_up(right_landmarks):
            return "two_thumbs_up", 0.95

        # Heart hands detection
        if self._is_heart_hands(left_hand, right_hand):
            return "heart_hands", 0.9

        return None, 0.0

    def _is_thumbs_up(self, landmarks) -> bool:
        """Check if hand is showing thumbs up.

        Args:
            landmarks: Hand landmarks

        Returns:
            True if thumbs up detected
        """
        # Thumb tip (4) should be above thumb IP (3)
        # Other fingers should be folded
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_mcp = landmarks[5]

        # Thumb is extended upward
        thumb_up = thumb_tip.y < thumb_ip.y

        # Index finger is folded
        index_folded = index_tip.y > index_mcp.y

        return thumb_up and index_folded

    def _is_thumbs_down(self, landmarks) -> bool:
        """Check if hand is showing thumbs down.

        Args:
            landmarks: Hand landmarks

        Returns:
            True if thumbs down detected
        """
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        index_tip = landmarks[8]
        index_mcp = landmarks[5]

        # Thumb is extended downward
        thumb_down = thumb_tip.y > thumb_ip.y

        # Index finger is folded
        index_folded = index_tip.y > index_mcp.y

        return thumb_down and index_folded

    def _is_peace_sign(self, landmarks) -> bool:
        """Check if hand is showing peace sign (V).

        Args:
            landmarks: Hand landmarks

        Returns:
            True if peace sign detected
        """
        # Index and middle fingers extended, others folded
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        middle_pip = landmarks[10]
        ring_tip = landmarks[16]
        ring_pip = landmarks[14]

        index_extended = index_tip.y < index_pip.y
        middle_extended = middle_tip.y < middle_pip.y
        ring_folded = ring_tip.y > ring_pip.y

        return index_extended and middle_extended and ring_folded

    def _is_raised_fist(self, landmarks) -> bool:
        """Check if hand is showing raised fist.

        Args:
            landmarks: Hand landmarks

        Returns:
            True if raised fist detected
        """
        # All fingers folded
        fingers_folded = all(
            landmarks[tip].y > landmarks[pip].y
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]
        )

        return fingers_folded

    def _is_heart_hands(self, left_hand, right_hand) -> bool:
        """Check if two hands are forming a heart shape.

        Args:
            left_hand: Left hand landmarks
            right_hand: Right hand landmarks

        Returns:
            True if heart hands detected
        """
        # Simplified check: thumbs and index fingers close together
        left_thumb = left_hand.landmark[4]
        right_thumb = right_hand.landmark[4]

        distance = np.sqrt(
            (left_thumb.x - right_thumb.x)**2 +
            (left_thumb.y - right_thumb.y)**2
        )

        # Thumbs are close together (forming top of heart)
        return distance < 0.15

    def draw_landmarks(self, frame: np.ndarray, results) -> np.ndarray:
        """Draw hand landmarks on frame for debugging.

        Args:
            frame: Input frame
            results: MediaPipe results

        Returns:
            Frame with landmarks drawn
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def cleanup(self) -> None:
        """Release resources."""
        if self.hands:
            self.hands.close()
        logger.info("GestureDetector cleanup complete")
