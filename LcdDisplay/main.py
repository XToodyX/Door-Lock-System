import network
import utime
import lcd_display as display
from machine import Pin
from umqtt.simple import MQTTClient
    
def connect_to_network(name, ssid):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(name, ssid)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return sta_if.ifconfig()[0]
    
def check_keys(method):
    done = False
    for row in range(4):
        for col in range(4): 
            row_pins[row].high()
            
            if col_pins[col].value() == 1:
                key_press = matrix_keys[row][col]
                if key_press == "#":
                    if len(guess) > 0:
                        utime.sleep(0.3)
                        guess.pop()
                        display.lcd.move_to(len(guess) + 1, 1)
                        display.lcd.putstr(" ")
                else:
                    utime.sleep(0.3)
                    guess.append(key_press)
                    display.lcd.move_to(len(guess), 1)
                    display.lcd.putstr("*")
                
            if len(guess) == 6:
                done = check_secret_pin(guess, method)
                
                for x in range(0,6):
                    guess.pop()
                    
        row_pins[row].low()
        
    mqtt_client.check_msg()
    return done
    

def check_secret_pin(guess, method):
    global doorStatus
    
    if guess == secret_pin:
        if method == "CLOSE":
            mqtt_client.publish(mqtt_publish_topic, "close")
            display.clear_display()
            display.print_on_display("Door now closed, Sir!")
            doorStatus = 'CLOSED'
        else:
            mqtt_client.publish(mqtt_publish_topic, "open")
            display.clear_display()
            display.print_on_display("Welcome Sir!")
            doorStatus = 'OPEN'
        
        utime.sleep(3)
        return True    
    else:
        display.lcd.move_to(1, 1)
        display.lcd.putstr("      ")
        return False

def mqtt_subscription_callback(topic, message):
    global doorStatus
    global statusChanged
    
    if message == b'open':
        doorStatus = 'OPEN'
        statusChanged = True
    elif message == b'close':
        doorStatus = 'CLOSED'
        statusChanged = True

###########################################################

### START ###
        
try:
    global doorStatus
    doorStatus = "OPEN"
    
    global statusChanged
    statusChanged = False

    # Defines if it should open or close
    method = ""
    
    # Create a map with your keyboard values
    matrix_keys = [['1', '2', '3', 'A'],
                   ['4', '5', '6', 'B'],
                   ['7', '8', '9', 'C'],
                   ['*', '0', '#', 'D']]

    # Define PINs according to cabling
    keypad_rows = [11,10,9,8]
    keypad_columns = [7,6,4,2]

    col_pins = []
    row_pins = []

    # The keys entered by the user
    guess = []

    secret_pin = list('1','2','3','4','5','6')

    for x in range(0,4):
        row_pins.append(Pin(keypad_rows[x], Pin.OUT))
        row_pins[x].value(1)
        col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
        col_pins[x].value(0)


    mqtt_host = "<your_broker_host_ip_or_domain>"
    mqtt_username = "<your_broker_username>"
    mqtt_password = "<your_mqtt_password>"
    mqtt_publish_topic = "<your_publish_topic>" 
    mqtt_receive_topic = "<your_receive_topic>"

    mqtt_client_id = "<your_unique_client_id>" # Can be a random number

    network_name = "<your_network_name>"
    network_password = "<your_network_ssid>"

    connect_to_network(network_name, network_password)
    
    # Initialize MQTTClient
    mqtt_client = MQTTClient(
            client_id = mqtt_client_id,
            server = mqtt_host,
            user = mqtt_username,
            password = mqtt_password)
    
    mqtt_client.set_callback(mqtt_subscription_callback)
    mqtt_client.connect()
    
    mqtt_client.subscribe(mqtt_receive_topic)
        
    while True:
        guess = []
        display.clear_display()
        
        if doorStatus == 'CLOSED':
            display.print_on_display("Enter Pin: ")
            method = "OPEN"
        else:
            display.print_on_display("Lock Door: ")
            method = "CLOSE"
            
        while not check_keys(method) and not statusChanged:
            pass
        
        statusChanged = False
    
except KeyboardInterrupt:
    mqtt_client.disconnect()