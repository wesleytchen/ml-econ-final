from operator import index
import county_adjacency as ca
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import re
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
"% Adults with Diabetes", "% Frequent Mental Distress", "% Frequent Physical Distress", "Life Expectancy", "Cig Tax Rate"]

abspath = os.getcwd()
parent_path = str(abspath)

def editcolname(filename):
    # To be used on unedited data to make column headers accurate
    df = pd.read_csv(filename)

    if "2" in filename:
        for i in range(df.columns.tolist().index("Uninsured adults"), df.columns.tolist().index("Uninsured children")):
            df.iat[0, i] += " (Adults)"
        for i in range(df.columns.tolist().index("Uninsured children"), df.columns.tolist().index("Other primary care providers")):
            df.iat[0, i] += " (Children)"

        for i in range(df.columns.tolist().index("Reading scores"), df.columns.tolist().index("Math scores")):
            df.iat[0, i] += (" (Math)")
        for i in range(df.columns.tolist().index("Math scores"), df.columns.tolist().index("Median household income")):
            df.iat[0, i] += (" (Reading)")

    colnames = df.iloc[0]
    df.columns = colnames
    df.drop(index=0, inplace=True)

    df.to_csv(filename)

def cleanratio(filename):
    # Reformats ratios, as they appear as timestamps if unedited
    df = pd.read_csv(filename)

    for index1 in range(len(df.columns)):
        if "Ratio" in df.columns.tolist()[index1]:
            for index2 in range(df.shape[0]):
                value = str(df.iat[index2, index1])
                df.iat[index2, index1] = value.split(':')[0]
                
    
    df.to_csv(filename)

def concatenator(f1, f2):
    # Concatenates "State" and "State2" files
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)

    df = pd.concat([df1, df2], axis=1)
    df = df.loc[:,~df.columns.duplicated()]

    return df


def createfinaldf():
    # Initialize final dataframe
    df = pd.DataFrame()
    state_taxes = pd.read_csv(parent_path + '\\data\\cigarette_tax_rates.csv')
    state_taxes["Cig Tax Rate"] = state_taxes["tax"] / state_taxes["cost"]
    state_taxes = state_taxes.set_index("State")
    # Iterate through, clean, and concatenate dfs along rows

    for key in states.keys():
        path1 = parent_path + f"\\data\\{states[key]}.csv"
        path2 = parent_path + f"\\data\\{states[key]}2.csv"

        statefinal = concatenator(path1, path2)
        statefinal["Cig Tax Rate"] = state_taxes.loc[states[key]]["Cig Tax Rate"]
        df = pd.concat([df, statefinal], axis=0, ignore_index=True)
        # Once cigtax function exists, append to each df at this point

    # Keep only relevant features
    df = df[relevantfeatures]
    

    df.to_csv(parent_path + "\\TrimmedData.csv")

    return df
    
def createcorrmatrix(frame):
    # Drop columns with too many missing items/incompatible data types, remove counties with null values
    frame.drop(columns=["Firearm Fatalities Rate", "Crude Rate", "High School Graduation Rate", "Average Grade Performance (Reading)",
    "Average Grade Performance (Math)", "Segregation Index", "% Uninsured"], inplace=True)
    
    frame['Presence of Water Violation'] = frame['Presence of Water Violation'].str.replace('Yes','1')
    frame['Presence of Water Violation'] = frame['Presence of Water Violation'].str.replace('No','0')
    frame['Presence of Water Violation'] = pd.to_numeric(frame['Presence of Water Violation'])

    frame.dropna(inplace=True)

    # Fill in correlation values
    data = frame.drop(columns=["State", "County", "Population"]).to_numpy().T
    print(data)
    covmatrix = np.cov(data)
    df = pd.DataFrame(covmatrix, columns=frame.columns.tolist()[3:])

    # Write to CorrMatrix and FinalDF
    df.to_csv(parent_path + "\\CovMatrix.csv")
    frame.to_csv(parent_path + "\\FinalDF.csv")

    return frame

def pctsmokercorrelationsvis(frame):
    spr = pd.DataFrame()
    features = frame.columns
    spr['feature'] = features
    spr['spearman'] = [frame[f].corr(frame['% Smokers'], 'spearman') for f in features]
    spr = spr.sort_values('spearman')
    plt.figure(figsize=(6, 0.25*len(features)))
    sns.barplot(data=spr, y='feature', x='spearman', orient='h')
    plt.show()

def correlationmatrixvis(frame):
    sns.heatmap(frame[frame.columns[list(range(1, frame.shape[0]))].tolist()], yticklabels=frame.columns.tolist()[1:])
    plt.show()

def getinterstateadj():
    counties = ca.supported_areas()
    isa = []

    for county in counties:
        state = county.split(", ")[1]
        adjacencies = ca.get_neighboring_areas(county)

        for adjacency in adjacencies:
            adjacencystate = adjacency.split(", ")[1]
            if adjacencystate != state:
                propercounty = tuple(re.split(" County, | Parish, |, ", county))
                properadj = tuple(re.split(" County, | Parish, |, ", adjacency))
                isa.append([propercounty, properadj])
    
    return isa

def adjdelta(frame):
    '''
    Generates a dataframe of the category-wise differences between all adjacent cross-state county
    pairs in the US. 
    '''
    adjacencypairs = getinterstateadj()
    result = pd.DataFrame(columns=["County Pair"] + frame.columns.tolist()[3:])

    for pair in adjacencypairs:
        county1 = pair[0][0]
        county2 = pair[1][0]

        row1 = frame.loc[frame["County"] == county1]
        row1 = row1.loc[row1["State"] == states[pair[0][1]]].values.flatten().tolist()
        row2 = frame.loc[frame["County"] == county2]
        row2 = row2.loc[row2["State"] == states[pair[1][1]]].values.flatten().tolist()

        trim1 = np.array(row1[3:])
        trim2 = np.array(row2[3:])

        if trim1.shape[0] == trim2.shape[0] == (len(frame.columns) - 3):
            finalrow = [f"{county1}/{county2}"] + np.subtract(trim1, trim2).tolist()
            result.loc[len(result.index)] = finalrow

    result.to_csv(parent_path + "\\AdjacentDelta.csv")

def normmeans(frame):

    normalfits = []
    for column in frame.columns.tolist()[1:]:
        data = frame[column].to_numpy()

        mu, std = norm.fit(data)
        normalfits.append(mu)

    return normalfits

def DGP():
    frame = pd.read_csv(parent_path + "\\FinalDF.csv")
    frame.drop(columns=["State", "County", "Population"], inplace=True)
    means = np.array(normmeans(frame))
    cov = pd.read_csv(parent_path + "\\CovMatrix.csv").to_numpy()[:, 1:]

    data = np.random.multivariate_normal(means, cov, size=cov.shape[0])
    
    resultframe = pd.DataFrame(data, columns=frame.columns.tolist()[1:])

    return resultframe

final = createfinaldf()
corrdata = createcorrmatrix(final)