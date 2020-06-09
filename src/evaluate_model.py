import sys
import os
import logging.config
import yaml
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d")
dateplus = lambda x: "%s-%s" % (now, x)

sys.path.append('./config')
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('evaluate-model')

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


def read_data(data_folder):
    """Read the data frame.
    Args:
        data_folder (`str`): Directory of the data.
    Returns:
        df (`pandas.DataFrame`): Data frame that's read in.
    """

    # Check data folder to be non-empty
    if not data_folder:
        raise FileNotFoundError

    try:
        df = pd.read_csv(data_folder)
    except Exception as e:
        logger.error("Failed to read data from {}".format(data_folder), e)
        pass

    return df


def plot_lift(data, feature_names, figs_folder):
    """Create lift plot of the trained model.
    Args:
        data (`pandas.DataFrame`): Data with clusters assigned.
        feature_names (`:obj:`list` of :obj:`str`): List of feature names.
        figs_folder (`str`): Directory to save the lift plot.
    Returns:
        None.
    """

    cluster_means = data.groupby('cluster')[feature_names].mean()
    population_means = data[feature_names].mean()
    lifts = cluster_means.divide(population_means)

    fig, ax = plt.subplots(figsize=(16, 10))

    xticklabels = lifts.index.tolist()
    yticklabels = lifts.columns.tolist()

    ax = sns.heatmap(lifts.T, center=1, vmax=2.5, cmap=sns.diverging_palette(10, 220, sep=80, n=7),
                     xticklabels=xticklabels, yticklabels=yticklabels, )
    ax.set_xlabel('Cluster number')
    ax.set_title('Lift in cluster features (Cluster mean/population mean)')
    fig_path = os.path.join(figs_folder, 'lift-' + now + '.png')
    fig.savefig(fig_path)


def count_clusters(data, figs_folder):
    """Count the number of coffee beans for each cluster.
    Args:
        data (`pandas.DataFrame`): Data with clusters assigned.
        figs_folder (`str`): Directory to save the result plot.
    Returns:
        None.
    """

    cluster_counts = data.groupby('cluster').count()[['Unnamed: 0']]
    counts_path = os.path.join(figs_folder, 'cluster_counts.csv')
    cluster_counts.to_csv(counts_path, index=False)

    ax = cluster_counts.divide(len(data)).plot(kind="barh", color='#888b8d', alpha=0.5)
    ax.set_xlabel("Fraction of beans belonging to cluster");
    ax.set_ylabel("Cluster label");
    ax.set_title("Relative size of each cluster");
    ax.get_legend().remove()
    fig_path = os.path.join(figs_folder, 'cluster-counts-' + now + '.png')
    fig = ax.get_figure()
    fig.savefig(fig_path)


if __name__ == "__main__":
    """
    The script fetches the trained model, prints the model coefficients and evaluates its prediction accuracy.
    """

    with open(config.YAML_PATH, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config_em = config["evaluate_model"]

    try:
        logger.debug("Loading true target values, predictions and the trained model")
        data_clusters = read_data(config["train_model"]['save_csv']['data_path'])
        logger.info("Successfully loaded true target values, predictions and the trained model")
    except Exception as e:
        logger.error("Failed to load the trained model and prediction values.", e)
        sys.exit(1)

    try:
        feature_names = config['generate_feature']['feature_split']['feature_names']
        plot_lift(data_clusters, feature_names, **config_em['plot_lift'])
        count_clusters(data_clusters, **config_em['count_clusters'])
        logger.info("Successfully created plots for lift and cluster counts.")
    except Exception as e:
        logger.error("Error occurred during creating plots for lift and cluster counts.")
        logger.error(e)
        sys.exit(1)


