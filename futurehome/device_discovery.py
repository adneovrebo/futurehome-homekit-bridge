import json, os, paho.mqtt.client as mqtt
from constants import app_name
from utils.logger import bridge_logger
from futurehome.fimp import FIMPMessage

devices_topic = "pt:j1/mt:cmd/rt:app/rn:vinculum/ad:1"

"""
    Discover devices connected to the Futurehome hub
"""
def discover_devices(client: mqtt.Client):
    bridge_logger.info("Discovering devices connected to Futurehome hub")
    response_topic = f"pt:j1/mt:rsp/rt:app/rn:{app_name}/ad:discover_devices"

    fimp = FIMPMessage(
        serv="vinculum",
        type="cmd.pd7.request",
        val_t="object",
        val={
            "cmd": "get",
            "component": None,
            "id": None,
            "param": {
                "components": [
                    "device"
                ]
            },
            "requestId": 7294000000007
        },
        resp_to=response_topic,
        topic=devices_topic
    )

    # fimp_message = {
    #   "ctime": "2019-09-04 17:36:31 +0200",
    #   "props": {},
    #   "resp_to": response_topic,
    #   "serv": "vinculum",
    #   "src": app_name,
    #   "tags": [],
    #   "type": "cmd.pd7.request",
    #   "uid": c.uid,
    #   "val": {
    #     "cmd": "get",
    #     "component": None,
    #     "id": None,
    #     "param": {
    #       "components": [
    #         "device"
    #       ]
    #     },
    #   "requestId": 7294000000007
    #   },
    #   "val_t": "object",
    #   "ver": "1"
    #   }

    client.subscribe(response_topic)
    client.publish(devices_topic, payload=fimp.to_json())

devices_filepath = "./data/devices.json"
def store_devices(payload):
    bridge_logger.info(f"Storing devices from Futurehome hub in {devices_filepath}")
    if not os.path.exists("./data"):
        os.makedirs("./data")

    with open(devices_filepath, "w") as outfile:
        devices = json.loads(payload)["val"]["param"]["device"]
        bridge_logger.info(f"Found {len(devices)} devices")
        json.dump(devices, outfile, indent=4)
        
      

    
    