import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:
    """
    Detects a hand in an OpenCV frame and returns
    21 normalized (x, y, z) landmarks.

    This module performs ONLY hand tracking.
    Gesture recognition belongs to Part 2.
    """

    def __init__(self, model_path="models/hand_landmarker.task"):

        # Tell MediaPipe where our trained model is located
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        # Configure the Hand Landmarker
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # Create the detector
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        """
        Takes an OpenCV BGR frame.

        Returns:
            landmarks: [(x, y, z), ...] containing 21 points
            result: raw MediaPipe detection result
        """

        # OpenCV gives us BGR.
        # MediaPipe expects RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert NumPy/OpenCV image into a MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Run hand landmark detection
        result = self.detector.detect(mp_image)

        if not result.hand_landmarks:
            return [], result

        # We're currently tracking only one hand
        hand = result.hand_landmarks[0]

        landmarks = []

        for landmark in hand:
            landmarks.append(
                (
                    landmark.x,
                    landmark.y,
                    landmark.z
                )
            )

        return landmarks, result

    def close(self):
        """Release MediaPipe resources."""
        self.detector.close()
