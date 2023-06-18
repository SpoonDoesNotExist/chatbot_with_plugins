import logging
from typing import List


class Logger:
    def __init__(self):
        self.loggers: List = []
        self._init_file_logger()

    def _init_file_logger(self) -> None:
        # Configure the logger
        logging.basicConfig(
            filename='log_file.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Create a logger instance
        self.loggers.append(
            logging.getLogger()
        )

    def debug(self, message: str):
        list(map(
            lambda logger: logger.debug(message),
            self.loggers,
        ))

    def info(self, message: str):
        list(map(
            lambda logger: logger.info(message),
            self.loggers,
        ))

    def warning(self, message: str):
        list(map(
            lambda logger: logger.warning(message),
            self.loggers,
        ))

    def error(self, message: str):
        list(map(
            lambda logger: logger.error(message),
            self.loggers,
        ))
