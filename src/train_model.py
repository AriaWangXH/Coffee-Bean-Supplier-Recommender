import sys
import os
import yaml
import warnings
import logging.config
warnings.filterwarnings('ignore')

import pandas as pd

import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt

from cycler import cycler

import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle

now = datetime.datetime.now().strftime("%Y-%m-%d")
dateplus = lambda x: "%s-%s" % (now, x)

sys.path.append('./config')
import config

# Logging
# logging.config.fileConfig(config.LOGGING_CONFIG)
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__file__)


# Update matplotlib defaults to something nicer
mpl_update = {
    'font.size': 16,
    'axes.prop_cycle': cycler('color', ['#0085ca', '#888b8d', '#00c389', '#f4364c', '#e56db1']),
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'figure.figsize': [12.0, 8.0],
    'axes.labelsize': 20,
    'axes.labelcolor': '#677385',
    'axes.titlesize': 20,
    'lines.color': '#0055A7',
    'lines.linewidth': 3,
    'text.color': '#677385',
    'font.family': 'sans-serif',
    'font.sans-serif': 'Tahoma'
}
mpl.rcParams.update(mpl_update)


def read_data(file_path):
    """Read the csv data file.
    Args:
        file_path (`str`): Location of the cloud data.
    Returns:
        clouds_data (`pandas.DataFrame`): The cloud data in a pandas data frame.
    """

    if not file_path:
        raise FileNotFoundError

    try:
        clouds_data = pd.read_csv(file_path)
    except Exception as e:
        logger.error("Failed to read data from {}".format(file_path), e)
        pass

    return clouds_data

def feature_split(data, feature_names):
    result = data[feature_names]
    return result

def get_scaler(unscaled_date, feature_names, feature_scaler_path):
    scaler = StandardScaler()
    feature_scaler = scaler.fit(unscaled_date[feature_names])

    with open(feature_scaler_path, "wb") as f:
        pickle.dump(feature_scaler, f)
    return feature_scaler


def stand_feat(unscaled_date, feature_names, feature_scaler):
    scaler = feature_scaler.fit(unscaled_date[feature_names])
    scaled_features = scaler.transform(unscaled_date[feature_names])

    return scaled_features


def plot_sil_iner(scaled_features, kmin, kmax, random_state, figs_folder):
    silhouette = []
    inertia = []

    # To capture model objects for each k
    models = {}

    # Upper bound for range of k to try
    for k in range(kmin, kmax):
        # Create model object
        model = KMeans(n_clusters=k, random_state=random_state)

        # Train model object
        model.fit(scaled_features)

        # Get inertia calculated for trained model
        inertia.append(model.inertia_)

        # Calculate silhouette score of trained model
        silhouette.append(sklearn.metrics.silhouette_score(scaled_features, model.labels_))

        # Capture trained model object
        models[k] = model

    fig, ax = plt.subplots(figsize=(12, 8));
    ax.scatter(range(kmin, kmax), inertia);
    ax.set_xlabel('Number of clusters, $k$');
    ax.set_ylabel('Inertia');
    ax.set_title('Inertia vs number of clusters');
    fig_path = os.path.join(figs_folder, dateplus('initial.png'))
    fig.savefig(fig_path)

    fig, ax = plt.subplots(figsize=(12, 8));
    ax.scatter(range(kmin, kmax), silhouette);
    ax.set_xlabel('Number of clusters, $k$');
    ax.set_ylabel('Silhouette score');
    fig_path = os.path.join(figs_folder, dateplus('silhouette.png'))
    fig.savefig(fig_path)



def train_model(scaled_features, k_chosen, random_state, save_tmo_path):
    """Train the classification model.
    Args:
        X_train (`pd.DataFrame`): Features in the training set.
        y_train (`:obj:`list` of :obj:`int`): List of target values in the training set.
        initial_features (`:obj:`list` of :obj:`str`): List of selected features.
        method: Type of model to train. Options = ('logistic', 'svm')
        save_tmo_path (`str`): Path to save trained model object. Optional. Default None.
         sample_weight: array-like of shape (n_samples,) default=None. Array of weights that are assigned to individual
                        samples. If not provided, then each sample is given unit weight.
        **kwargs: Keyword arguments for sklearn.linear_model.LogisticRegression. Please see sklearn documentation
                  for all possible options:
                  https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
    Returns:
        model (`sklearn.linear_model.LogisticRegression`): Trained model object.
    """

    logger.info('Training a K-means')

    try:
        kmeans_model = KMeans(n_clusters=k_chosen, random_state=random_state)
        kmeans_model.fit(scaled_features)
        # full_data['cluster'] = kmeans_model.predict(scaled_features)
    except Exception as e:
        logger.error("Error occurred when fitting the model", e)
        pass

    try:
        if save_tmo_path is not None:
            model_path = os.path.join(save_tmo_path, 'kmeans-' + str(k_chosen) + '-' + now + '.pkl')
            with open(model_path, "wb") as f:
                pickle.dump(kmeans_model, f)
            logger.info("Trained model object saved to %s", save_tmo_path)
    except:
        logger.error("Error occurred when saving the trained model")
        pass

    return kmeans_model


def predict_cluster(feat_scaler, raw_features, kmeans_model):
    scaled_features = feat_scaler.transform(raw_features)
    clusters = kmeans_model.predict(scaled_features)
    return clusters

def save_csv(data, data_path):
    """Save the data frame.
    Args:
        features (`pd.DataFrame`): Features data frame.
        target (`:obj:`list` of :obj:`str`): List of target variable values
        data_path (`str`): Path to save the data
    Returns:
        None.
    """
    if not data_path:
        raise FileNotFoundError
    try:
        data.to_csv(data_path, index=False)
    except Exception as e:
        logger.error("Failed to save the data for modeling", e)


if __name__ == "__main__":
    """
    The script trains a logistic/svm model on the training data and calculates predicted values for the test data.
    """

    with open(config.YAML_PATH, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config_tm = config["train_model"]

    try:
        logger.debug("Loading data")
        path_full = config['generate_feature']['save_csv']['data_path']
        data_full = read_data(path_full)
        # feature_names = config['generate_feature']['feature_split']['feature_names']
        data_model = feature_split(data_full, **config['generate_feature']['feature_split'])
        logger.info("Successfully loaded the data for modeling")
    except Exception as e:
        logger.error("Failed to load the data for modeling.", e)
        sys.exit(1)

    feature_names = config['generate_feature']['feature_split']['feature_names']
    data_scaler = get_scaler(data_model, feature_names, **config_tm['get_scaler'])
    data = stand_feat(data_model, feature_names, data_scaler)
    plot_sil_iner(data, **config_tm['plot_sil_iner'])

    try:
        logger.debug("Fitting model")
        model = train_model(data, **config_tm['train_model'])
        clusters_pred = predict_cluster(data_scaler, data_model, model)
        logger.info("Successfully fitted and saved the model")
    except Exception as e:
        logger.error("Failed to fit the model.", e)
        sys.exit(1)

    data_full['cluster'] = clusters_pred
    save_csv(data_full, **config_tm['save_csv'])
