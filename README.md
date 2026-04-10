# Trackify: Smart Attendance and Engagement System
> "Stay On Track, Stay Engaged!"

## Overview
Trackify is a smart attendance system that automates attendance tracking and optimizes classroom engagement using IoT hardware and AI-powered tools.
It addresses the limitations of traditional attendance methods by combining RFID authentication, facial recognition, and ultrasonic sensors to deliver accurate logging, energy-efficient resource management, and real-time analytics for students, professors, and administrators.

## Table of Contents
1. [Key Features](#key-features)
2. [System Components](#system-components)
3. [System Architecture](#system-architecture)
4. [Future Enhancements](#future-enhancements)
5. [Contributors](#contributors)
6. [License](#license)

## Key Features
- **Ultrasonic Proximity Detection** — Activates the system when someone is within ~50 cm
- **RFID Authentication** — Fast and secure check-in for students and professors
- **Facial Recognition** — Secondary authentication via OpenCV-based face detection
- **Classroom Resource Management** — Automates lights and power through a dual-relay card
- **Real-Time Notifications** — Sends reminders and attendance summaries via WhatsApp API
- **Data Storage & Visualization** — Logs attendance in SQLite with intuitive dashboards
- **Role-Based Dashboards** — Custom views for administrators, professors, and students

## System Components

### 🛠️ Hardware
> The physical backbone of Trackify

- 🖥️ **Raspberry Pi 4** — Main processing unit that orchestrates all components
- 📡 **Ultrasonic Sensor (HC-SR04)** — Detects presence within ~50 cm to wake the system
- 🔖 **RFID Reader (MFRC522)** — Scans student and professor ID cards
- 📷 **Hikvision 1080p Camera** — Captures images for facial recognition
- ⚡ **Dual-Relay Card** — Controls classroom lights and electrical devices

### 💻 Software
> The intelligence behind the system

- 🐍 **Python** — Core programming language powering all logic
- 👁️ **OpenCV** — Real-time facial detection and recognition
- 🗄️ **SQLite** — Database storing all attendance records
- 💬 **WhatsApp API** — Delivers instant notifications and reminders
- 🔌 **RPi.GPIO** — Manages GPIO pins and hardware communication

## System Architecture
```
+------------------+     +-------------------+     +----------------------+
|  Ultrasonic      |     |   RFID Reader     |     |   Camera Module      |
|  Sensor          |     |   (MFRC522)       |     |   (Hikvision 1080p)  |
+------------------+     +-------------------+     +----------------------+
         |                        |                          |
         +------------------------+--------------------------+
                                  |
                    +-------------+-------------+
                    |     Raspberry Pi 4        |
                    |  - Facial Recognition     |
                    |  - Data Processing        |
                    |  - Attendance Logs        |
                    |  - Notifications          |
                    +---------------------------+
                                  |
                    +---------------------------+
                    |  Dashboards & Analytics   |
                    |  - Admin UI               |
                    |  - User Management        |
                    |  - Attendance Reports     |
                    +---------------------------+
```

## Future Enhancements
- **Mobile App** — Access attendance records via mobile apps
- **Cloud Integration** — Migrate to a cloud-based database for scalability
- **Emotion Detection** — Analyze student engagement via facial expressions
- **Energy Optimization** — Smarter IoT controls for resource management

## Contributors
| 🎓 | Younes Farah |
| 🎓 | Ahmed Rekik |
| 🎓 | Wael Baccouche |
| 🎓 | Nabil Chelly |
| 🎓 | Skander Amira |

## License
This project is licensed under the [MIT License](LICENSE).

