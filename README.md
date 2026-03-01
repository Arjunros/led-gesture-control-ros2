# LED Gesture Control - ROS2

Control an LED connected to Arduino by showing 5 fingers to a webcam.

## System Architecture
Camera → finger_detector node → /finger_count topic → led_controller node → Serial → Arduino → LED

## Requirements
- ROS2 Humble
- Python: mediapipe, opencv-python, pyserial
- Arduino Uno/Nano + LED + 220Ω resistor

## Run
```bash
# Terminal 1
ros2 run led_gesture_control finger_detector

# Terminal 2
ros2 run led_gesture_control led_controller --ros-args -p serial_port:=/dev/ttyUSB0
```

## Wiring
Arduino Pin 13 → 220Ω resistor → LED (+) → GND
