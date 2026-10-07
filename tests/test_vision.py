import cv2

from vision.hand_tracking import HandTracker


# Use the same DroidCam IP that worked in our camera test
CAMERA_URL = "http://192.168.29.97:4747/video"


def main():
    cap = cv2.VideoCapture(CAMERA_URL)

    if not cap.isOpened():
        print("[ERROR] Could not connect to DroidCam.")
        return

    tracker = HandTracker()

    print("[OK] Camera connected.")
    print("[OK] HandTracker loaded.")
    print("[INFO] Show one hand to the camera.")
    print("[INFO] Press Q to quit.")

    try:
        while True:
            success, frame = cap.read()

            if not success:
                print("[ERROR] Failed to read camera frame.")
                break

            landmarks, result = tracker.detect(frame)

            if landmarks:
                print(
                    f"\r[DETECTED] {len(landmarks)} landmarks",
                    end=""
                )

                height, width, _ = frame.shape

                # Convert normalized coordinates into pixel coordinates
                for x, y, z in landmarks:
                    pixel_x = int(x * width)
                    pixel_y = int(y * height)

                    cv2.circle(
                        frame,
                        (pixel_x, pixel_y),
                        5,
                        (0, 255, 0),
                        -1
                    )

            cv2.imshow("Kinetic-UI | Hand Tracking", frame)

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        tracker.close()
        cap.release()
        cv2.destroyAllWindows()

        print("\n[OK] Vision system shut down safely.")


if __name__ == "__main__":
    main()

