import argparse
import logging
import logging.config
import sys

from src.bean_db import persist_to_db

sys.path.append('./config')
import config
import flaskconfig
from flaskconfig import SQLALCHEMY_DATABASE_URI

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

