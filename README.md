# Bluetooth LED Strip control (with Google Assistant)

This is a project that uses a **Raspberry Pi (RPI)** to control a Bluetooth LED strip via **Google Assistant**.
The script uses **Python** to control the LED strip with the RPI and to create an API to access the script's methods.
Also **IFTT** is used to create the Google Assistant <-> API requests.

## Contents

- [Acknowledgements and resources](#acknowledgements-and-resources)
- [Disclaimer](#disclaimer)
- [1. Intro and Setup](#intro-and-Setup)
  - [Requirements](#requirements)
    - [LED strip reverse engineering](#led-strip-reverse-engineering)

## Acknowledgements and resources

This Python script is based on the tutorials of:
  - **Led strip with Bluetooth Control**
    - [Reddit](https://www.reddit.com/r/homeassistant/comments/gnjqlp/reverse_engineering_bluetooth_led_strip_light/): Reverse engineering of a Bluetooth LED strip - I 
    - Reverse engineering of a Bluetooth LED strip - II [Blog](http://nilhcem.com/iot/reverse-engineering-bluetooth-led-name-badge)
    - Reverse engineering of a Bluetooth LED strip - III [Medium](https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546)
  - **Server/API**
    - API creation - I [Medium](https://medium.com/@sidhantpanda/raspberry-pi-home-automation-with-google-assistant-integration-part-1-software-71b3b8904205)
    - API creation - II [Medium](https://medium.com/sysf/introduction-to-iot-with-raspberry-pi-and-node-js-using-rgb-led-lights-77f4750a5ea9)
    - API creation - III [Blog](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
  - **Google Assistant**
    - Google Assistant implementation - I [Intructables](https://www.instructables.com/Google-Home-Raspberry-Pi-Power-Strip/)
    - Google Assistant implementation - II [Programminghistorian](https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#installing-python-and-flask)

## **Disclaimer:**
**You can't brick your RPI or strips using this methods, but I don't take responsibility for any damage caused.**  
If you find any mistakes in this tutorial, _please_ submit a PR 👍🏻

## Intro and setup

### Requirements
#### LED strip reverse engineering
1. A computer with ADB drivers installed
2. A mobile phone with Android
3. An USB type C cable (or similar)

#### API Server
1. A RPI with Raspbian installed
2. An IDE (Atom or similar)

#### Google Assistant / IFTT
UNDER DEVELOPMENT
