from os import path

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

PATH_SRC = path.join(PROJECT_HOME, 'src')

