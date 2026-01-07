import sys
sys.path.append("./MvImport")
from MvCameraControl_class import *

deviceList = MV_CC_DEVICE_INFO_LIST()
tlayerType = (MV_GIGE_DEVICE | MV_USB_DEVICE | MV_GENTL_CAMERALINK_DEVICE | MV_GENTL_CXP_DEVICE | MV_GENTL_XOF_DEVICE)
# Enumerate devices
ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
print(f"Found {deviceList.nDeviceNum} device.")
if ret != 0:
    print ("enum devices fail! ret[0x%x]" % ret)
    sys.exit()

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

cam = MvCamera()
# Select a device, and create a handle
stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
ret = cam.MV_CC_CreateHandle(stDeviceList)
if ret != 0:
    print ("create handle fail! ret[0x%x]" % ret)
    sys.exit()

ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
if ret != 0:
    print ("open device fail! ret[0x%x]" % ret)
    sys.exit()

ret = cam.MV_CC_CloseDevice()
if ret != 0:
    print ("close deivce fail! ret[0x%x]" % ret)
    sys.exit()

ret = cam.MV_CC_DestroyHandle()
if ret != 0:
    print ("destroy handle fail! ret[0x%x]" % ret)
    sys.exit()

interfaceList = MV_INTERFACE_INFO_LIST()
transportLayerType = MV_GIGE_INTERFACE | MV_CAMERALINK_INTERFACE | MV_CXP_INTERFACE | MV_XOF_INTERFACE | MV_LC_INTERFACE
# Enumerate frame grabbers
ret = MvCamera.MV_CC_EnumInterfaces(transportLayerType, interfaceList)
if ret != 0:
    print("enum interfaces fail! ret[0x%x]" % ret)
    sys.exit()