import boto3
import os
import sys
import config
import logging.config
import logging

aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('write_to_s3')

def upload_file(s3_client, data_path, s3_bucket, s3_object):
    """Upload the local data file to S3 bucket.

    Args:
        s3_client (:py:class:`boto3.client`): boto3 connection client
        data_path (`str`): the path of the local data file
        s3_bucket (`str`): S3 bucket name
        s3_object (`str`): S3 object name

    Returns:
        None
    """

    if not data_path:
        raise FileNotFoundError

    try:
        s3_client.upload_file(data_path, s3_bucket, s3_object)
        logger.info('Object `{}` successfully written to S3 bucket `{}`'.format(s3_bucket, s3_object))
    except ClientError as e:
        logger.error(e)

    return None


if __name__ == "__main__":
    """Write the data object to S3 bucket. 
    """

    S3_BUCKET_NAME = config.S3_BUCKET_NAME
    S3_OBJECT_NAME = config.S3_OBJECT_NAME
    DOWNLOADED_DATA_PATH = config.DOWNLOADED_DATA_PATH

    for element in [aws_access_key_id, aws_secret_access_key, S3_BUCKET_NAME, S3_OBJECT_NAME, DOWNLOADED_DATA_PATH]:
        if element is None:
            logger.error("Empty info for DOWNLOADED_DATA_PATH and S3 bucket in config.py")
            sys.exit(1)
        if not isinstance(element, str):
            logger.error("Change the data type of {} to string in config.py".format(element))
            sys.exit(1)


    boto3_client = boto3.client('s3', aws_access_key_id=S3_PUBLIC_KEY, aws_secret_access_key=S3_SECRET_KEY)

    try:
        upload_file(boto3_client, DOWNLOADED_DATA_PATH, S3_BUCKET_NAME, S3_OBJECT_NAME)
    except Exception as e:
        logger.error(e)
        sys.exit(1)


