import logging
import os
import yaml
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Setup application logger"""
    # Load configuration
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config["logging"]["file"])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure logger
    logger = logging.getLogger("taxassist")
    logger.setLevel(config["logging"]["level"])

    # Create formatter
    formatter = logging.Formatter(config["logging"]["format"])

    # Setup file handler
    file_handler = RotatingFileHandler(
        config["logging"]["file"],
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger 