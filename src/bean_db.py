import os
import logging
import logging.config
import sqlalchemy as sql
import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Text, MetaData
from helpers import create_connection, get_session
import config

# Obtain parameters from os
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
database = os.environ.get("DATABASE_NAME")
local_database_path = config.LOCAL_DATABASE_PATH

Base = declarative_base()

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('bean-models')

class BeanAttributes(Base):
    """ Defines the data model for the table `bean_attributes`. """

    __tablename__ = 'bean_attributes'

    id = Column(String(100), primary_key=True, unique=True, nullable=False)
    species = Column(String(100), unique=False, nullable=True)
    owner = Column(Text, unique=False, nullable=True)
    country = Column(Text, unique=False, nullable=True)
    farm_name = Column(Text, unique=False, nullable=True)
    company = Column(Text, unique=False, nullable=True)
    region = Column(Text, unique=False, nullable=True)
    producer = Column(Text, unique=False, nullable=True)
    grading_date = Column(String(100), unique=False, nullable=True)
    processing_method = Column(Text, unique=False, nullable=True)
    aroma = Column(Float, unique=False, nullable=True)
    flavor = Column(Float, unique=False, nullable=True)
    aftertaste = Column(Float, unique=False, nullable=True)
    acidity = Column(Float, unique=False, nullable=True)
    body = Column(Float, unique=False, nullable=True)
    balance = Column(Float, unique=False, nullable=True)
    uniformity = Column(Float, unique=False, nullable=True)
    cleancup = Column(Float, unique=False, nullable=True)
    sweetness = Column(Float, unique=False, nullable=True)
    total_cup_point = Column(Float, unique=False, nullable=True)
    moisture = Column(Float, unique=False, nullable=True)
    color = Column(Text, unique=False, nullable=True)

    def __repr__(self):
        return '<BeanAttributes %r>' % self.id


def _truncate_bean_attributes(session):
    """Deletes bean attributes table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM bean_attributes''')


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base`.

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """

    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from tweet_scores table before create_all "
                             "so that table can be recreated without unique id issues ")
    args = parser.parse_args()

    # Whether to create a local SQLite database or an AWS RDS database
    if config.LOCAL_DB_FLAG:
        engine_string = "sqlite:///{}".format(local_database_path)
    else:
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

    # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the tweet_score table)
    if args.truncate:
        session = get_session(engine_string=engine_string)
        try:
            logger.info("Attempting to truncate bean_attributes table.")
            _truncate_bean_attributes(session)
            session.commit()
            logger.info("bean_attributes truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate bean_attributes table.")
            logger.error(e)
        finally:
            session.close()

    create_db(engine_string=engine_string)

    try:
        engine = sql.create_engine(engine_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        bean1 = BeanAttributes(id='200', species='Arabica', owner='metad plc',
                               country='us', farm_name='some farm',
                               company='Nestle', region='Chicago',
                               producer='some producer', grading_date='some date',
                               processing_method='unknown', aroma=3, flavor=10,
                               aftertaste=7, acidity=8, body=8,
                               balance=8.9, uniformity=4, cleancup=7,
                               sweetness=8.8, total_cup_point=80,
                               moisture=2, color='brown'
                         )
        session.add(bean1)
        session.commit()
        logger.info("Database created with one row")
    except sqlalchemy.exc.IntegrityError as e:      # Check primary key duplication
        logger.error("Duplicated coffee bean")
    except sqlalchemy.exc.OperationalError:         # Check credentials
        logger.error("Incorrect credentials, access denied")
    finally:
        session.close()