import network
from umqtt.simple import MQTTClient
import servo

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

def mqtt_subscription_callback(topic, message):
    if message == b'open':
        servo.open_door()
    elif message == b'close':
        servo.close_door()


mqtt_host = "<your_broker_host_ip_or_domain>"
mqtt_username = "<your_broker_username>"
mqtt_password = "<your_broker_password>"
mqtt_receive_topic = "<your_trigger_topic>" 

mqtt_client_id = "<your_unique_client_id>" # Can be a random number

network_name = "<your_network_name>"
network_password = "<your_network_ssid>"

try:
    while True:
        connect_to_network(network_name, network_password)
        
        # Initialize MQTTClient
        mqtt_client = MQTTClient(
                client_id = mqtt_client_id,
                server = mqtt_host,
                user = mqtt_username,
                password = mqtt_password)

        mqtt_client.set_callback(mqtt_subscription_callback)
        mqtt_client.connect()

        # Listen / Subscribe to specified topic
        mqtt_client.subscribe(mqtt_receive_topic)

        try:
            while True:
                mqtt_client.wait_msg()
        except Exception as e:
            print(f'Failed to wait for MQTT messages: {e}')
        finally:
            mqtt_client.disconnect()

except KeyboardInterrupt:
    pass