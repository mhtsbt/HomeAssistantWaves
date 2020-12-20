import requests
import time
import paho.mqtt.client as mqtt

DEVICE_IP = "http://10.0.3.35/v1/constellation"

connected = False

while not connected:
    try:
        client = mqtt.Client(client_id="hawaves")
        client.connect("10.0.3.2", 1883)
        client.loop_start()
        connected = True
    except:
        print("Failed to connect to MQTT server")
        time.sleep(30)

def send_message(topic, content):
    client.publish(topic, content, 2)
    print(topic, content)


def register_sensor(uuid, name):
    topic = f"homeassistant/fan/{uuid}/config"
    #  \"stat_t\": \"~/state\",
    content = "{\"~\": \"homeassistant/"+uuid+"\",\"name\": \""+name+"\", \"cmd_t\": \"~/set\", \"speed_state_topic\":\"~/speed\" \"unique_id\": \""+uuid+"\"}"

    send_message(topic, content)


register_sensor(uuid="bathroomfan", name="Bathroom fan")


def check_status():
    r = requests.get(DEVICE_IP)
    data = r.json()

    fan_rpm = data['actuator']['0']['parameter']['rpm']['value']

    send_message(f"homeassistant/bathroomfan/speed", fan_rpm)


while True:

    try:
        check_status()
    except:
        print("error")

    time.sleep(60)
