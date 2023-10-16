import logging
import logging.handlers
import argparse

logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Configure so that the last 1mb of logs are saved
handler = logging.handlers.RotatingFileHandler("bridge.log", maxBytes=1000000, backupCount=1)
bridge_logger = logging.getLogger("Bridge")

# Add the handler to the logger
bridge_logger.addHandler(handler)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Enable debug logging", action="store_true")
args = parser.parse_args()

if args.debug:
    bridge_logger.setLevel(logging.DEBUG)
else:
    bridge_logger.setLevel(logging.INFO)
