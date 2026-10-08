# Part 1 — Hand Detection and Landmark Tracking

## Objective
Convert live camera frames into a consistent set of 21 hand landmarks for Kinetic-UI's gesture-recognition module (Part 2).

## Current status
**Working prototype tested on Ubuntu 22.04:** DroidCam video reaches OpenCV, MediaPipe detects one hand, and 21 landmark points follow the hand in a live preview.

## Environment
- Ubuntu 22.04.5 LTS, Python 3.10.12
- Python virtual environment: `.venv/`
- OpenCV, NumPy, MediaPipe 1.1.0 (Tasks API)
- Android DroidCam over local Wi-Fi (`http://PHONE_IP:4747/video`)
- Model: `models/hand_landmarker.task` (approximately 7.5 MB)

## Relevant files
| File | Responsibility |
| --- | --- |
| `vision/hand_tracking.py` | Defines `HandTracker`, loads the model, processes frames, returns landmarks, closes detector. |
| `models/hand_landmarker.task` | Trained MediaPipe Hand Landmarker model. |
| `tests/test_camera.py` | Tests DroidCam → OpenCV video capture. |
| `tests/test_vision.py` | Displays the camera feed with detected landmarks. |
| `requirements.txt` | Python dependencies (keep updated). |

## Processing pipeline
```
Android DroidCam → OpenCV BGR frame → RGB conversion
→ MediaPipe Hand Landmarker → 21 normalized (x, y, z) tuples
→ Part 2 gesture classifier
```

## Part 1 interface
```python
from vision.hand_tracking import HandTracker

tracker = HandTracker()
landmarks, result = tracker.detect(frame)
# landmarks is [] if no hand is found; otherwise 21 (x, y, z) tuples
tracker.close()
```
- `x` and `y` are normalized image coordinates; `z` is MediaPipe's relative depth coordinate.
- `detect(frame)` accepts an OpenCV BGR image.
- Gesture decisions and OS actions must remain outside this module.

## Setup and run
From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install opencv-python numpy mediapipe
```

Ensure `models/hand_landmarker.task` is present and nonempty. Start DroidCam on the phone and connect phone and computer to the same Wi-Fi. Update `CAMERA_URL` in the test file to the IP shown by DroidCam.

```bash
python -m tests.test_vision
```

If `tests` isn't recognized as a package, add an empty `tests/__init__.py`. Hold a hand in view: the preview should show 21 tracking dots. Press **Q** in the preview window to quit.

## Implemented behavior
- Initializes MediaPipe's Tasks `HandLandmarker` in `IMAGE` mode with `num_hands=1`.
- Converts OpenCV BGR frames to MediaPipe RGB images.
- Returns an empty list when no hand is detected.
- Returns 21 `(x, y, z)` tuples for the first detected hand.
- Test preview draws green circles at the landmark positions.
- Closes the model, releases video capture, and destroys OpenCV windows on exit.

## Teammate handoff / acceptance criteria
1. Ensure the module can be imported from the repo root.
2. Keep `HandTracker.detect(frame)` returning the same landmark structure (`[]` or 21 tuples).
3. Validate on a live camera, including no-hand and hand-entering/leaving-frame cases.
4. Improve Part 1 only: optional landmark connections, FPS overlay, capture reliability, error handling, and clear documentation.
5. Do **not** add pinch classification, click commands, or OS control to Part 1.
6. Commit Part 1 work on `feature/vision` and open a pull request for review.

## Next integration step
Part 2 reads the 21 landmarks and maps gestures to standardized commands. It should not depend on MediaPipe directly.
