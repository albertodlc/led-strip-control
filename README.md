# Bluetooth LED Strip control (with Google Assistant)

<p align="center">
    <img height="auto" width="auto" src="img/img0.jpg" />
</p>

## Background

Searching the Internet lead me to a few cheap LED strips from China (thank you Aliexpress) for under 1€/meter. The strip include 30 LEDs, the Bluetooth controller and a 5v power supply (an USB connector).

<p align="center">
    <img height="auto" width="30%" src="img/img01.jpg" />
    <img height="auto" width="18%" src="img/img02.jpg" />
</p>

As you can expect there was no documentation about the product - just a link to download the Android App (Happy Lightning).

A few days later I find another deal (this time on Amazon). The package include 10 meters of strip (30 LEDs/meter), Bluetooth-RF controller, RF remote control and 12v power supply. It sounded very professional, but there was **not** documentation either about the product - just the same link to the Android App.

<p align="center">
    <img height="auto" width="30%" src="img/img04.jpg" />
    <img height="auto" width="45%" src="img/img03.jpg" />
</p>

So I decided to investigate how to control these strips using Google Assistant, a Raspberry Pi (RPI) and my programming skills.

Finally I have developed an API-REST (all using **Python**) to control the LED strip with the RPI. Also **IFTTT** is used to create the Google Assistant <-> API requests communication.

## Contents

- [Acknowledgements And Resources](#acknowledgements-and-resources)
- [Disclaimer](#disclaimer)
- [1. Intro and Setup](#intro-and-Setup)
  - [LED Strip Reverse Engineering](#led-strip-reverse-engineering)
  - [API Server](#api-server)
  - [Google Assistant / IFTTT](#google-assistant-ifttt)
- [2. Sniffing Bluetooth packets and reverse engineering the commands](#sniffing-bluetooth-packets-and-reverse-engineering-the-commands)
  - [Requirements](#requirements)
- [3. Creating an API-REST service](creating-an-api-rest-service)
  - [Requirements](#requirements)
- [4. Google Assistant integration with the API-REST](google-assistant-integration-with-the-api-rest)
  - [Requirements](#requirements)
  - [Static IP configuration (RPI specific)](static-ip-configuration-rpi-specific)
  - [DDNS configuration (DuckDNS)](ddns-configuration-duckdns)
  - [Port-Forwarding configuration (depends on the router model)](#port-forwarding-configuration-depends-on-the-router-model))
## Acknowledgements and resources

This Python script is based on the tutorials from:
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
**In theory, it is impossible to brick your RPI or strips using this method, but I don't take responsibility for any damage caused.**  
If you find any mistakes in this tutorial, _please_ submit a PR 👍🏻

## Intro and setup

The basic set-up of the project is:

<p align="center">
    <img height="auto" width="auto" src="img/img1.jpg" />
</p>

### LED strip reverse engineering
1. A LED strip with a Bluetooth controller.
2. A computer with ADB drivers installed.
3. A mobile phone with Android (with the LED strip app and the nRF Connect app).
4. An USB type C cable (or similar).
5. General knowledges of Wireshark and packet sniffing

### API Server
1. A RPI with Raspbian installed.
2. An IDE (Atom or similar).
3. General knowledges of Python and API operation.

### Google Assistant / IFTTT
1. A Google account and an IFTTT account.

## Sniffing Bluetooth packets and reverse engineering the commands
### Requirements
T

## Creating an API-REST service
### Requirements

## Google Assistant integration with the API-REST
### Requirements
After defining the **API-REST** methods, you need to configure a **Static IP** on your RPI, configure a **DDNS** service and configure **Port-forwarding** on your router's firewall.

In addition to that, you need to set the **IFTTT services**. IFTTT refers to:
> If This Then That (commonly known as IFTTT, /ɪft/) is a web-based service that allows users to create chains of conditional statements triggered by changes that occur within other web services such as Gmail, Facebook, Telegram, Instagram, Pinterest or Google Assistant.
> - Wikipedia

### Static IP configuration (RPI specific)
1. You need to edit the /etc/dhcpcd.conf file
```sh
sudo nano /etc/dhcpcd.conf
```
2. Inside the file uncomment and edit the following lines (you need to indicate an IP within the range of your network, the IP of your router and your favorite DNS provider's IP)
```sh
# Example static IP configuration:
interface eth0
static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1 8.8.8.8 fd51:42f8:caae:d92e::1
```
3. Finally save the file (CTRL+o) and reboot the System
```sh
sudo reboot
```

### DDNS configuration (DuckDNS)
1. Go to the [DuckDNS](https://www.duckdns.org/) website and sign up with your Google account (or other via).
2. The web will redirect you to the administration panel, you need to enter a name for your domain and press "add domain". The **domain** and you **public IP** will be added below.

<p align="center">
    <img height="auto" width="auto" src="img/img49.JPG" />  
</p>

3. Now go to [DuckDNS/install](https://www.duckdns.org/install.jsp) and select your **Operating System (OS)** and the domain you want to configure. In this case, we are going the use the RPI to run the DDNS (but as I mention before you can use OpenWRT or other OS).

<p align="center">
    <img height="auto" width="auto" src="img/img48.JPG" />  
</p>

4. After choosing a domain, a step by step guide will be deployed. In the case of the RPI:
>If your linux install is running a crontab, then you can use a cron job to keep updated. We can see this with
```sh
ps -ef | grep cr[o]n
```
>If this returns nothing - then go and read up how to install cron for your distribution of linux.
also confirm that you have curl installed, test this by attempting to run curl
```sh
curl
```
>If this returns a command not found like error - then find out how to install curl for your distribution.
otherwise lets get started and make a directory to put your files in, move into it and make our main script
```sh
mkdir duckdns
cd duckdns
sudo nano duck.sh
```
>Now copy this text and put it into the file. The example below is for the domain XXXX. If you want the configuration for a different domain, use the drop down box above. You can pass a comma separated (no spaces) list of domains, you can if you need to hard code an IP (best not to - leave it blank and we detect your remote ip).
```sh
echo url="https://www.duckdns.org/update?domains=XXXX&token=YOUR_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
```
>Now save the file (CTRL+o and CTRL+x). This script will make a https request and log the output in the file duck.log. Now make the duck.sh file executeable
```sh
sudo chmod 700 duck.sh
```
>Next we will be using the cron process to make the script get run every 5 minutes
```sh
crontab -e
```
>Copy this text and paste it at the bottom of the crontab
```sh
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```
>Now save the file (CTRL+o then CTRL+x)lets test the script
```sh
./duck.sh
```
>This should simply return to a prompt. We can also see if the last attempt was successful (OK or bad KO)
```sh
cat duck.log
```
>If it is KO check your Token and Domain are correct in the duck.sh script.
> - DuckDNS.org

### Port-Forwarding configuration (depends on the router model)
1. Go to the web browser and type the private IP of your router (i.e 192.168.0.1)
2. Inside the router administration panel you have to find your firewall/port-forwards setting
3. And create a rule allowing connection from the **WAN** to the **LAN** on the **external port 80 (http)** and destination the **RPI static IP** on the **server port** (generally 5000).

<p align="center">
    <img height="auto" width="auto" src="img/img47.JPG" />
</p>


### IFTTT Configuration
1. Go to [IFTTT](https://ifttt.com) website and create a new account.
2. Click **create** a new **Applet**.
3. In the "If this" rectangle click **add** and search for **Google Assistant**, select it.

<p align="center">
    <img height="auto" width="auto" src="img/img50.JPG" />
</p>

4. Choose "Say a simple phrase" as your trigger (you can choose other option depending of the project you are working on).
<p align="center">
    <img height="auto" width="auto" src="img/img51.JPG" />
</p>

5. Now choose the phrase and other variations. For example "Turn my lamp on". And the response of the assistant. After that click "Create Trigger" and proceed.

<p align="center">
    <img height="auto" width="auto" src="img/img52.JPG" />  
</p>

6. In the "Then that" rectangle click **add** and search for **Webhooks**, select it.
7. Now select "Make a web request" and set "Method" to POST, "Content Type" should be text/plain and "Body" can be left blank. Finally set the URL to
```
http://ipaddressgoeshere/methodyouwanttocall
```
8. Create your action and choose Finish.
