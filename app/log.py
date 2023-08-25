import logging
import os


def get_logger():
    logger = logging.getLogger('egrul')
    format_ = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:file %(module)s line %(lineno)d:%(message)s')

    # File log
    file_name = os.path.dirname(__file__) + "/egrul.log"
    f_handler = logging.FileHandler(file_name)
    f_handler.setLevel(logging.INFO)
    f_handler.setFormatter(format_)
    logger.botlog_filename = file_name
    logger.addHandler(f_handler)

    # Console log
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter('%(name)s - %(levelname)s - file %(module)s line %(lineno)d - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    return logger


logger = get_logger()
