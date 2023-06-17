# 🚪 Door Lock System 🔑

This repo provides you with the material to Setup your own door lock system with a Raspberry Pi Pico W communicating via MQTT Protocol over Wi-Fi.

## Prerequisites:
- running MQTT broker (like Mosquitto, cloud hosted, ...)

In my case I have a Mosquitto Docker Container up running
on my Raspberry Pi 4B.

## Guide

So, now we can move on ...

1. Download the lightweight python code editor [Thonny](https://thonny.org/) with integrated support for the Pi Pico W
</br></br>
2. Hold the BOOTSEL-Button pressed while connecting the Pi Pico to your computer
</br></br>
3. Open Thonny, click in the bottom right corner and select "Install Micropython". The Pi Pico should already been chosen as Target Volume. Choose variant "Pico W / Pico WH" and hit install.<br>(=> Now the initial setup is done)
</br></br>
4. To communicate over MQTT we need to install "micropython-umqtt.simple".<br> Go to Thonny Tools -> Manage Packages, search for umqtt.simple and install the first one. <br>This Package can then be found in the /lib directory on your Pico
</br></br>
5. I discovered that the initial keepalive value at /lib/umqtt/simply.py with 0 doesn't work for me. I set it to 1 year (in seconds), so the connection should hold on for a year and will be then renewed by the while loop.
</br></br>
6. Then you only have to replace the credentials in the code at main.py with your personal and change the Pin of the servo at servo.py if needed.

Now you have finished the setup, well done 💪

To test it, you can publish a message with the specified topic to your Broker either with the payload "on/off"

## Contribute

If you have any further ideas or better solutions, please contribute by creating a Pull Request.<br>
I would be very happy :-)
   

