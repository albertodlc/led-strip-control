# Bluetooth LED Strip control (with Google Assistant)

<p align="center">
    <img height="auto" width="auto" src="img/img0.jpg" />
</p>

This is a project that uses a **Raspberry Pi (RPI)** to control a Bluetooth LED strip via **Google Assistant**.
The script uses **Python** to control the LED strip with the RPI and to create an API to access the script's methods.
Also **IFTT** is used to create the Google Assistant <-> API requests.

## Contents

- [Acknowledgements And Resources](#acknowledgements-and-resources)
- [Disclaimer](#disclaimer)
- [1. Intro and Setup](#intro-and-Setup)
  - [LED Strip Reverse Engineering](#led-strip-reverse-engineering)
  - [API Server](#api-server)
  - [Google Assistant / IFTT](#google-assistant-iftt)
- [2. Sniffing Bluetooth packets and reverse engineering the commands](#sniffing-bluetooth-packets-and-reverse-engineering-the-commands)
- [3. Creating an API-REST service](creating-an-api-rest-service)

## Acknowledgements and resources

This Python script is based on the tutorials of:
  - **Led strip with Bluetooth Control**
    - [Reddit](https://www.reddit.com/r/homeassistant/comments/gnjqlp/reverse_engineering_bluetooth_led_strip_light/) : Reverse engineering of a Bluetooth LED strip - I
    - [Blog](http://nilhcem.com/iot/reverse-engineering-bluetooth-led-name-badge) : Reverse engineering of a Bluetooth LED strip - II
    - [Medium](https://medium.com/@urish/reverse-engineering-a-bluetooth-lightbulb-56580fcb7546) : Reverse engineering of a Bluetooth LED strip - III
  - **Server/API**
    - [Medium](https://medium.com/@sidhantpanda/raspberry-pi-home-automation-with-google-assistant-integration-part-1-software-71b3b8904205) : API creation - I
    - [Medium](https://medium.com/sysf/introduction-to-iot-with-raspberry-pi-and-node-js-using-rgb-led-lights-77f4750a5ea9) : API creation - II
    - [Blog](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) : API creation - III
  - **Google Assistant**
    - [Intructables](https://www.instructables.com/Google-Home-Raspberry-Pi-Power-Strip/) : Google Assistant implementation - I
    - [Programminghistorian](https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#installing-python-and-flask) : Google Assistant implementation - II

## **Disclaimer:**
**You can't brick your RPI or strips using this method, but I don't take responsibility for any damage caused.**  
If you find any mistakes in this tutorial, _please_ submit a PR 👍🏻

## Intro and setup

The basic set-up of the project is:

<p align="center">
    <img height="auto" width="auto" src="img/img1.jpg" />
</p>

### LED strip reverse engineering
1. A LED strip with a Bluetooth controller.
2. A computer with ADB drivers installed.
3. A mobile phone with Android (and the official App of the LED strip).
4. An USB type C cable (or similar).
5. General knowledges of Wireshark and packet sniffing

### API Server
1. A RPI with Raspbian installed.
2. An IDE (Atom or similar).
3. General knowledges of Python and API operation.

### Google Assistant / IFTT
1. A Google account and an IFTT account.

## Sniffing Bluetooth packets and reverse engineering the commands
### Requirements


## Creating an API-REST service
### Requirements

## Google Assistant integration with the API-REST
### Requirements
After defining the API-REST methods, we need to set the IFTT services. IFTT refers to:

```
If This Then That (commonly known as IFTTT, /ɪft/) is a web-based service that allows users to create chains of conditional statements triggered by changes that occur within other web services such as Gmail, Facebook, Telegram, Instagram, Pinterest or Google Assistant
```
