import json
from devices.lightbulb import LightBulb
from pyhap.accessory import Bridge
from utils.logger import bridge_logger

"""
    Generates accessories from devices.json
    - Returns a list of accessories
"""
def generate_accessories(driver):
    with open("./data/devices.json", "r") as infile:
        loaded_devices = json.load(infile)

    devices_list = []
    for device in loaded_devices:
        if device["functionality"] == "lighting":
            device_name = device["client"]["name"]
            new_device = LightBulb(driver,
                                device_name, 
                                config=device)
            devices_list.append(new_device)
        else:
            bridge_logger.warning(f"Unsupported functionality: {device['functionality']} for device {device['client']['name']}")
    return devices_list
    
accessories_list = []
        
"""
    Returns a bridge with all accessories
"""
def get_bridge(driver):
    bridge = Bridge(driver, 'FutureHome Bridge')
    accessories = generate_accessories(driver)
    for accessory in accessories:
        bridge.add_accessory(accessory)
    bridge_logger.info(f"Added {len(accessories)} accessories to bridge")
    accessories_list.extend(accessories)
    return bridge, accessories
