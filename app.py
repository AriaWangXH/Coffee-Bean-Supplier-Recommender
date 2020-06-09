import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
import pandas as pd
import pickle

from src.train_model import predict_cluster
from src.bean_db import BeanAttributes
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Main view that lists beans in the database.
    Create view into index page that uses data queried from BeanAttribute database and
    inserts it into the app/templates/index.html template.
    Returns: rendered html template
    """

    if request.method == 'POST':
        try:
            # Insert the input entry into the database
            entries = pd.DataFrame({'Aroma': [request.form['aroma']],
                                    'Aftertaste': [request.form['aftertaste']],
                                    'Acidity': [request.form['acidity']],
                                    'Sweetness': [request.form['sweetness']],
                                    'Moisture': [request.form['moisture']]})

            sc = pickle.load(open('models/feature_scaler.pkl', 'rb'))
            model = pickle.load(open('models/kmeans-5-2020-06-08.pkl', 'rb'))
            cluster_pred = predict_cluster(sc, entries, model)[0]

            bean1 = BeanAttributes(
                                   species='Unknown',
                                   owner='Unknown',
                                   country='Unknown',
                                   farm_name='Unknown',
                                   company='Unknown',
                                   region='Unknown',
                                   producer='Unknown',
                                   grading_date='Unknown',
                                   processing_method='Unknown',
                                   aroma=request.form['aroma'],
                                   flavor=0,
                                   aftertaste=0,
                                   acidity=0,
                                   body=0,
                                   balance=0,
                                   uniformity=0,
                                   cleancup=0,
                                   sweetness=request.form['sweetness'],
                                   total_cup_point=0,
                                   moisture=request.form['moisture'],
                                   color='Unknown',
                                   cluster=cluster_pred)
            db.session.add(bean1)
            db.session.commit()
            logger.info("New cluster predicted: {}".format(cluster_pred))

            # Query the beans based on the predicted cluster of input features
            beans = db.session.query(BeanAttributes).\
                filter(BeanAttributes.cluster == 1).\
                order_by(BeanAttributes.total_cup_point.desc()).limit(app.config["MAX_ROWS_SHOW"]).all()
            return render_template('index.html', beans=beans)
        except Exception as e:
            traceback.print_exc()
            logger.error("Not able to add mew record")
            logger.error(e)
            return render_template('error.html')

    else:
        try:
            # Query the beans and sort the displayed records by total cup point
            beans = db.session.query(BeanAttributes).order_by(BeanAttributes.total_cup_point.desc()).\
                limit(app.config["MAX_ROWS_SHOW"])
            logger.info("Successfully queried from the database")
            return render_template('index.html', beans=beans)

        except Exception as e:
            logger.warning("Not able to display tracks, error page returned", e)
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])