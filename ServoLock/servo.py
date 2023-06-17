from machine import Pin, PWM

servo = PWM(Pin(1)) # Change number to your connected GPIO Pin

servo.freq(50)


# Customize with own rotation
def open_door():
    servo.duty_u16(3000)
    
def close_door():
    servo.duty_u16(6550)
