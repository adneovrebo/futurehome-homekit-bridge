from utils.logger import bridge_logger
import signal
from pyhap.accessory_driver import AccessoryDriver
import futurehome.mqtt as mqtt
from devices.device_factory import get_bridge
import futurehome.mqtt as mqtt

PORT = 51826

bridge_logger.info("Starting MQTT client")
mqtt.client.loop_start()
while not mqtt.client.is_connected():
    pass
bridge_logger.info("MQTT client connected")


if __name__ == '__main__':
    bridge_logger.info(f"Starting bridge on port {PORT}")
    driver = AccessoryDriver(port=PORT)
    bridge, accessories = get_bridge(driver)
    driver.add_accessory(bridge)
    signal.signal(signal.SIGTERM, driver.signal_handler)
    driver.start()
