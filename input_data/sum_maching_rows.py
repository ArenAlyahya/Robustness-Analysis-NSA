
from cmath import nan
from email import header
import numpy as np
import string
from datetime import date

import pandas as pd



#DATA 1

#data = pd.read_csv('../../input_data/cases-brazil-cities-time_till_Sept_2nd_2020.csv', delimiter=',')
data = pd.read_csv('T_T100D_MARKET_US_CARRIER_ONLY.csv', delimiter=',', header=None)

print(len(data))

# Group by 'Category' and sum 'Amount'
data = data.groupby([0,1,2,3])[4].mean().reset_index()

data.to_csv('processed_T_T100D_MARKET_US_CARRIER_ONLY.csv', index=False, header=False)


data = pd.read_csv('state_to_state_data.csv', delimiter=',', header=None)

print(len(data))

# Group by 'Category' and sum 'Amount'
data = data.groupby([0,1,2,3])[4].mean().reset_index()

data.to_csv('processed_state_to_state_data2023.csv', index=False, header=False)


data = pd.read_csv('State_ID.csv', delimiter=',', header=None)

print(len(data))


data = data.drop_duplicates()


data = data.sort_values(by=[0])

data.to_csv('processed_State_ID.csv', index=False, header=False)



'''
cases_per_day['date'] = pd.to_datetime(cases_per_day['date'])
cases_per_day['date'] = cases_per_day['date'].dt.strftime('%Y/%m/%d')
print(cases_per_day.head())
cases_per_day.to_csv('cases_per_day.csv', index=False, header=False)

'''

