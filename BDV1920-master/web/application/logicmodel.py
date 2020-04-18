##############
# Logic layer
##############

import numpy as np
import pandas as pd
import json
import glob
import os
import logging

# sort of print
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# dealing with data computation 

class PandasDataModel:
	
	def readDataset(self, path_confirmed, path_deaths, path_recovered):
		self.confirmed = pd.read_csv(path_confirmed, error_bad_lines=False)
		self.deaths = pd.read_csv(path_deaths, error_bad_lines=False)
		self.recovered = pd.read_csv(path_recovered, error_bad_lines=False)
			
	def writeDataset(self, path_confirmed, path_deaths, path_recovered):
		self.confirmed.to_csv(path_confirmed, index=False)
		self.confirmed.to_csv(path_deaths, index=False)
		self.confirmed.to_csv(path_recovered, index=False)

	def __init__(self, path_confirmed, path_deaths, path_recovered):
			
		logger.info("Starting up Data Model...")
		self.readDataset(path_confirmed, path_deaths, path_recovered)
		#logger.info(self.confirmed, self.deaths, self.recovered)
		self.dfconfirmed = self.confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1).groupby('Country/Region').sum()
		self.dfdeaths = self.deaths.drop(['Province/State', 'Lat', 'Long'], axis=1).groupby('Country/Region').sum()
		self.dfrecovered = self.recovered.drop(['Province/State', 'Lat', 'Long'], axis=1).groupby('Country/Region').sum()
		#logger.info(list(self.dfconfirmed.columns), list(self.dfdeaths.columns), list(self.dfrecovered.columns))
		#logger.info(list(self.dfconfirmed.index), list(self.dfdeaths.index), list(self.dfrecovered.index))
		
		#{'row1': {'col1': 1, 'col2': 0.5}, 'row2': {'col1': 2, 'col2': 0.75} ...}
		self.confirmed_dict = self.dfconfirmed.to_dict(orient='index')
		self.death_dict = self.dfconfirmed.to_dict(orient='index')
		self.recovered_dict = self.dfconfirmed.to_dict(orient='index')
		
		self.confirmed_json = self.dfconfirmed.to_json()

		# My Code
		
		self.my_confirmed = self.dfconfirmed.pivot_table(index='Country/Region',aggfunc=sum).T
		self.my_deaths = self.dfdeaths.pivot_table(index='Country/Region',aggfunc=sum).T
		self.my_recovered = self.dfrecovered.pivot_table(index='Country/Region',aggfunc=sum).T
		self.confirmed_pt = self.my_confirmed['Portugal']
		self.deaths_pt = self.my_deaths['Portugal']
		self.recovered_pt = self.my_recovered['Portugal']
		self.confirmed_pt = pd.DataFrame(self.confirmed_pt)
		self.deaths_pt = pd.DataFrame(self.deaths_pt)
		self.recovered_pt = pd.DataFrame(self.recovered_pt)
		self.confirmed_pt = self.confirmed_pt.rename({'Portugal':'Confirmed'}, axis=1)
		self.deaths_pt = self.deaths_pt.rename({'Portugal':'Deaths'}, axis=1)
		self.recovered_pt = self.recovered_pt.rename({'Portugal':'Recovered'}, axis=1)
		self.result_pt = pd.concat([self.confirmed_pt, self.deaths_pt, self.recovered_pt], axis=1, join='outer')
		self.result_pt = self.result_pt.reset_index()
		self.result_dict = self.result_pt.to_dict(orient='index')
		self.list_pt = [ v for v in self.result_dict.values() ]
		
		# End My Code

		logger.info("Data Model built.")

	def getConfirmedListings(self):
    		return json.dumps(self.confirmed_dict, indent=2)
	
	def getDeathListings(self):
    		return json.dumps(self.death_dict, indent=2)

	def getRecoveredistings(self):
    		return json.dumps(self.recovered_dict, indent=2)

	def getCountryListining(self):
			return self.list_pt
	
