import logging
import os

from logging.handlers import RotatingFileHandler


LOG_FOLDER = "logs"
LOG_FILE = "library.log"

os.makedirs(LOG_FOLDER, exist_ok=True)

log_path = os.path.join(
    LOG_FOLDER,
    LOG_FILE
)

handler = RotatingFileHandler(
    log_path,
    maxBytes=1024 * 1024,
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(
    formatter
)

logger = logging.getLogger(
    "library_app"
)

logger.setLevel(
    logging.INFO
)

if not logger.handlers:
    logger.addHandler(handler)