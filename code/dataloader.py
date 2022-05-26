# loads and modifies data in cold storage

import pandas as pd
import numpy as np
import os
from pathlib import Path

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'

states_lst = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

relevantfeatures = ["State", "County", "Population", "% Smokers", "% Adults with Obesity", "Food Environment Index", "% Physically Inactive", "% With Access to Exercise Opportunities", 
"% Excessive Drinking", "% Driving Deaths with Alcohol Involvement", "Chlamydia Rate", "Teen Birth Rate", 
"% Uninsured", "Primary Care Physicians Rate", "Dentist Rate", "Mental Health Provider Rate",
"% With Annual Mammogram", "% Vaccinated", "% Fair or Poor Health", "% Low birthweight", "% Completed High School",
"% Some College", "% Unemployed", "% Children in Poverty", "Income Ratio", "Violent Crime Rate", "Social Association Rate",
"Average Daily PM2.5", "Injury Death Rate", "Presence of Water Violation", "% Severe Housing Problems", "% Drive Alone to Work",
"% Long Commute - Drives Alone", "% Less Than 18 Years of Age", "% 65 and Over", "% Black", "% Asian", "% Native Hawaiian/Other Pacific Islander",
"% American Indian & Alaska Native", "% Hispanic", "% Non-Hispanic White", "% Not Proficient in English", "% Homeowners", "% Broadband Access", 
"Firearm Fatalities Rate", "Crude Rate", "% Enrolled in Free or Reduced Lunch", "Segregation Index", "Median Household Income", "Average Grade Performance (Reading)", 
"Average Grade Performance (Math)", "High School Graduation Rate", "% Uninsured", "% Insufficient Sleep", "% Limited Access to Healthy Foods", "% Food Insecure", 
"% Adults with Diabetes", "% Frequent Mental Distress", "% Frequent Physical Distress", "Life Expectancy"]

path = parent_path + 'data/'

state_taxes_2017 = pd.read_csv(path + 'state_cigarette_rates_2017.csv')
state_taxes_2018 = pd.read_csv(path + 'state_cigarette_rates_2018.csv')
state_taxes_2019 = pd.read_csv(path + 'state_cigarette_rates_2019.csv')
state_taxes_2020 = pd.read_csv(path + 'state_cigarette_rates_2020.csv')
state_taxes_2021 = pd.read_csv(path + 'state_cigarette_rates_2021.csv')
#print(state_taxes_2017.head())

yearly_tax_lst = [state_taxes_2017, state_taxes_2018, state_taxes_2019,
                  state_taxes_2020, state_taxes_2021]

tax_lst = []
for x in yearly_tax_lst:
    x_fixed = pd.DataFrame(np.concatenate((x.iloc[:, 0:2].values,
                           x.iloc[:, 4:6].values)),
                           columns=['State', 'Tax Rate'])
    x_fixed = x_fixed.dropna(axis=0)
    x_dict = x_fixed.set_index('State').to_dict()
    tax_lst.append(x_dict)

state_dict = {}
for state in states_lst:
    state_data = path + states[state] + '.csv'
    state_data2 = path + states[state] + '2.csv'
    state_file = pd.read_csv(state_data)
    state_file2 = pd.read_csv(state_data2)
    state_file = state_file.rename(columns=state_file.iloc[0]).drop(state_file.index[0])
    state_file2 = state_file2.rename(columns=state_file2.iloc[0]).drop(state_file2.index[0])
    state_file = pd.concat((state_file2, state_file), axis=1)
    state_dict[state] = state_file
    print(state_file["Average Grade Performance"])
    for i, tax_year in enumerate(tax_lst):
        year = 2017 + i
        state_name = states[state]
        tax_rate = tax_year['Tax Rate'][state_name]
        state_dict[state]["cig_tax_" + str(year)] = tax_rate
print(state_dict["AL"]["Average Grade Performance"])
