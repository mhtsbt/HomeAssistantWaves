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


def register_sensor(uuid, name, unit=None):
    topic = f"homeassistant/sensor/{uuid}/config"
    #  \"stat_t\": \"~/state\",
    if unit:
        content = "{\"~\": \"homeassistant/"+uuid+"\",\"name\": \""+name+"\", \"state_topic\":\"~/state\", \"unique_id\": \""+uuid+"\", \"unit_of_measurement\": \""+unit+"\"}"
    else:
        content = "{\"~\": \"homeassistant/" + uuid + "\",\"name\": \"" + name + "\", \"state_topic\":\"~/state\", \"unique_id\": \"" + uuid + "\"}"

    send_message(topic, content)


register_sensor(uuid="bathroomfanspeed", name="Bathroom fan speed", unit='rpm')
register_sensor(uuid="bathroomtemp", name="Bathroom temp", unit='°C')
register_sensor(uuid="bathroomhumidity", name="Bathroom humidity", unit='%')
register_sensor(uuid="bathroomco2", name="Bathroom co2", unit='ppm')
register_sensor(uuid="bathroompressure", name="Bathroom pressure", unit='Pa')
register_sensor(uuid="bathroomdecission", name="Bathroom decission")

def check_status():
    r = requests.get(DEVICE_IP)
    data = r.json()

    fan_rpm = data['actuator']['0']['parameter']['rpm']['value']
    send_message(f"homeassistant/bathroomfanspeed/state", fan_rpm)

    for key, sensor in data['sensor'].items():
        if sensor['name'] == "temp":
            state = sensor['parameter']['temperature']['value']
            send_message(f"homeassistant/bathroomtemp/state", state)
        elif sensor['name'] == "rh":
            state = sensor['parameter']['humidity']['value']
            send_message(f"homeassistant/bathroomhumidity/state", state)
        elif sensor['name'] == "co2":
            state = sensor['parameter']['concentration']['value']
            send_message(f"homeassistant/bathroomco2/state", state)
        elif sensor['name'] == "press":
            state = sensor['parameter']['pressure']['value']
            send_message(f"homeassistant/bathroompressure/state", state)
        elif sensor['name'] == "decision":
            state = sensor['parameter']['trigger']['value']
            send_message(f"homeassistant/bathroomdecission/state", state)


while True:

    #try:
    check_status()
    #except Exception as ex:
    #    print(f"error {ex}")

    time.sleep(60)
