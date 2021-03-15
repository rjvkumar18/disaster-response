# Disaster Response Pipeline

## Table of Contents
1. [Project Motivation](#motivation)
2. [Getting Started](#getting_started)
	1. [Dependencies](#dependencies)
	2. [Installation](#installation)
	3. [Running the App](#executing)
	4. [Main Files](#files)
3. [Authors](#authors)
4. [License](#license)
5. [Acknowledgement](#acknowledgement)

<a name="motivation"></a>
## Project Motivation

This work is a part of Udacity Data Science Nano-degree program.
The initial dataset contains pre-labelled tweet and messages from real-life disasters. 
The main goal of this project is to build a Natural Language Processing tool that categorise messages and 
helps in identifying if these messages are related to disaster or not. This would be of great help for any disaster relief agencies.

This Project is divided into the following parts:

1. ETL Pipeline to extract data from source, clean data and save them in database
2. Machine Learning Pipeline to train a model and classify text message into multiple categories
3. Web App to display model results

<a name="getting_started"></a>
## Getting Started

<a name="dependencies"></a>
### Dependencies
* Python 3.*
* Machine Learning Libraries: NumPy, SciPy, Pandas, Sciki-Learn
* Natural Language Process Libraries: NLTK
* SQLlite Database Libraqries: SQLalchemy
* Web App and Data Visualization: Flask, Plotly

<a name="installation"></a>
### Installation
Clone this GIT repository:
```
git clone https://github.com/rjvkumar18/disaster-response.git
```
<a name="executing"></a>
### Running the App:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

<a name="files"></a>
### Main Files

* app/templates/*:
    - *master.html*: Main page of web app
    - *go.html*: Classification result page of web app
* *app/run.py*: Flask file that runs the app

* data/*:
    - *process_data.py*: ETL pipeline used for data extraction, preprocessing and loading in a SQLite database
    - *disaster_categories.csv*: Categories data to be processed
    - *disaster_messages.csv*: Messages data to be processed
    - *DisasterResponse.db*: Database to save cleaned data

* models/*:
    - *train_classifier.py*: A machine learning pipeline that loads data, trains a model, and saves the trained model as a .pkl file
    - *classifier.pkl*: Saved ML model


<a name="authors"></a>
## Authors

* [Rajeev](https://github.com/rjvkumar18/)

<a name="license"></a>
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<a name="acknowledgement"></a>
## Acknowledgements

* [Udacity](https://www.udacity.com/)
* [Figure Eight](https://www.figure-eight.com/)