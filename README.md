# Smart-Toll-Gate-System
An IoT-enabled smart toll gate system using Raspberry Pi, RFID sensors, and a Flask-based web dashboard for real-time vehicle monitoring and toll collection.

## Team Members

- **Hassan Alhilo**
- **Muhammad Ismail Sadaqat**
- **Dwayne Fonseca**

## Project Overview

The Smart Toll Gate System enables real-time toll collection, vehicle speed monitoring, and balance verification using RFID technology. It integrates hardware sensors with a Raspberry Pi and sends data to a cloud dashboard via ThingSpeak, while also offering an API via Flask for real-time monitoring.

## Features

- **RFID-based identification**
- **Balance deduction and alert system**
- **Speed monitoring using ADC and IR sensors**
- **Automatic photo/video capture for violations**
- **Live data upload to ThingSpeak**
- **Flask-based API for real-time monitoring**
- **LCD display + buzzer alerts**
- **User keypad interface for balance inquiry/recharge**
- **DHT11 for temperature/humidity readings**

## Hardware Components

| Component       | Description                       |
|----------------|-----------------------------------|
| Raspberry Pi   | Central controller                |
| RFID Reader    | Vehicle ID input                  |
| IR Sensor      | Car detection                     |
| Ultrasonic Sensor (HC-SR04) | Distance sensing      |
| LCD1602        | Display messages                  |
| Buzzer         | Sound alerts                      |
| Push Button    | Manual control input              |
| DHT11          | Temperature and humidity sensor   |
| Potentiometer  | Simulated speed control           |
| Pi Camera      | Image/video capture               |

## System Architecture

### Hardware Block Diagram
![Hardware Block Diagram](https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/b481221d50a3c54539407ac0c028a07773ec220c/Hardware-and-Software-Diagrams/Hardware%20diagram%20of%20Smart%20Toll%20Gate.png)

### Software Flowchart
<div style="display: flex; justify-content: center; align-items: flex-start; gap: 50;">
  <img src="https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/b481221d50a3c54539407ac0c028a07773ec220c/Hardware-and-Software-Diagrams/Flowchart%20for%20first%20half%20of%20main%20program%20loop.png?raw=true" alt="Software Flowchart Part 1" height = "500">
  <img src="https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/b481221d50a3c54539407ac0c028a07773ec220c/Hardware-and-Software-Diagrams/Flowchart%20of%20second%20half%20of%20main%20program%20loop.png" alt="Software Flowchart Part 2" height = "500">
</div>

<table>
  <tr>
    <td align="center" style="padding: 15px;">
      <img src="[YOUR_IMAGE_1_URL.png?raw=true](https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/b481221d50a3c54539407ac0c028a07773ec220c/Hardware-and-Software-Diagrams/Flowchart%20for%20first%20half%20of%20main%20program%20loop.png?raw=true)" alt="Software Flowchart Part 1" height = "500">
      <br>
      *Software Flowchart Part 1*
    </td>
    <td align="center" style="padding: 15px;">
      <img src="[YOUR_IMAGE_2_URL.png?raw=true](https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/b481221d50a3c54539407ac0c028a07773ec220c/Hardware-and-Software-Diagrams/Flowchart%20of%20second%20half%20of%20main%20program%20loop.png)" alt="Software Flowchart Part 2" height = "500">
      <br>
      *Software Flowchart Part 2*
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 15px;">
      <img src="https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/95074aacdafcf5330fd207e8c60dd10276eaef57/Hardware-and-Software-Diagrams/Flowchart%20for%20first%20half%20of%20main%20program%20loop.png" alt="First interrupt when the button is pressed" height = "500">
      <br>
      *First interrupt when the button is pressed*
    </td>
    <td align="center" style="padding: 15px;">
      <img src="https://github.com/Ismail-Sadaqat/Smart-Toll-Gate-System/blob/95074aacdafcf5330fd207e8c60dd10276eaef57/Hardware-and-Software-Diagrams/Flowchart%20for%20first%20interrupt%20when%20the%20button%20is%20pressed.png" alt="Second interrupt when infrared detects motion" height = "500">
      <br>
      *Second interrupt when infrared detects motion*
    </td>
  </tr>
</table>

