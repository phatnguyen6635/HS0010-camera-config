import cvb
import os

discovered_devices_list = cvb.DeviceFactory.discover_from_root(cvb.DiscoverFlags.IgnoreVins)
devices_list = []
for i in range(0, len(discovered_devices_list)):
    if discovered_devices_list[i].read_property(
            cvb.DiscoveryProperties.InterfaceDriverType) == "SOCKET":
        
        devices_list.append(discovered_devices_list[i])

print(f"Found {len(devices_list)} devices! ")

print("Serial number: ")
for index, device in enumerate(devices_list):
    print(device[cvb.DiscoveryProperties.DeviceSerialNumber])
print("-"*40)

for idx, info in enumerate(devices_list):
    print(f"Opening camera {idx}")

    with cvb.DeviceFactory.open(info.access_token, cvb.AcquisitionStack.GenTL) as device:
        
        node_map = device.node_maps[cvb.NodeMapID.Device]
        
        exposure_node = node_map["Std::ExposureTimeAbs"]

        print("ExposureTime value:", exposure_node.value)
