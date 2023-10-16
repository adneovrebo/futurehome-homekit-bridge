# Futurehome - Apple HomeKit Bridge

Integration for automatic bridging of devices connected to Futurehome hub to Apple HomeKit. The bridge utililzes `pyhap` which is a python implementation of the HomeKit Accessory Protocol (HAP).

## Getting started
1. Enable local API access over MQTT on your Futurehome hub. [See guide](https://support.futurehome.no/hc/en-no/articles/360033256491-Local-API-access-over-MQTT-Beta-)
2. Ensure the device running this bridge is on the same network as the Futurehome hub.
2. Clone the repository
3. Install dependencies
    - As a prerequisite, you will need Avahi/Bonjour installed (due to zeroconf package). On a Raspberry Pi/MacOs, you can get it with:
    `sudo apt-get install libavahi-compat-libdnssd-dev` 
    - Install python requirements 
    `pip install -r requirements.txt`
4. Create a `.env` file in the root of the project with the variables shown in `.env.example`
    - Tips: To find the ip of the hub use an app such as [Fing](https://www.fing.com/products/fing-app)
5. Run the bridge via `python3 main.py` or with docker via e.g.`docker-compose up`. Tips use the `-d` or `--debug` flag to see detailed debug logs (Last 1 MB of logs is stored in `bridge.log`).
6. Add the bridge to HomeKit by scanning the QR code or entering the pin code.
7. Enjoy your devices in HomeKit!

## Supported accessories
The supported devices implementations can be located in the `devices` directory.

### Supported accessories and characteristics
- Lightbulb
    - On of switch
    - Dimming

Feel free to add new implementations for other devices and submit a pull request. Adding new devices is easy, see [Adding support for new accessories](#adding-support-for-new-accessories).

### Adding support for new accessories
1. Create a new file in the `devices` directory with the name of the device.
2. Create a class that inherits from `Accessory` and implement the `__init__` and `update_state` methods.
3. Add functionality to the `update_state` method and add the characteristics to the `__init__` method.
4. Add case for the device in the `generate_accessories` method in `devices/device_factory.py`
5. Add the device to the `supported` list in the `README.md` file.


## Flow
1. Connecting to Futurehome hub via [local API access over MQTT](https://support.futurehome.no/hc/en-no/articles/360033256491-Local-API-access-over-MQTT-Beta-)
2. Discover devices connected to the hub via the `vinculum` `cmd.pd7.request` request.
    -  A List of devices gets stored in the `/data/devices.json` file.
3. For each device in the device list, a `Accessory` object is created and added to the `Bridge` object.
    - For each `Accessory` object, a subscription is created to get updates from the device. Also, a report request command is sent to the device to get the current state of the device. 
    - Messages from the device is handeled in the `on_message` method in `/futurehome/mqtt.py`. This calls update_state on the device with the payload. This updates the state of the device which reflected in the HomeKit Accessory.


## Examples
### Device information structure
```json
 {
    "client": {
        "name": "Lys soverom"
    },
    "fimp": {
        "adapter": "zwave-ad",
        "address": "11",
        "group": "ch_0"
    },
    "functionality": "lighting",
    "id": 2,
    "lrn": true,
    "model": "zw_411_4_8705",
    "param": {
        "dimValue": 66,
        "energy": 2.28999996185303,
        "power": "off",
        "timestamp": "2023-10-15 14:48:38 +0200",
        "wattage": 0.0,
        "zwaveConfigParameters": []
    },
    "problem": false,
    "room": 4,
    "services": {
        "dev_sys": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:dev_sys/ad:11_0",
            "enabled": true,
            "intf": [
                "cmd.config.get_report",
                "cmd.config.set",
                "cmd.group.add_members",
                "cmd.group.delete_members",
                "cmd.group.get_members",
                "cmd.ping.send",
                "evt.config.report",
                "evt.group.members_report",
                "evt.ping.report"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true
            }
        },
        "indicator_ctrl": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:indicator_ctrl/ad:11_0",
            "enabled": true,
            "intf": [
                "cmd.indicator.identify",
                "cmd.indicator.set_visual_element"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true
            }
        },
        "meter_elec": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:meter_elec/ad:11_0",
            "enabled": true,
            "intf": [
                "cmd.meter.get_report",
                "cmd.meter.reset",
                "evt.meter.report"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true,
                "sup_export_units": [],
                "sup_units": [
                    "kWh",
                    "W"
                ]
            }
        },
        "out_lvl_switch": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:out_lvl_switch/ad:11_0",
            "enabled": true,
            "intf": [
                "cmd.binary.set",
                "cmd.lvl.get_report",
                "cmd.lvl.set",
                "cmd.lvl.start",
                "cmd.lvl.stop",
                "evt.binary.report",
                "evt.lvl.report"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true,
                "max_lvl": 100,
                "min_lvl": 0
            }
        },
        "scene_ctrl": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:scene_ctrl/ad:11_0",
            "enabled": true,
            "intf": [
                "evt.scene.report"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true,
                "sup_scenes": [
                    "1.key_pressed_1_time",
                    "1.key_released",
                    "1.key_held_down",
                    "1.key_pressed_2_times",
                    "1.key_pressed_3_times",
                    "1.key_pressed_4_times",
                    "1.key_pressed_5_times",
                    "2.key_pressed_1_time",
                    "2.key_released",
                    "2.key_held_down",
                    "2.key_pressed_2_times",
                    "2.key_pressed_3_times",
                    "2.key_pressed_4_times",
                    "2.key_pressed_5_times"
                ]
            }
        },
        "version": {
            "addr": "/rt:dev/rn:zw/ad:1/sv:version/ad:11_0",
            "enabled": true,
            "intf": [
                "cmd.version.get_report",
                "evt.version.report"
            ],
            "props": {
                "is_secure": false,
                "is_unsecure": true
            }
        }
    },
    "supports": [
        "clear",
        "poll"
    ],
    "thing": 2,
    "type": {
        "subtype": null,
        "supported": {
            "appliance": [],
            "blinds": [],
            "fan": [],
            "heater": [],
            "light": []
        },
        "type": "light"
    }
}
```
