from flask import request, render_template
from flask import current_app as app

# render_template alows to separate presentation from controller
# it will render HTML pages
# notice Flask uses Jinja2 template engine for rendering templates

# url_for() to reference static resources. 
# For example, to refer to /static/js/main.js, 
# you can use url_for('static', filename='js/main.js')

# request is to hold requests from a client e.g request.headers.get('')

# in the dynamic routes we can use 4 Flask context global variables:
# current_app, g, request, session
# Further details can be found in the Flask documentation 

# URLs to be handled by the app route handler

import os
from .logicmodel import PandasDataModel
import logging

# sort of print
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# dataset path
basedir = os.path.abspath(os.path.dirname(__file__))
dataset_path = os.path.join(basedir,"data/")
dataset_online_path = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/"

path_confirmed = dataset_online_path + "time_series_covid19_confirmed_global.csv"
path_deaths = dataset_online_path + "time_series_covid19_deaths_global.csv"
path_recovered = dataset_online_path + "time_series_covid19_recovered_global.csv"

local_path_confirmed = dataset_path + "time_series_covid19_confirmed_global.csv"
local_path_deaths = dataset_path + "time_series_covid19_deaths_global.csv"
local_path_recovered = dataset_path + "time_series_covid19_recovered_global.csv"

#datamodel = PandasDataModel(path_confirmed, path_deaths, path_recovered)
datamodel = PandasDataModel(local_path_confirmed, local_path_deaths, local_path_recovered)
#datamodel.writeDataset(local_path_confimed, local_path_deaths, local_path_recovered)

title='Big Data Visualization'

@app.route('/', methods=['GET'])
def home():
    listing = datamodel.getConfirmedListings()
    logger.info("Home")
    logger.info(listing)

    return render_template('home.html',
                            title=title,
                            data=listing,
                            template='home-template'
                        )

@app.route('/about', methods=['GET'])
def about():
    logger.info("About")
    listing = datamodel.getCountryListining()
    return render_template('about.html',
                            title=title,
                            data=listing,
                            template='about-template'
                        )

@app.route('/filtering', methods=['GET', 'POST'])
def filtering():
    # TODO
    listing = datamodel.getCountryListining()
    return render_template('about.html',
                            title=title,
                            data=listing,
                            template='about-template'
                        )



