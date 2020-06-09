import os
from os import path

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "bean"
DEBUG = True

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/logging.conf')

# Downloaded data path
DOWNLOADED_DATA_PATH = path.join(PROJECT_HOME, 'data/external/merged_data_cleaned.csv')

# S3 bucket
S3_BUCKET_NAME = 'msia423-bean'
S3_OBJECT_NAME = 'merged_data_cleaned.csv'
S3_PUBLIC_KEY = os.environ.get("S3_PUBLIC_KEY")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")

# SQLite database connection config
DATA_TABLE_PATH = path.join(PROJECT_HOME, 'data/clusters.csv')
LOCAL_DB_FLAG = True  # If true, create a local SQLite database
LOCAL_DB_NAME = 'data/bean.db'
LOCAL_DATABASE_PATH = path.join(PROJECT_HOME, LOCAL_DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# YAML for modeling
YAML_PATH = path.join(PROJECT_HOME, 'config/config.yaml')


