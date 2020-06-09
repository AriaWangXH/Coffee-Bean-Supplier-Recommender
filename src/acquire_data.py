import boto3
import os
import sys
import logging.config
import logging
from botocore.exceptions import ClientError

sys.path.append('./config')
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('acquire_data')


if __name__ == "__main__":
    """Write the data object to S3 bucket. 
    """

    S3_BUCKET_NAME = config.S3_BUCKET_NAME
    S3_OBJECT_NAME = config.S3_OBJECT_NAME
    S3_PUBLIC_KEY = config.S3_PUBLIC_KEY
    S3_SECRET_KEY = config.S3_SECRET_KEY
    DOWNLOADED_DATA_PATH = config.DOWNLOADED_DATA_PATH

    # Check the elements for boto3 to be non-empty strings
    for element in [S3_PUBLIC_KEY, S3_SECRET_KEY, S3_BUCKET_NAME, S3_OBJECT_NAME, DOWNLOADED_DATA_PATH]:
        if element is None:
            logger.error("Empty info for DOWNLOADED_DATA_PATH and S3 bucket in config.py")
            sys.exit(1)
        if not isinstance(element, str):
            logger.error("Change the data type of {} to string in config.py".format(element))
            sys.exit(1)

    s3 = boto3.resource('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)

    # Acquire raw data from S3
    try:
        s3 = boto3.resource('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)
        bucket = s3.Bucket(S3_BUCKET_NAME)
        bucket.download_file(S3_OBJECT_NAME, DOWNLOADED_DATA_PATH)
        logger.info("Data successfully acquired")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


