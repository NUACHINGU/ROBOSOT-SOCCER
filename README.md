# ROBOSOT - PSIS Roboteam (CREATE BY ANWAR)  
**Navigation & Mission Control System + ESP32 Robot Control Firmware**

---

## 🧭 Overview
This project consists of two integrated components developed by **PSIS Roboteam** for the RoboCup Small Size League (SSL):

1. **Navigation & Mission Control System**: A Python-based GUI application for real-time vision, mission logic, and robot communication.
2. **ESP32 Robot Control Firmware**: Low-level firmware running on an ESP32 microcontroller for motor control, IMU tracking, and command handling.

Together, these systems allow full control of a four-motor robot using real-time video and feedback from onboard sensors.

---

## 🖥️ Navigation & Mission Control System

### ✅ Features

#### 🖼 GUI Interface
- Built with **Tkinter** for intuitive user interaction
- Real-time video feed with object detection overlays
- HSV color calibration tools for vision tuning
- COM port auto-detection for ESP32 connection

#### 🧠 Mission Modes
- **Avoidance**: Navigate around obstacles to reach the ball  
- **Goal First**: Reach the goal before interacting with the ball  
- **Keeper Mode**: Stay near the goal to block incoming shots  
- Individual PID tuning panels for each mode

#### 👁️ Vision Processing
- Object detection using **OpenCV**
- HSV-based color segmentation
- Distance estimation based on object size and camera calibration

#### 🔌 Robot Communication
- Serial communication with the ESP32
- Command types: movement, grabbing, kicking, rotation, relay
- Real-time feedback from robot (e.g., yaw angle)

#### 💾 Configuration Management
- Persistent settings via `.ini` files
- Save/load configurations for color and mission logic

---

## 🔧 ESP32 Robot Control Firmware

### ✅ Features

#### ⚙️ Motor Control
- Control of **four independent DC motors** via direction and PWM pins
- Additional Motor A & B with H-bridge support
- Supports:
  - Forward / Backward
  - Left / Right
  - Diagonal movement
  - In-place rotation
- Motor speed offsets for tuning balance and straight-line movement

#### 🧭 IMU Integration
- **MPU6050** used for yaw tracking (gyro-based)
- Startup calibration to correct drift
- Smoothed angle readings with filtering
- **Automatic yaw correction** during straight motion
- Targeted angle rotation

#### 📡 Bluetooth Serial Communication
- Bluetooth serial interface named `ESP32_Robot`
- Receives commands from external devices (e.g., GUI, mobile)
- Command types:
  - Movement
  - Rotation
  - Relay toggle
  - Speed adjustments
- Feedback messages and command acknowledgment

#### ⚡ Relay Control
- Relay connected to GPIO 23
- Supports ON, OFF, TOGGLE modes
- Optional auto-off pulse behavior

#### 📜 Command Protocol
- Lightweight single-character commands via serial
- Optional checksum verification
- Responsive and efficient communication

---

## 🔩 Hardware Requirements

### For ESP32 Firmware:
- **ESP32 Development Board**
- **MPU6050** IMU (I2C: SDA, SCL)
- **Four DC motors** with motor driver (PWM + DIR pins)
- **Relay module** (connected to GPIO 23)
- Bluetooth-capable control device (PC, mobile, or Raspberry Pi)

---

## ⚙️ Software Setup & Usage

### 📁 Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
