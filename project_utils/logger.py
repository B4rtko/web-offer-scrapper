import logging
import os
from datetime import datetime
from logging import FileHandler, Logger


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        formatter = logging.Formatter(
            "%(levelname)s - %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.WARNING)
        logger.addHandler(sh)

        logs_dir_name = "tmp_logs"
        logs_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
        logs_file_path = os.path.join(logs_dir_name, logs_file_name)
        os.makedirs(logs_dir_name, exist_ok=True)

        fh = FileHandler(logs_file_path)
        fh.setFormatter(formatter)
        # fh.setLevel(logging.INFO)
        logger.addHandler(fh)
    return logger
