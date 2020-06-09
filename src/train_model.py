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
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s     %(message)s')
logger = logging.getLogger("train-model")


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
    'text.color': '#677385'
}
mpl.rcParams.update(mpl_update)


def read_data(file_path):
    """Read the csv data file.
    Args:
        file_path (`str`): Location of the data to be read in.
    Returns:
        bean_data (`pandas.DataFrame`): The bean data in a pandas data frame.
    """

    # Check the input data path to be non-empty
    if not file_path:
        raise FileNotFoundError

    try:
        bean_data = pd.read_csv(file_path)
    except Exception as e:
        logger.error("Failed to read data from {}".format(file_path), e)
        pass

    return bean_data


def feature_split(data, feature_names):
    """Split the data into features.
    Args:
        data (`pandas.DataFrame`): Full data.
        feature_names (`:obj:`list` of :obj:`str`): List of column names to be used as features.
    Returns:
        result (`pandas.DataFrame`): The features in a data frame.
    """

    result = data[feature_names]
    return result


def get_scaler(unscaled_date, feature_names, feature_scaler_path):
    """Get the scaler user for standardizing the features.
    Args:
        unscaled_date (`pandas.DataFrame`): Features before scaling.
        feature_names (`:obj:`list` of :obj:`str`): List of feature names
    Returns:
        feature_scaler (`sklearn.preprocessing._data.StandardScaler`): The feature scaler.
    """

    scaler = StandardScaler()
    feature_scaler = scaler.fit(unscaled_date[feature_names])

    with open(feature_scaler_path, "wb") as f:
        pickle.dump(feature_scaler, f)
    return feature_scaler


def stand_feat(unscaled_date, feature_names, feature_scaler):
    """Get the scaler user for standardizing the features.
    Args:
        unscaled_date (`pandas.DataFrame`): Features before scaling.
        feature_names (`:obj:`list` of :obj:`str`): List of feature names
        feature_scaler (`sklearn.preprocessing.StandardScaler`): The feature scaler.
    Returns:
        scaled_features (`pandas.DataFrame`): Features after scaling.
    """
    try:
        scaler = feature_scaler.fit(unscaled_date[feature_names])
        scaled_features = scaler.transform(unscaled_date[feature_names])
        return scaled_features
    except Exception as e:
        logger.error(e)
        return


def plot_sil_iner(scaled_features, kmin, kmax, random_state, figs_folder):
    """Plot silhouette and inertia scores for different number of clusters.
    Args:
        scaled_features (`pandas.DataFrame`): Features after scaling.
        kmin (`int`): The minimum number of the clusters.
        kmax (`int`): The maximum number of the clusters.
        random_state (`int`): The random state parameter for k-means clustering
        figs_folder (`str`): Directory for resulting figs.
    Returns:
        None.
    """

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
    """Train the k-means clustering model.
    Args:
        scaled_features (`pd.DataFrame`): Data frame of scaled features.
        k_chosen (`int`): The optimal number of clusters.
        random_state (`int`): The random state parameter for k-means clustering
        save_tmo_path (`str`): Path to save trained model object.
    Returns:
        kmeans_model (`sklearn.cluster.KMeans`): Trained model object.
    """

    logger.info('Training a K-means')

    try:
        kmeans_model = KMeans(n_clusters=k_chosen, random_state=random_state)
        kmeans_model.fit(scaled_features)
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
    """Predict the clusters.
    Args:
        feat_scaler (`sklearn.preprocessing._data.StandardScaler`): Scaler for standardizing the features.
        raw_features (`pd.DataFrame`): Data frame of scaled features.
        kmeans_model (`sklearn.cluster.KMeans`): Trained model object.
    Returns:
        clusters (`numpy.ndarray`): Array of predicted clusters.
    """

    scaled_features = feat_scaler.transform(raw_features)
    clusters = kmeans_model.predict(scaled_features)
    return clusters


def save_csv(data, data_path):
    """Save the data frame.
    Args:
        data (`pd.DataFrame`): Data to be stored.
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
        data_model = feature_split(data_full, **config['generate_feature']['feature_split'])
        logger.info("Successfully loaded the data for modeling")
    except Exception as e:
        logger.error("Failed to load the data for modeling.", e)
        sys.exit(1)

    try:
        feature_names = config['generate_feature']['feature_split']['feature_names']
        data_scaler = get_scaler(data_model, feature_names, **config_tm['get_scaler'])
        data = stand_feat(data_model, feature_names, data_scaler)
    except Exception as e:
        logger.error("Failed to standardize the features")
        logger.error(e)
        sys.exit(1)

    if data is None:
        logger.warning("Please check the column names of the data to be predicted")
        sys.exit(1)

    try:
        plot_sil_iner(data, **config_tm['plot_sil_iner'])
        logger.info("Successfully created and saved the silhouette and inertia plots")
    except Exception as e:
        logger.error("Failed to create the silhouette and inertia plots")
        logger.error(e)
        sys.exit(1)

    try:
        logger.debug("Fitting model")
        model = train_model(data, **config_tm['train_model'])
        clusters_pred = predict_cluster(data_scaler, data_model, model)
        logger.info("Successfully fitted and saved the model")
    except Exception as e:
        logger.error("Failed to fit the model.", e)
        sys.exit(1)

    try:
        data_full['cluster'] = clusters_pred
        logger.info("Predictions for clusters successfully created and saved")
    except Exception as e:
        logger.error("Failed to make predictions of the clusters")

    save_csv(data_full, **config_tm['save_csv'])
