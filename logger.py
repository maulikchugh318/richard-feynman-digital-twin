from loguru import logger
import sys
import os

os.makedirs("logs", exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time} | {level} | {message}"
)

logger.add(
    "logs/feynman.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)

app_logger = logger