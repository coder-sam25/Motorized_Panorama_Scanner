# 180° Automated Panorama Scanner

## Overview

This project creates a **clean 180-degree panoramic image** automatically using a **servo-driven camera rotation system** and **OpenCV image stitching**.

The system combines:

* **Hardware control (Arduino + Servo)** to rotate the camera at fixed angles
* **Computer vision (Python + OpenCV)** to capture images and stitch them into a single panorama

The servo rotates the camera in steps while the Python program captures frames from the webcam and stitches them together into a **clean panoramic image with automatic cropping**.


# System Architecture

The project has **two main components**:

1. **Arduino Servo Controller**
   Controls the camera rotation.

2. **Python Panorama Stitcher**
   Captures frames and stitches them using OpenCV.

Arduino → rotates camera → Webcam captures frames
               ↓
          Python OpenCV
               ↓
       Panorama Stitching
               ↓
        Clean Cropped Panorama


# Features

* Automated **180° scanning**
* **Ghost frame overlay** for better alignment
* **Timed frame capture**
* OpenCV **SCANS mode stitching** (optimized for rotational scans)
* Automatic **black border removal**
* Clean **cropped panorama output**
* Simple hardware setup



# Hardware Requirements

* Arduino board (Uno)
* Servo motor
* USB webcam
* Computer running Python
* Jumper wires


# Hardware Setup

| Component    | Connection |
| ------------ | ---------- |
| Servo Signal | Pin 13     |
| Servo VCC    | 5V         |
| Servo GND    | GND        |

Mount the **webcam on the servo** so the camera rotates horizontally.


# Arduino Servo Controller

The Arduino rotates the servo **from 0° to 160°** in **20° steps** and pauses at each position.


# Python Panorama Capture & Stitching

The Python script:

1. Captures frames from the webcam
2. Shows a **ghost overlay** to align images
3. Collects multiple frames
4. Uses OpenCV **Stitcher (SCANS mode)** to combine them
5. Automatically **removes black borders**

Key functionality includes:

### Frame Capture

* Captures **8 images**
* Time interval between captures
* Resizes frames for consistent processing

### Ghost Alignment

The previously captured frame is shown as a **semi-transparent overlay** to help align the next frame.

### Panorama Stitching

Uses:

```
cv2.Stitcher_SCANS
```

which works better for **linear camera motion**.

### Automatic Cropping

After stitching:

1. Convert image to grayscale
2. Detect non-black regions
3. Find the largest contour
4. Iteratively erode mask
5. Extract the largest clean rectangle

This removes the **black borders common in panoramas**.

---


# Possible Improvements

* Serial communication between **Arduino and Python**
* Automatic **trigger-based capture**
* Real-time **panorama preview**
* Integration with **Raspberry Pi**
* Higher resolution stitching

---

# Applications

* Indoor environment scanning
* Robotics vision systems
* Security monitoring
* 3D mapping pre-processing
* DIY panoramic photography


# License

This project is open-source and free to use for educational and research purposes.

--

Panoramic scanning system combining **Arduino hardware control** and **OpenCV computer vision**.
