# 🌀 LazyCrank

**LazyCrank** is a fun project to automate an old awning that uses a manual iron crank. Instead of turning it by hand, an **ESP32** with **MicroPython** controls a **12V DC gear motor** to crank it automatically via a web interface. 

---

## 🛠️ Features

- Web interface with buttons: **UP**, **DOWN**, and **STOP**
- 12V 100 RPM gear motor with enough torque to operate the crank
- Controlled by an **ESP32** running **MicroPython**
- No external servers or Home Assistant required
- Great educational project for teaching robotics to children

---

## 🔩 Hardware Used

| Component          | Description                                        |
|--------------------|----------------------------------------------------|
| ESP32              | Microcontroller with Wi-Fi                         |
| DC Motor           | 12V, 100 RPM, high torque with gearbox             |
| L298N Motor Driver | For controlling motor direction and power          |
| 12V Power Supply   | To power the motor                                 |
| Wires & Breadboard | To connect all components                          |
| Mechanical Coupler | To connect motor shaft to the manual crank         |

> ⚠️ Speed is not an issue, but **torque** is. A slow, powerful motor works best for moving the iron crank handle.

---

## 🔌 Wiring Overview

```
[ESP32] → GPIOs → [L298N] → [DC Motor]
                  ↑         ↑
              12V IN    Motor Outputs
```

- Connect IN1, IN2 on L298N to ESP32 GPIO pins
- Power the L298N with a separate 12V power supply
- Share GND between the ESP32 and the motor power supply

---

## 🌐 Web Interface

The ESP32 hosts a local web page with three control buttons:

- 🔼 **UP** — Rotates motor to retract the awning
- 🔽 **DOWN** — Rotates motor to extend the awning
- ⏹️ **STOP** — Stops the motor immediately

Accessible from any device on the same Wi-Fi network.

---

## 💾 Software

- Written in **MicroPython**
- Uses `socket` for a basic web server
- Direct GPIO control for L298N motor driver
- Simple and clean structure, ideal for learning

---

## 📂 Project Structure

```
lazycrank/
├── main.py        # MicroPython control script
├── boot.py        # Wi-Fi setup
└── README.md      # This file
```

---

## Installation instructions

- Copy the three files inside ESP32
```
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put index.html
```
- Reboot ESP32
- Connect to the IP that appears in your home router with the name "mpy-esp32c3"

## 🧪 Current Status

✅ The prototype is **working perfectly**  
😄 Fun to use and ideal for demonstration or learning

---

## 🚀 Future Improvements

- Add **limit switches** to detect fully opened/closed positions
- Integrate with **ESPHome** or MQTT
- Voice control via Home Assistant and Alexa
- Track runtime to estimate awning position
- Add OTA firmware updates

---

## 🎓 Educational Value

LazyCrank is a great way to learn and teach:

- Basic home automation
- Controlling DC motors
- Web interfaces with MicroPython
- Real-world electronics applications

---

## 🙌 Credits

If someone finds this useful — awesome!  
If you improve it, I'd love to see your version 😄

---
