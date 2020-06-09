docker run -it \
-p 5000:5000 \
--env MYSQL_HOST \
--env MYSQL_PORT \
--env MYSQL_USER \
--env MYSQL_PASSWORD \
--env DATABASE_NAME \
--env S3_PUBLIC_KEY \
--env S3_SECRET_KEY \
--mount type=bind,source="$(pwd)",target=/app/ \
bean src/bean_db.py