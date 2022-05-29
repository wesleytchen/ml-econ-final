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

state_taxes = pd.read_csv(path + 'cigarette_tax_rates.csv')
state_taxes["Cig Tax Rate"] = state_taxes["tax"] / state_taxes["cost"]
state_taxes = state_taxes.set_index("State")


state_dict = {}
for state in states_lst:
    state_data = path + states[state] + '.csv'
    state_data2 = path + states[state] + '2.csv'
    state_file = pd.read_csv(state_data)
    state_file2 = pd.read_csv(state_data2)
    state_file = state_file.rename(columns=state_file.iloc[0]).drop(state_file.index[0])
    state_file2 = state_file2.rename(columns=state_file2.iloc[0]).drop(state_file2.index[0])
    state_file = pd.concat((state_file2, state_file), axis=1)
    state_file["Cig Tax Rate"] = state_taxes.loc[states[state]]["Cig Tax Rate"]
    state_dict[state] = state_file
    #print(state_file["Cig Tax Rate"])
