from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

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

abspath = os.path.abspath(os.getcwd())
path = str(abspath)

def pctsmokercorrelationsvis(frame, features):
    spr = pd.DataFrame()
    spr['feature'] = features
    spr['spearman'] = [frame[f].corr(frame['% Smokers'], 'spearman') for f in features]
    spr = spr.sort_values('spearman')
    plt.figure(figsize=(6, 0.25*len(features)))
    sns.barplot(data=spr, y='feature', x='spearman', orient='h')
    plt.show()

def correlationmatrixvis(frame):
    sns.heatmap(frame[frame.columns[list(range(1, frame.shape[0]))].tolist()], yticklabels=frame.columns.tolist()[1:])
    plt.show()
