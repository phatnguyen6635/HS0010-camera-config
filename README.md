# <div align="center">HS0010 CAMERA CONFIGURATION</div>

## Table of Contents

- [About](#about)
- [Structure](#structure)
- [Folder Description](#folder-description)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
    - [`main.py`](#mainpy)
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

### Common Files

- **`main.py`**
  - Central entry point for testing camera connectivity and configuration.
- **`settings/`**
  - Vendor-specific camera configuration files.
- **`requirements.txt`**
  - Python dependencies required to run the project.
- **`pyproject.toml`**
  - Project metadata and build configuration.

---

## Getting Started

### Installation

1. Clone the repository

```bash
git clone git@github.com:<your-username>/HS0010-camera-config.git
cd HS0010-camera-config
```

2. Create and activate a virtual environment (recommended)

Using **conda**:

```bash
conda create -n camera-config python=3.9
conda activate camera-config
```

Or using **venv**:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note:**  
> Vendor SDKs such as **Basler Pylon**, **Hikrobot MVS**, **Allied Vision Vimba**, and **CVB** must be installed separately according to each manufacturer’s official documentation.

---

## Usage

### `main.py`

The `main.py` script acts as a **central entry point** where you can:

- Select the camera vendor
- Test camera detection and connection
- Load and apply camera parameters
- Validate SDK installation

Run:

```bash
python main.py
```

Vendor-specific scripts can also be executed directly, for example:

```bash
python basler/list_cameras.py
python hik/open_camera.py
python mako/asynchronous_grab_opencv.py
```

---

## Notes

- This repository focuses on **camera configuration and connectivity**, not full image processing or AI pipelines.
- Designed for **industrial machine vision environments**.
- Easily extendable for image processing, AI inference, and automated inspection systems.
