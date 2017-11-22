""" Configuring root logger """
import logging


logger = logging.getLogger()  # pylint: disable=invalid-name
handler = logging.StreamHandler()  # pylint: disable=invalid-name
formatter = logging.Formatter('[{levelname}][{name}] {message}', style='{')  # pylint: disable=invalid-name
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
