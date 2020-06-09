import sys
import os
import logging.config
import yaml
import warnings
warnings.filterwarnings('ignore')

sys.path.append('./config')
import config

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import datetime

from cycler import cycler

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

now = datetime.datetime.now().strftime("%Y-%m-%d")
dateplus = lambda x: "%s-%s" % (now, x)

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('generate-features')


def read_data(file_path, column_names):
    """Read the data file.
    Args:
        file_path (`str`): Location of the cloud data.
        column_names (`:obj:`list` of :obj:`str`): List of column names to be saved to the output.
    Returns:
        bean_data (`pandas.DataFrame`): The bean data in a pandas data frame.
    """

    # Check data path to be non-empty
    if not file_path:
        raise FileNotFoundError

    try:
        bean_data = pd.read_csv(file_path, usecols=column_names)
        logger.info("Data successfully loaded")
    except Exception as e:
        logger.error("Failed to read data from {}".format(file_path), e)
        pass

    return bean_data


def feature_split(data, feature_names):
    """Split the data into features.
    Args:
        data (`pandas.DataFrame`): Full data.
        feature_names (`:obj:`list` of :obj:`str`): List of column names to be used as features
    Returns:
        result (`pandas.DataFrame`): The features in a data frame
    """

    result = data[feature_names]
    return result


def histogram(features, figs_folder, figs_name):
    """Create histograms for all features.
    Args:
        features (`pandas.DataFrame`): Features data frame.
        figs_folder (`str`): Directory for bar plots.
        figs_name (`str`): Name for bar plots
    Returns:
        None.
    """

    # Check path to store the histograms to be non-empty
    if not figs_folder or not figs_name:
        logger.warning("Directory and name for histograms should be non-empty")

    # Plot histograms for all the features
    figs = []
    for feat in features.columns:
        try:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.hist([features[feat].values], bins=40)
            ax.set_xlabel(' '.join(feat.split('_')).capitalize())
            ax.set_ylabel('Number of observations')
            fig_path = os.path.join(figs_folder, feat + '-' + dateplus(figs_name))
            fig.savefig(fig_path)
            figs.append(fig)
        except Exception as e:
            logger.error("Failed to plot {}".format(feat), e)
            pass

    return


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
    The script reads the acquired data and creates histograms for all the features.
    """

    with open(config.YAML_PATH, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config_gf = config["generate_feature"]

    try:
        logger.debug("Loading data")
        data = read_data(**config_gf['read_data'])
    except Exception as e:
        logger.error("Error occurred while loading data from the local path.", e)
        sys.exit(1)

    try:
        features = feature_split(data, **config_gf['feature_split'])
        logger.info("Successfully saved the features for modeling")
    except Exception as e:
        logger.error("Error occurred while splitting and saving the features.", e)
        sys.exit(1)

    try:
        histogram(features, **config_gf['histogram'])
        logger.info("Successfully plot features")
    except Exception as e:
        logger.error("Error occurred while plotting features.", e)
        sys.exit(1)

    try:
        logger.debug("Saving data after feature engineering")
        save_csv(data, **config_gf['save_csv'])
    except Exception as e:
        logger.error("Error occurred while saving the data for modeling.", e)
        sys.exit(1)
