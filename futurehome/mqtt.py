import constants as c, json, futurehome.device_discovery as dd, paho.mqtt.client as mqtt
from utils.logger import bridge_logger
from devices.device_factory import accessories_list

def on_connect(client, userdata, flags, rc):
    bridge_logger.info(f"Connected to MQTT broker with result code {rc}")
    if rc != 0:
        bridge_logger.error("Failed to connect to MQTT broker")
        return
    dd.discover_devices(client)

def on_message(client, userdata, msg):
    if msg.topic.endswith("discover_devices"):
        dd.store_devices(msg.payload)
    else:
        bridge_logger.info(f"Received message on topic {msg.topic}")
        bridge_logger.debug(f"Message payload: {msg.payload}")
        device = None
        for accessory in accessories_list:
            if accessory.address in msg.topic:
                device = accessory
                break

        if device is None:
            bridge_logger.error(f"Received message for unknown device: {msg.topic}")
            return

        payload = json.loads(msg.payload)
        device.update_state(payload)

client = mqtt.Client()
client.username_pw_set(c.username, c.password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(c.futurehome_ip, 1884)
