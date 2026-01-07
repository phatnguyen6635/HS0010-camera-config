# -- coding: utf-8 --

import sys
import cv2
import numpy as np
from ctypes import *
import os

# Load Hikrobot SDK
sys.path.append("./MvImport")
from MvCameraControl_class import *


def main():
    # 1. Init SDK
    MvCamera.MV_CC_Initialize()

    # 2. Enum camera
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayer = MV_GIGE_DEVICE | MV_USB_DEVICE

    ret = MvCamera.MV_CC_EnumDevices(tlayer, deviceList)
    if ret != 0:
        print ("enum devices fail! ret[0x%x]" % ret)
        sys.exit()

    print(f"Found {deviceList.nDeviceNum} cameras")

    for i in range(deviceList.nDeviceNum):
        dev = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if dev.nTLayerType == MV_GIGE_DEVICE:
            gige_info = dev.SpecialInfo.stGigEInfo

                # The IP address is stored as a 32-bit integer (Big Endian)
            ip_addr = (gige_info.nCurrentIp & 0xff000000) >> 24
            ip_addr_2 = (gige_info.nCurrentIp & 0x00ff0000) >> 16
            ip_addr_3 = (gige_info.nCurrentIp & 0x0000ff00) >> 8
            ip_addr_4 = (gige_info.nCurrentIp & 0x000000ff)
        
            print(f"Camera [{i}] IP: {ip_addr}.{ip_addr_2}.{ip_addr_3}.{ip_addr_4}")


    nConnectionNum = int(input("Select the index camera: "))


    # 3. Create handle
    cam = MvCamera()
    stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
    ret = cam.MV_CC_CreateHandle(stDeviceList)

    if ret != 0:
        print ("create handle fail! ret[0x%x]" % ret)
        sys.exit()

    # 4. Open camera
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print ("open device fail! ret[0x%x]" % ret)
        sys.exit()

    print("Camera opened")

    # 5. GigE packet size
    if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
        size = cam.MV_CC_GetOptimalPacketSize()
        if size > 0:
            cam.MV_CC_SetIntValue("GevSCPSPacketSize", size)

    # 6. Trigger OFF
    cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)

    # 7. Start grabbing
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print ("start grabbing fail! ret[0x%x]" % ret)
        sys.exit()

    # 8. Buffer frame
    frame = MV_FRAME_OUT()
    memset(byref(frame), 0, sizeof(frame))

    while True:
        ret = cam.MV_CC_GetImageBuffer(frame, 1000)
        if ret == 0 and frame.pBufAddr:
            w = frame.stFrameInfo.nWidth
            h = frame.stFrameInfo.nHeight
            pixel_type = frame.stFrameInfo.enPixelType

            if pixel_type == PixelType_Gvsp_Mono8:
                img = np.frombuffer(
                    string_at(frame.pBufAddr, w * h),
                    dtype=np.uint8
                ).reshape((h, w))

                cv2.imshow("Hikrobot Camera", img)

            cam.MV_CC_FreeImageBuffer(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 9. Cleanup
    cam.MV_CC_StopGrabbing()
    cam.MV_CC_CloseDevice()
    cam.MV_CC_DestroyHandle()
    MvCamera.MV_CC_Finalize()
    cv2.destroyAllWindows()
    print("Camera closed")


if __name__ == "__main__":
    main()
