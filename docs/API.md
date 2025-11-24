# Camera Reactions API Documentation

## Core Modules

### GestureDetector

Hand gesture recognition using MediaPipe.

```python
from src.gesture_detector import GestureDetector

detector = GestureDetector(confidence_threshold=0.8)
gesture = detector.detect(frame)
```

**Methods:**
- `detect(frame: np.ndarray) -> Optional[str]`: Detect gesture in frame
- `cleanup() -> None`: Release resources

**Supported Gestures:**
- `thumbs_up`: Single thumbs up
- `thumbs_down`: Single thumbs down
- `two_thumbs_up`: Both hands thumbs up
- `peace_sign`: Peace/victory sign
- `heart_hands`: Hands forming heart shape
- `raised_fist`: Closed fist raised

### AnimationEngine

Manages and renders visual effects.

```python
from src.animation_engine import AnimationEngine

engine = AnimationEngine(effect_duration=3.0)
engine.trigger_effect("heart_hands")
output_frame = engine.render(input_frame)
```

**Methods:**
- `trigger_effect(gesture_name: str, duration: Optional[float]) -> None`
- `render(frame: np.ndarray) -> np.ndarray`
- `clear_effects() -> None`
- `cleanup() -> None`

### VirtualCamera

Virtual camera driver interface.

```python
from src.virtual_camera import VirtualCamera

camera = VirtualCamera(
    camera_name="Camera Reactions Virtual Camera",
    width=1280,
    height=720,
    fps=30
)
camera.send_frame(frame)
```

**Methods:**
- `send_frame(frame: np.ndarray) -> bool`
- `get_latest_frame() -> Optional[np.ndarray]`
- `is_running() -> bool`
- `stop() -> None`

### Config

Configuration management.

```python
from src.config import Config

config = Config()
value = config.get("camera_width", default=1280)
config.set("gesture_confidence", 0.9)
config.enable_gesture("thumbs_up", True)
```

**Methods:**
- `get(key: str, default: Any) -> Any`
- `set(key: str, value: Any) -> None`
- `is_gesture_enabled(gesture_name: str) -> bool`
- `enable_gesture(gesture_name: str, enabled: bool) -> None`
- `reset_to_defaults() -> None`

## Effect Classes

All effects inherit from `BaseEffect`.

### BaseEffect

```python
class CustomEffect(BaseEffect):
    def render(self, frame: np.ndarray, progress: float) -> np.ndarray:
        # Render effect
        return frame
```

Available effects:
- `HeartsEffect`: Floating hearts animation
- `ConfettiEffect`: Confetti and fireworks
- `BalloonsEffect`: Rising balloons
- `ThumbsEffect`: Thumbs up/down display
- `LasersEffect`: Laser beam effects

## Configuration File Format

`config.json`:
```json
{
    "camera_width": 1280,
    "camera_height": 720,
    "camera_fps": 30,
    "gesture_confidence": 0.8,
    "effect_duration": 3.0,
    "enabled_gestures": {
        "thumbs_up": true,
        "thumbs_down": true,
        "two_thumbs_up": true,
        "peace_sign": true,
        "heart_hands": true,
        "raised_fist": true
    }
}
```

## Events and Callbacks

Currently the application uses polling. Future versions may add callback support:

```python
# Future API (not yet implemented)
def on_gesture_detected(gesture_name, confidence):
    print(f"Detected: {gesture_name} ({confidence})")

detector.on_gesture = on_gesture_detected
```
