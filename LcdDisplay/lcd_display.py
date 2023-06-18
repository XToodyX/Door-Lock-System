from time import sleep_ms
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd

# Display-Zeilen ausgeben
def print_on_display(text):
    lcd.putstr(text)

# Display-Inhalt löschen
def clear_display():
    lcd.clear()

# Initialisierung I2C auf GPIO Pins 20 & 21
i2c = I2C(0, sda=Pin(20), scl=Pin(13), freq=100000)
    
# Initialisierung LCD über I2C
lcd = I2cLcd(i2c, 0x27, 2, 16)