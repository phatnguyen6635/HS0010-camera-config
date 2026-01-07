# <div align="center">HS0010 CAMERA CONFIGURATION</div>

## Table of Contents

- [About](#about)
- [Structure](#structure)
- [Folder Description](#folder-description)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Notes](#notes)

---

## About

This repository provides a unified structure for **configuring, managing, and testing industrial cameras from multiple vendors**.

Supported camera brands include:

- **Basler**
- **Hikrobot (HIK)**
- **Allied Vision Mako**
- **CVB (Common Vision Blox)** – used as a reference library that can work across multiple camera vendors

The repository focuses on:

- Listing and detecting connected cameras
- Opening and initializing cameras
- Loading and saving camera configuration parameters
- Providing vendor-specific SDK usage examples

This project is intended to serve as:

- A **camera configuration toolkit** for machine vision systems
- A **reference implementation** for integrating multiple camera SDKs
- A **base repository** for future vision pipelines such as inspection, tracking, or measurement systems

---

## Structure

```text
.
├── basler
│   ├── list_cameras.py
│   ├── load_save_settings.py
│   ├── open_camera.py
│   └── settings
│
├── cvb
│   ├── list_cameras.py
│   ├── open_camera.py
│   └── settings
│
├── hik
│   ├── list_cameras.py
│   ├── load_save_settings.py
│   ├── open_camera.py
│   ├── MvImport
│   │   ├── CameraParams_const.py
│   │   ├── CameraParams_header.py
│   │   ├── MvCameraControl_class.py
│   │   ├── MvErrorDefine_const.py
│   │   ├── MvISPErrorDefine_const.py
│   │   └── PixelType_header.py
│   └── settings
│
├── mako
│   ├── asynchronous_grab_opencv.py
│   ├── list_cameras.py
│   ├── list_chunk_data.py
│   ├── load_save_settings.py
│   ├── multithreading_opencv.py
│   └── settings
│
├── main.py
├── README.md
├── requirements.txt
└── pyproject.toml
```

---

## Folder Description

### Vendor-Specific Directories

Each camera vendor is isolated in its own directory with dedicated examples and configuration files.

- **basler/**
  - Scripts for listing cameras, opening cameras, and loading/saving parameters using the Basler Pylon SDK.

- **hik/**
  - Hikrobot camera control examples using the official MVS SDK.
  - Includes the `MvImport` module containing Python bindings and constants required by the SDK.

- **mako/**
  - Allied Vision Mako camera examples.
  - Includes asynchronous and multithreaded image acquisition with OpenCV.

- **cvb/**
  - Common Vision Blox (CVB) examples.
  - Used as a cross-vendor reference library for camera handling.

---

## Getting Started

### Installation

1. Clone the repository

```bash
git clone git@github.com:<your-username>/HS0010-camera-config.git
cd HS0010-camera-config
```

2. Create and activate a virtual environment using UV (recommmended)

Using **conda**:

```bash
uv  init --python 3.10
uv venv .venv
source .venv/bin/activate
```

3. Install Python dependencies

```bash
uv pip install -r requirements.txt
```

## Usage

This repository **does not use a single unified entry script**.  
The workflow is **vendor-based**.

**Select the camera brand you are using**, navigate to the corresponding folder, and run the provided scripts to test camera connection and configuration.

### General Workflow

1. Identify your camera vendor (Basler, Hikrobot, Mako, or CVB)
2. Navigate to the vendor-specific directory
3. Run the example scripts to:
   - List connected cameras
   - Open and stream from the camera
   - Load or save camera parameters (if supported)

Each script is standalone and focuses on a specific task.
### Examples

#### Basler Camera

```bash
cd basler
python list_cameras.py        # List all connected Basler cameras
python open_camera.py         # Open camera and start grabbing
python load_save_settings.py  # Load or save camera parameters
```

---

## Notes

- This repository focuses on **camera configuration and connectivity**, not full image processing or AI pipelines.
- Designed for **industrial machine vision environments**.
- Easily extendable for image processing, AI inference, and automated inspection systems.
