import pypylon.pylon as  py
import matplotlib.pyplot as plt
import numpy as np
import cv2

tlf = py.TlFactory.GetInstance()

print(f"tlf: {tlf}")

devices = tlf.EnumerateDevices()

print(f"Device: {devices}")

for d in devices:
    print(f"Model name: {d.GetModelName()}; Serial number: {d.GetSerialNumber()}")
