import boto3
import os
import sys
import logging.config
import logging
from botocore.exceptions import ClientError

sys.path.append('./config')
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('write_to_s3')

if __name__ == "__main__":
    """Write the data object to S3 bucket. 
    """

    S3_BUCKET_NAME = config.S3_BUCKET_NAME
    S3_OBJECT_NAME = config.S3_OBJECT_NAME
    S3_PUBLIC_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
    S3_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    DOWNLOADED_DATA_PATH = config.DOWNLOADED_DATA_PATH

    # Check the elements for boto3 to be non-empty
    for element in [S3_PUBLIC_KEY, S3_SECRET_KEY, S3_BUCKET_NAME, S3_OBJECT_NAME, DOWNLOADED_DATA_PATH]:
        if element is None:
            logger.error("Empty info for DOWNLOADED_DATA_PATH and S3 bucket in config.py")
            sys.exit(1)

    s3 = boto3.client('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)

    try:
        s3.upload_file(DOWNLOADED_DATA_PATH, S3_BUCKET_NAME, S3_OBJECT_NAME)
        logger.info('Data successfully write to the S3 bucket {} with name {}'.format(S3_BUCKET_NAME,
                                                                                      S3_OBJECT_NAME))
    except ClientError as e:
        logger.error("Error occurred with the S3 client.", e)
        sys.exit(1)


