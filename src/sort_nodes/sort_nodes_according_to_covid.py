from cmath import nan
import numpy as np
import string
from datetime import date

import pandas as pd





########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
codes = np.genfromtxt(in_files.get_codes_file_name())
##############################################

relative_path = '../../results/sort_nodes_covid-19/'


print('SORT COVID-19 CASES')


file_cities = open(relative_path + 'sorted_covid_cases_by_cities.csv', 'w')
file_cities_BRWN = open(relative_path + 'sorted_covid_cases_by_cities_BRWN.csv', 'w')
file_states = open(relative_path + 'sorted_covid_cases_by_states.csv', 'w')
file_cities_SP = open(relative_path + 'sorted_covid_cases_by_cities_SP.csv', 'w')
file_cities_MG = open(relative_path + 'sorted_covid_cases_by_cities_MG.csv', 'w')

file_cities_US = open(relative_path + 'sorted_covid_cases_by_cities_US.csv', 'w')

#file_cases_per_day = open(relative_path + 'cases_per_day_US.csv', 'w')


#file_cases_per_day = open(relative_path + 'cases_per_day.csv', 'w')


#data = pd.read_csv('../../input_data/cases-brazil-cities-time_till_Sept_2nd_2020.csv', delimiter=',')
data = pd.read_csv('../../input_data/us-counties-2020.csv', delimiter=',')



#data['fips'] = np.where((data['state'] == "Northern Mariana Islands") & (((pd.isna(data['fips'])) | ((data['county'] == "Unknown") ))), 69, data['fips'])
data['fips'] = np.where((data['state'] == "New York") & pd.isna(data['fips']), 36, data['fips'])
#data['fips'] = np.where((data['state'] == "New York") & pd.isna(data['fips']), 36, data['fips'])



indices_to_drop = data[(data['fips'] == 69) | (data['state'] == "Northern Mariana Islands")|(data['state'] == 'District of Columbia')].index

data = data.drop(indices_to_drop)

data.to_csv('processed_us-counties-2020.csv', index=False)



# Group by 'Category' and sum 'Amount'
cases_per_day = data.groupby('date').agg({'cases':['sum']}).reset_index()
cases_per_day['date'] = pd.to_datetime(cases_per_day['date'])
cases_per_day['date'] = cases_per_day['date'].dt.strftime('%Y/%m/%d')
cases_per_day.to_csv(relative_path + 'cases_per_day.csv', index=False, header=False)



data_ = data.to_numpy()


sorted_covid_cases_by_cities = []
#sorted_covid_cases_by_cities_BRWN = []
#sorted_covid_cases_by_states = []
#sorted_covid_cases_by_cities_SP = []
#sorted_covid_cases_by_cities_MG = []

sorted_covid_cases_by_cities_US = []
sorted_covid_cases_by_states = []



first_date = date(2020, 1, 21) 


#northern_states = [12,16,13,15,11,14,17] # North


#preprocess data of cases-brazil-cities-time_till_Sept_2nd_2020
for ln in data_: #delay_lines:

	#print(ln)

	date_str = ln[0].strip().split('-')

	year = int(date_str[0])
	month = int(date_str[1])
	day = int(date_str[2])
	date_now = date(year,month,day)

	date_str = str(date_str[0]) + '/' + str(date_str[1]) + '/' + str(date_str[2])

	#if(ln[3] == 'TOTAL'):
	#	file_cases_per_day.write(str(date_str) + ';' + str(ln[9]) + '\n')
	#else:
	
	if  np.isnan(ln[3]):
		continue

	code = int(ln[3])




	
	# not a state
	if(code > 80):
		# States (converting to state code)
		code_state = int(int(code) / int(1000))

		#print(code_state)
				
	# Cities
	if(code not in sorted_covid_cases_by_cities):
		if(code in codes):
			sorted_covid_cases_by_cities.append(code)
			file_cities.write( str(code) + ';' + str(ln[1]) + ';' + str(ln[2]) + ';' + str((date_now-first_date).days) + ';' + str(ln[0]) + '\n')
			file_cities_US.write( str(code) + ';' + str(ln[1]) + ';' + str(ln[2]) + ';' + str((date_now-first_date).days) + ';' + str(ln[0]) + '\n')

	'''
					
					if(code_state not in northern_states):
						sorted_covid_cases_by_cities_BRWN.append(code)
						file_cities_BRWN.write(str(code) + ';' + str(ln[4].split('/')[0]) + ';' + str(ln[3]) + ';' + str((date_now-first_date).days) + ';' + str(ln[1]) + '\n')
					

					if( (code_state == 35) and (code not in sorted_covid_cases_by_cities_SP)):
						sorted_covid_cases_by_cities_SP.append(code)
						file_cities_SP.write(str(code) + ';' + str(ln[4].split('/')[0]) + ';' + str(ln[3]) + ';' + str((date_now-first_date).days) + ';' + str(ln[1]) + '\n')

					if( (code_state == 31) and (code not in sorted_covid_cases_by_cities_MG)):
						sorted_covid_cases_by_cities_MG.append(code)
						file_cities_MG.write(str(code) + ';' + str(ln[4].split('/')[0]) + ';' + str(ln[3]) + ';' + str((date_now-first_date).days) + ';' + str(ln[1]) + '\n')
	'''

	# Include state
	if(int(code_state) not in sorted_covid_cases_by_states):
		sorted_covid_cases_by_states.append(int(code_state))
		file_states.write(str( int(code_state) ) + ';' + str(ln[1]) + ';' + str(ln[2]) + ';' + str((date_now-first_date).days) + ';' + str(ln[0]) + '\n')




#file_cases_per_day.close()
file_cities.close()
file_cities_BRWN.close()
file_states.close()
file_cities_SP.close()
file_cities_MG.close()