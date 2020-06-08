import os
import sys
import logging.config
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Text, Integer

sys.path.append('./config')
import config

import pandas as pd
import numpy as np


logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)

Base = declarative_base()

class BeanAttributes(Base):
    """ Defines the data model for the table `bean_attributes`. """

    __tablename__ = 'bean_attributes'

    id = Column(Integer, primary_key=True)
    species = Column(String(100), unique=False, nullable=True)
    owner = Column(String(100), unique=False, nullable=True)
    country = Column(String(100), unique=False, nullable=True)
    farm_name = Column(String(100), unique=False, nullable=True)
    company = Column(String(100), unique=False, nullable=True)
    region = Column(String(100), unique=False, nullable=True)
    producer = Column(String(100), unique=False, nullable=True)
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
    color = Column(String(100), unique=False, nullable=True)
    cluster = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<BeanAttributes %r>' % self.id

def persist_to_db(engine_string):
    engine = sql.create_engine(engine_string)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # delete all existing records in the table
    if config.LOCAL_DB_FLAG:
        try:
            session.execute('''DELETE FROM msia_db.bean_attributes''')
        except:
            pass
    else:
        try:
            session.execute('''DELETE FROM bean_attributes''')
        except:
            pass

    raw_data = pd.read_csv(config.DATA_TABLE_PATH)
    raw_data = raw_data.replace(np.nan, '', regex=True)

    try:
        for i in range(raw_data.shape[0]):
            bean_row = BeanAttributes(id=int(raw_data.iloc[i]['Unnamed: 0']),
                                      species=str(raw_data.iloc[i]['Species']),
                                      owner=str(raw_data.iloc[i]['Owner.1']),
                                      country=str(raw_data.iloc[i]['Country.of.Origin']),
                                      farm_name=str(raw_data.iloc[i]['Farm.Name']),
                                      company=str(raw_data.iloc[i]['Company']),
                                      region=str(raw_data.iloc[i]['Region']),
                                      producer=str(raw_data.iloc[i]['Producer']),
                                      grading_date=str(raw_data.iloc[i]['Grading.Date']),
                                      processing_method=str(raw_data.iloc[i]['Processing.Method']),
                                      aroma=float(raw_data.iloc[i]['Aroma']),
                                      flavor=float(raw_data.iloc[i]['Flavor']),
                                      aftertaste=float(raw_data.iloc[i]['Aftertaste']),
                                      acidity=float(raw_data.iloc[i]['Acidity']),
                                      body=float(raw_data.iloc[i]['Body']),
                                      balance=float(raw_data.iloc[i]['Balance']),
                                      uniformity=float(raw_data.iloc[i]['Uniformity']),
                                      cleancup=float(raw_data.iloc[i]['Clean.Cup']),
                                      sweetness=float(raw_data.iloc[i]['Sweetness']),
                                      total_cup_point=float(raw_data.iloc[i]['Total.Cup.Points']),
                                      moisture=float(raw_data.iloc[i]['Moisture']),
                                      color=str(raw_data.iloc[i]['Color']),
                                      cluster=int(raw_data.iloc[i]['cluster'])
                                      )
            session.add(bean_row)
            logger.debug('Row %d added to table ' % i)
            session.commit()
    except sql.exc.IntegrityError as e:  # Check primary key duplication
        logger.error("Duplicated coffee bean")
    # except sql.exc.OperationalError:         # Check credentials
    except Exception as e:
        logger.error("Incorrect credentials, access denied", e)
    finally:
        session.close()

if __name__ == "__main__":

    # Obtain parameters from os
    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    database = os.environ.get("DATABASE_NAME")
    local_database_path = config.LOCAL_DATABASE_PATH


    # Whether to create a local SQLite database or an AWS RDS database
    if config.LOCAL_DB_FLAG:
        engine_string = "sqlite:///{}".format(local_database_path)
    else:
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

    try:
        persist_to_db(engine_string)
        logger.info("Data successfully persisted into the database")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


