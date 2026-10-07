import cv2

# Replace YOUR_PHONE_IP with the Wi-Fi IP shown in DroidCam
CAMERA_URL = "http://192.168.29.97:4747/video"

print("[INFO] Connecting to DroidCam...")

cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("[ERROR] Could not connect to DroidCam.")
    raise SystemExit(1)

print("[OK] DroidCam connected.")

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("[ERROR] Could not receive frame.")
            break

        cv2.imshow("Kinetic-UI | Camera Test", frame)

        # Press Q while the camera window is selected to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("[OK] Camera released safely.")

