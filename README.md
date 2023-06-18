# 🚪 Door Lock System 🔑

This repo provides you with the material to Setup your own door lock system with a Raspberry Pi Pico W (inside / outside) communicating via MQTT Protocol over Wi-Fi.

## Prerequisites:
- running MQTT broker (like Mosquitto, cloud hosted, ...)

In my case I have a Mosquitto Docker Container up running
on my Raspberry Pi 4B.

## Initial Setup

So, now we can move on ...

1. Download the lightweight python code editor [Thonny](https://thonny.org/) with integrated support for the Pi Pico W
</br></br>
2. Hold the BOOTSEL-Button pressed while connecting the Pi Pico to your computer
</br></br>
3. Open Thonny, click in the bottom right corner and select "Install Micropython". The Pi Pico should already been chosen as Target Volume. Choose variant "Pico W / Pico WH" and hit install.
</br></br>
4. To communicate over MQTT we need to install "micropython-umqtt.simple".<br> Go to Thonny Tools -> Manage Packages, search for umqtt.simple and install the first one. <br>This Package can then be found in the /lib directory on your Pico
</br></br>
5. I discovered that the initial keepalive value at **lib/umqtt/simply.py** with 0 doesn't work for me. I set it to the maximum of 65535 seconds, so the connection should hold on for a year and will be then renewed by the while loop.

Now you have finished the setup, well done 💪

## Guide to the inside servo lock

1. Copy the files of **ServoLock** to your Pi Pico
<br><br>
2. Replace the credentials in the code at **main.py** with your personal and change the Pin of the servo at **servo.py** if needed

To test it, you can publish a message with the specified topic to your Broker either with the payload "on / off"

## Guide to the outside door opening interface

To 🔓 the door you can now simply send a message over mqtt, but it's more funny to have a dedicated interface outside the door, where you have to enter the correct key to open the door.

1. Copy the files of **LcdDisplay** to your Pi Pico
<br><br>
2. Replace the credentials in the code at **main.py** with your personal and change the Pins at **lcd_display.py** to your connected

To test this out you can of course simply type the correct
pin you stored before. The other Pi Pico should get notified.

## Further ideas 💡

As an extension you can create a security mechanism.
When someone puts the interface off the wall, you can
check this connection and if necessary 💣 all the credentials you entered in your program

## Contribute

If you have any further ideas or better solutions, please contribute by creating a Pull Request.<br>
I would be very happy :-)
   

