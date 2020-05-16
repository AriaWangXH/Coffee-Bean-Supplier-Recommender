# MSiA423 Project (Beans!) Repository

<!-- toc -->
- Developer - Xiaohan (Aria) Wang
- Quality Assurance - Yige (Irene) Lai.



- [Project Charter](#project-charter)
- [Backlog](#backlog)

## Running the app
### Acquire the data 

- Download the dataset from [this Kaggle page](https://www.kaggle.com/volpatto/coffee-quality-database-from-cqi?select=merged_data_cleaned.csv).
Make sure to choose the `merged_data_cleaned.csv` data file and then click the 'Download' button.

- Move the downloaded data file under the `data/external` folder.
Or move the file to other places and be sure to specify the new location in `src/config.py` after `DOWNLOADED_DATA_PATH = `.


### Write the data to S3 bucket
- Specify the S3 bucket and object name in `src/config.py` after `S3_BUCKET_NAME` and `S3_OBJECT_NAME`.

- To build the Docker image, run from this directory (the root of the repo):

```bash
 docker build -f app/Dockerfile -t bean .
```

- Run the following command with your AWS credentials.

```bash
docker run -e AWS_ACCESS_KEY_ID=<aws_key> -e AWS_SECRET_ACCESS_KEY=<aws_secret_key> bean src/write_to_s3.py
```

### Create the database
Option 1. Create a local SQLite database

- Go to `src/config.py`, specify `True` for `LOCAL_DB_FLAG`. 

- Change the default local database path `data/bean.db` if needed.

- Build the Docker image with the command below:

```bash
 docker build -f app/Dockerfile -t bean .
```

- Run the following command to create local SQLite database.

```bash
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data bean src/bean_db.py
```

*Note: When recreating the database, add `--truncate` or `--t` at the end of the line above to avoid IntegrityError.*

Option 2. Create an AWS RDS database (*Note: connect to Northwestern VPN for this option*)

- Go to `src/config.py`, specify `False` for `LOCAL_DB_FLAG`

- Run the command below and update the information.

```bash
vi .mysqlconfig
```
1) Set `MYSQL_USER` to the “master username” that you used to create the database server.
2) Set `MYSQL_PASSWORD` to the “master password” that you used to create the database server. 
3) Set `MYSQL_HOST` to be the RDS instance endpoint from the console
4) Set `MYSQL_POST` to be 3306
5) Set `DATABASE_NAME` to be the created database's name

- Run the following command.

```bash
source .mysqlconfig
```

- Build the Docker image with the command below:

```bash
sh run_docker.sh
```
*Note: When recreating the database, add `--truncate` or `--t` inside `run_docker.sh` to avoid IntegrityError.*


### Query a table
Option 1. From SQLite

- Query tables within SQLite with the SQLite application or through applications such as `SQLAlchemy` in Python.

Option 2. From RDS

- After `.mysqlconfig` is set up, run the following command:

```bash
sh run_mysql_client.sh
```

- Run `show databases` to view the databases
- Run `show tables from <YOUR-DATABASE>` to view the tables in `<YOUR-DATABASE>`
- Run `select * from <YOUR-DATABASE>.<YOUR-TABLE>` to query the table




<!-- tocstop -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)

<!-- tocstop -->

## Project Charter
### Vission
This project aims to connect local coffee producers with wholesale coffee suppliers. While there are numerous farms that are producing coffee, it might still be difficult for the wholesale business to learn about coffee producers and find the kind of coffee that the market wants. By introducing sources of high-qulity coffee beans to the market, the 'Bean!' application helps improve the lives of local coffee producers and contributes to a thriving coffee community.

### Mission
From the application interface, users can input their desired values of coffee bean attributes (aroma, acidicity, etc.), and then they will get a list of 10 coffee beans generated from the k-means algorithm using the data scraped from [the Coffee Quality Institute's review pages](https://database.coffeeinstitute.org/). The dataset contains reviews of 1312 arabica and 28 robusta coffee beans from the Coffee Quality Institute's trained reviewers, and users can directly contact the owners of high-quality arabica and robusta lots by following the links provided in the app.

### Success criteria
The k-means clustering models will be evaluated by comparing their sum of squares within clusters and sum of squares between clusters, and from the F and Silhouette plots. The optimal number of clusters will generate distinct groups that contains coffee beans with very similar attributes. After the best model is chosen, the business value of this application will be evaluated by the number of coffee lots that the app connects with the market. This application will be considered as a success if at least 10% of the coffee bean producers are contacted from the link in the app.


## Backlog
### Planning
- Initiative 1. Build clustering models.
  * Epic 1. Prepare the data for analysis.

    + Story 1. Download the data from [this Kaggle page](https://www.kaggle.com/volpatto/coffee-quality-database-from-cqi?select=merged_data_cleaned.csv).
    + Story 2. Clean the data and correct inconsistencies due to human recording.
    + Stroy 3. Setting up RDS to query from the app.
  * Epic 2. Conduct exploratory data analysis.
    + Story 1. Capture patterns within the data and have a basic idea of the key variables in the clustering analysis.
  * Epic 3. Develop and come up with the best clustering model.
    + Story 1. Train k-means clustering models and test different values of k based on SSW, SSB and F and Silhouette plots. 
    + Story 2. Train and test Gaussian mixture models with different values of k and variance type.
    + Story 3. Explain the clusters and make sure they are meaningful and valuable.
- Initiative 2. Create the app.
  * Epic 1. Build the interactive interface for the app.
    + Story 1. Design the layout of home page, user input page and the output list.
    + Story 2. Use S3 to store the data on AWS.
  * Epic 2. Integrate the model and develop the app with Flask.
- Initiative 3. Test the app.
  * Epic 1. Test the app's functionality.
  * Epic 2. Conduct A/B tests to evaluate the app's business value.

### Backlog
- Initiative1.epic1.story1 (1 of story points) - PLANNED for next 2 weeks
- Initiative1.epic1.story2 (2 of story points) - PLANNED for next 2 weeks
- Initiative1.epic2.story1 (1 of story points) - PLANNED for next 2 weeks
- Initiative1.epic3.story1 (2 of story points) - PLANNED for next 2 weeks
- Initiative1.epic3.story3 (0 of story points) - PLANNED for next 2 weeks



### Icebox
- Initiative1.epic3.story2 (4 of story points) 
- Initiative2.epic1.story1
- Initiative2.epic1.story2
- Initiative2.epic2
- Initiative3.epic1
- Initiative3.epic2

** Explanation on the story points above:


0 points - quick chore; 1 point ~ 1 hour (small); 2 points ~ 1/2 day (medium); 4 points ~ 1 day (large); 8 points - big and needs to be broken down more when it comes to execution.




<!-- toc -->

# MSiA423 Template Repository

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/logging.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
