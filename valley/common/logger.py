import os
import logging

logging.basicConfig()

logger = logging.getLogger("default")
logger.setLevel(level=os.environ.get("LOGLEVEL", "INFO").upper())
