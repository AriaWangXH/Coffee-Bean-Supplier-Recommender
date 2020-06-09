# MSiA423 Project (Beans!) Repository


<em>Developedc by Xiaohan (Aria) Wang, QA by Yige (Irene) Lai.</em>


<!-- tocstop -->

- [Project Charter](#project-charter)
  * [Vision](#vision)
  * [Mission](#mission)
  * [Success riteria](#success-criteria)
- [Backlog](#backlog)
  * [Planning](#planning)
  * [Backlog](#backlog)
  * [Icebox](#icebox)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Acquire the raw data](#1-acquire-the-raw-data)
  * [2. Write the data to S3 bucket](#2-write-the-data-to-s3-bucket)
  * [3. Execute the pipeline for modeling](#3-execute-the-pipeline-for-modeling)
  * [4. Create the database](#4-create-the-database)
    + [Query a table](#query-a-table)
  * [5. Run the Flask app](#5-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
- [Testing](#testing)

<!-- tocstop -->

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


## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│   ├── Dockerfile_bash               <- Dockerfile for building image to run the model building pipeline  
│
├── config                            <- Directory for configuration files 
│   ├── logging/                      <- Configuration of python loggers
│   ├── config.py                     <- Configurations for uploading data to S3 bucket and AWS RDS 
│   ├── config.yaml                   <- Configurations for model pipeline 
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data table
│   ├── bean.db                       <- Local SQLite database
│   ├── clusters.csv                  <- Data frame containing coffee bean clusters after model prediction
│   ├── data_clean.csv                <- Data frame with selected columns
│
├── deliverables/                     <- Presentation slides 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs)
│
├── notebooks/
│   ├── develop/                      <- Current notebooks being used in development.
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│   ├── acquire_data.py               <- Acquire raw data from S3 bucket
│   ├── bean_db.py                    <- Create the database in SQLite or AWS RDS 
│   ├── evaluate_model.py             <- Evaluate the K-means clustering performance 
│   ├── generate_features.py          <- Feature engineering and exploratory analysis 
│   ├── train_model.py                <- Train and select the best model 
│   ├── write_to_s3.py                <- Write the raw data to S3 bucket 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── requirements.txt                  <- Python package dependencies 
├── run-pipeline.sh                   <- Script for building image to run the model building pipeline
├── run-reproducibility-tests.sh      <- Script for building image to run unit tests
├── run_docker.sh                     <- Script for building image to create local SQLite data base or an RDS instance
├── run_mysql_client.sh               <- Script for building image to query the database
```

## Running the app
### 1. Acquire the raw data 

Download the dataset from [this Kaggle page](https://www.kaggle.com/volpatto/coffee-quality-database-from-cqi?select=merged_data_cleaned.csv).
Make sure to choose the `merged_data_cleaned.csv` data file.

Move the downloaded data file under the `data/external` folder.
Or move the file to other places and be sure to specify the new location in `src/config.py` after `DOWNLOADED_DATA_PATH = `.


### 2. Write the data to S3 bucket
Specify the S3 bucket and object name in `src/config.py` after `S3_BUCKET_NAME` and `S3_OBJECT_NAME`.

To build the Docker image, run from this directory (the root of the repo):

```bash
 docker build -f app/Dockerfile -t bean .
```

Run the following command with your AWS credentials.

```bash
 docker run -e S3_PUBLIC_KEY=<your_aws_access_key> -e S3_SECRET_KEY=<your_aws_secret_key> bean src/write_to_s3.py
```

### 3. Execute the pipeline for modeling
If needed, change the file paths and parameters in `config/config.yaml`.

Build the docker image from the root of the repository with the command below:

```bash
 docker build -f app/Dockerfile_bash -t bean .
```
Execute the pipeline and reproduce the analysis using a single docker run command (fill in your aws access and secret keys):

```bash
 docker run -e S3_PUBLIC_KEY=<your_aws_access_key> -e S3_SECRET_KEY=<your_aws_secret_key> --mount type=bind,source="$(pwd)"/,target=/app/ bean run-pipeline.sh
```

### 4. Create the database
Option 1. Create a local SQLite database

Go to `src/config.py`, specify `True` for `LOCAL_DB_FLAG`. 

Change the default local database path `data/bean.db` if needed.

Build the Docker image with the command below:

```bash
 docker build -f app/Dockerfile -t bean .
```

Run the following command to create local SQLite database.

```bash
 docker run --mount type=bind,source="$(pwd)",target=/app/ bean src/bean_db.py
```

Option 2. Create an AWS RDS database (*Note: connect to Northwestern VPN for this option*)

Go to `src/config.py`, specify `False` for `LOCAL_DB_FLAG`

Run the command below and update the information.

```bash
 vi .mysqlconfig
```
1) Set `MYSQL_USER` to the “master username” that you used to create the database server.
2) Set `MYSQL_PASSWORD` to the “master password” that you used to create the database server. 
3) Set `MYSQL_HOST` to be the RDS instance endpoint from the console
4) Set `MYSQL_POST` to be 3306
5) Set `DATABASE_NAME` to be the created database's name

Run the following command.

```bash
 source .mysqlconfig
```

Build the Docker image with the command below:

```bash
 sh run_docker.sh
```

#### Query a table
Option 1. From SQLite

Query tables within SQLite with the SQLite application or through applications such as `SQLAlchemy` in Python.

Option 2. From RDS

After `.mysqlconfig` is set up, run the following command:

```bash
 sh run_mysql_client.sh
```

Run `show databases` to view the databases

Run `show tables from <YOUR-DATABASE>` to view the tables in `<YOUR-DATABASE>`

Run `select * from <YOUR-DATABASE>.<YOUR-TABLE>` to query the table

### 5. Run the Flask app

To run the Flask app, run:

```bash
 python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t bean .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
 docker run -p 5000:5000 --name test bean
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `bean` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
 docker kill test 
```
Remove the `test` container with this command (`test` is the name given in the `docker run` command): 

```bash
 docker rm test 
```

## Testing
Build the image from the root of this repository with this command:
```bash
 docker build -f app/Dockerfile_bash -t bean .
```

Run reproducibility tests for feature engineering:

```bash
 docker run --mount type=bind,source="$(pwd)"/,target=/app/ clouds run-reproducibility-tests.sh
```
