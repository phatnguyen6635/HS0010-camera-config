import pypylon.pylon as py
import numpy as np
import cv2
import threading
import time
import sys


class ImageHandler(py.ImageEventHandler):
    """
    Image event handler chạy trong pylon background thread
    Chỉ copy frame – KHÔNG xử lý GUI ở đây
    """
    def __init__(self):
        super().__init__()
        self.latest_img = None
        self.lock = threading.Lock()
        self.frame_count = 0

    def OnImageGrabbed(self, camera, grabResult):
        try:
            if grabResult.GrabSucceeded():
                img = grabResult.Array.copy()   # BẮT BUỘC copy
                with self.lock:
                    self.latest_img = img
                    self.frame_count += 1
        except Exception as e:
            print("Grab error:", e)


def main():
    # -----------------------------
    # Create & open camera
    # -----------------------------
    tlf = py.TlFactory.GetInstance()
    devices = tlf.EnumerateDevices()

    if len(devices) == 0:
        print("No Basler camera found")
        sys.exit(1)

    for d in devices:
        print(f"Found camera: {d.GetModelName()}  SN: {d.GetSerialNumber()}")

    cam = py.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()

    # -----------------------------
    # Camera configuration
    # -----------------------------
    cam.PixelFormat.SetValue("BayerGB8")

    # Continuous mode
    cam.TriggerMode.SetValue("Off")

    # Exposure (manual)
    cam.ExposureAuto.SetValue("Off")
    cam.ExposureTimeAbs.SetValue(5000.0)  # us

    # Gain auto
    cam.GainAuto.SetValue("Continuous")

    print("Camera opened and configured")

    # -----------------------------
    # Register background handler
    # -----------------------------
    handler = ImageHandler()
    cam.RegisterImageEventHandler(
        handler,
        py.RegistrationMode_ReplaceAll,
        py.Cleanup_None
    )

    # -----------------------------
    # Start background grabbing
    # -----------------------------
    cam.StartGrabbing(
        py.GrabStrategy_LatestImageOnly,
        py.GrabLoop_ProvidedByInstantCamera
    )

    print("Grabbing started (press 'q' to quit)")

    last_count = 0
    last_time = time.time()

    # -----------------------------
    # Main loop (OpenCV GUI)
    # -----------------------------
    while cam.IsGrabbing():
        with handler.lock:
            img = handler.latest_img

        if img is not None:
            # Bayer → RGB
            rgb = cv2.cvtColor(img, cv2.COLOR_BAYER_GB2RGB)

            # FPS calculation
            now = time.time()
            if now - last_time >= 1.0:
                fps = handler.frame_count - last_count
                last_count = handler.frame_count
                last_time = now
                cv2.putText(
                    rgb,
                    f"FPS: {fps}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Basler Background Grab", rgb)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # -----------------------------
    # Cleanup
    # -----------------------------
    cam.StopGrabbing()
    cam.DeregisterImageEventHandler(handler)
    cam.Close()
    cv2.destroyAllWindows()
    print("Camera closed")


if __name__ == "__main__":
    main()
