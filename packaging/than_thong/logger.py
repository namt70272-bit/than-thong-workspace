"""Logging — file + console with rotation."""
import logging, sys
from pathlib import Path
from than_thong.config import config

LEVELS = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
           "WARN": logging.WARNING, "ERROR": logging.ERROR}

def setup():
    level = LEVELS.get(config.get("log_level", "INFO"), logging.INFO)
    log_path = config.log_path

    logger = logging.getLogger("than-thong")
    logger.setLevel(level)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


log = setup()
