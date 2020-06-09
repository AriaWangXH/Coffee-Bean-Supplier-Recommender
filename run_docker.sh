docker run -it \
-p 5000:5000 \
--env MYSQL_HOST=nw-msia423-aria-wang.cd3ne4wa7jus.us-east-2.rds.amazonaws.com \
--env MYSQL_PORT=3306 \
--env MYSQL_USER=admin \
--env MYSQL_PASSWORD=Wangxiaohan43! \
--env DATABASE_NAME=msia_db \
--env AWS_ACCESS_KEY_ID \
--env AWS_SECRET_ACCESS_KEY \
--env SQLALCHEMY_DATABASE_URI \
--mount type=bind,source="$(pwd)",target=/app/ \
bean