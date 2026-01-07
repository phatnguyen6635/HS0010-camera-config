import cvb
import cv2
import os

# -------- Discover Camera --------

discovered = cvb.DeviceFactory.discover_from_root(
    cvb.DiscoverFlags.IgnoreVins
)

devices = []

for info in discovered:
    try:
        if info.read_property(cvb.DiscoveryProperties.InterfaceDriverType) == "SOCKET":
            serial = info[cvb.DiscoveryProperties.DeviceSerialNumber]
            devices.append((serial, info))
    except Exception:
        pass

print(f"Found {len(devices)} cameras (SOCKET)")

if not devices:
    print("No GigE camera found!")
    exit(0)

serial, info = devices[0]
print(f"Using camera serial: {serial}")

# -------- Open & Streaming --------

with cvb.DeviceFactory.open(info.access_token, cvb.AcquisitionStack.GenTL) as device:

    # Lấy node map "Device"
    node_map = device.node_maps["Device"]

    # -------- Turn OFF hardware trigger --------
    try:
        if "Std::TriggerMode" in node_map.nodes:
            node_map["Std::TriggerMode"].value = "Off"
            print("TriggerMode set to Off (Free-Run)")
        else:
            print("TriggerMode not supported, skip")
    except Exception as e:
        print("Failed to turn off trigger:", e)

    # -------- Start Acquisition --------
    try:
        if "Std::AcquisitionStart" in node_map.nodes:
            node_map["Std::AcquisitionStart"].execute()
            print("Acquisition started")
        else:
            print("AcquisitionStart not supported")
    except Exception as e:
        print("Warning starting acquisition:", e)

    # -------- Get Image Stream --------
    try:
        stream = device.stream(cvb.ImageStream, 0)
    except Exception as e:
        print("Failed to get ImageStream:", e)
        exit(1)

    # -------- Start Streaming --------
    try:
        stream.start()
        print("Streaming started. Press ESC to exit...")
    except Exception as e:
        print("Could not start stream:", e)
        exit(1)

    # -------- Show images --------
    while True:
        try:
            image, status, node_maps = stream.wait()
        except Exception as ex:
            print("Stream wait exception:", ex)
            break

        if status == cvb.WaitStatus.Ok:
            frame = cvb.as_array(image, copy=False)
            cv2.imshow(f"Camera {serial}", frame)
        elif status == cvb.WaitStatus.Timeout:
            print("Timeout - no frame yet...")

        if cv2.waitKey(1) == 27:  # ESC
            print("Exit by user")
            break

    # -------- Stop streaming & acquisition --------
    try:
        stream.stop()
    except Exception:
        pass

    try:
        if "Std::AcquisitionStop" in node_map.nodes:
            node_map["Std::AcquisitionStop"].execute()
    except Exception:
        pass

    cv2.destroyAllWindows()
