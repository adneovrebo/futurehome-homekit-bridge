import futurehome.mqtt as mqtt
from pyhap.const import CATEGORY_LIGHTBULB
from pyhap.accessory import Accessory
from utils.logger import bridge_logger as logger
from futurehome.fimp import FIMPMessage

"""
Lightbulb accessory

Implemented characteristics:
    - Switches on/off
    - Dimmable
"""
class LightBulb(Accessory):
    category = CATEGORY_LIGHTBULB

    def __init__(self,*args, config,**kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = config["client"]["name"]
        logger.info(f"Initializing lightbulb {self.name}")

        is_dimmable = "out_lvl_switch" in config["services"]
        if is_dimmable:
            logger.info("\t Lightbulb is dimmable")
            address = config["services"]["out_lvl_switch"]["addr"]
        else:
            logger.info("\t Lightbulb is NOT dimmable")
            address = config["services"]["out_bin_switch"]["addr"]
        
        logger.debug(f"\t Lightbulb address: {address}")

        self.device_identifier = address.split(":")[-1]
        logger.info(f"\t Lightbulb identifier: {self.device_identifier}")

        self.address = address
        self.is_dimmable = is_dimmable

        functionality = []
        if is_dimmable:
            functionality.append("Brightness")

        serv_light = self.add_preload_service('Lightbulb', chars=functionality)
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.switch_bulb)
        
        if is_dimmable:
            self.char_level = serv_light.configure_char(
                'Brightness', setter_callback=self.set_level)

        mqtt.client.subscribe(f"pt:j1/mt:evt{address}")

        self.ask_for_report()

        
    def __setstate__(self, state):
        self.__dict__.update(state)

    def update_state(self, msg):
        logger.debug(f"Updating state for {self.name}")
        logger.debug(f"Message: {msg}")

        if msg["type"] == "evt.lvl.report":
            self.char_level.set_value(msg["val"])
        elif msg["type"] == "evt.binary.report":
            self.char_on.set_value(msg["val"])

    def switch_bulb(self, value):
        if value:
            logger.info(f"Setting {self.name} to on")
            self.switch_light(f"pt:j1/mt:cmd{self.address}", True, self.is_dimmable)
        else:
            logger.info(f"Setting {self.name} to off")
            self.switch_light(f"pt:j1/mt:cmd{self.address}", False, self.is_dimmable)

    """
        Set the dimmer level of the lightbulb
        value: int between 0 and 100
    """
    def set_level(self, value):
        if value < 0 or value > 100:
            raise ValueError("Value must be between 0 and 100")

        logger.info(f"Setting {self.name} to level {value}")
        light_dimmer_topic = f"pt:j1/mt:cmd{self.address}"
        self.dim_light(light_dimmer_topic, value, duration=0)
    
    """
        Switch light on or off
    """
    def switch_light(self, topic:str, state:bool, is_dimmable:bool = False):
        serv = "out_bin_switch"
        if is_dimmable:
            serv = "out_lvl_switch"

        fimp = FIMPMessage(
            serv=serv,
            type="cmd.binary.set",
            val_t="bool",
            val=state,
            topic=topic
        )

        logger.debug(f"Publishing to {topic}")
        logger.debug(f"Payload: {fimp.to_json()}")

        mqtt.client.publish(topic, payload=fimp.to_json(), qos=0, retain=False)

    def dim_light(self, topic:str, level:int, duration:int = 2):
        fimp = FIMPMessage(
            serv="out_lvl_switch",
            type="cmd.lvl.set",
            val_t="int",
            val=level,
            props={
                "duration": str(duration)
            },
            topic=topic
        )

        logger.debug(f"Publishing to {topic}")
        logger.debug(f"Payload: {fimp.to_json()}")


        mqtt.client.publish(topic, payload=fimp.to_json(), qos=0, retain=False)

    """
        Ask for report from device to get current state on startup
    """
    def ask_for_report(self):
        addr = f"pt:j1/mt:cmd{self.address}"
        serv = "out_bin_switch"
        if self.is_dimmable:
            serv = "out_lvl_switch"

        fimp = FIMPMessage(
            serv=serv,
            type="cmd.lvl.get_report",
            topic=addr
        )

        logger.debug(f"Asking for report from {self.name}")
        logger.debug(f"Publishing to {addr}")
        logger.debug(f"Payload: {fimp.to_json()}")

        mqtt.client.publish(addr, payload=fimp.to_json())

    def stop(self):
        super().stop()