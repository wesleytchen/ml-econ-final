import pandas as pd
import numpy as np
import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'

final_df = pd.read_csv(parent_path + "FinalDF.csv")
adj_counties = pd.read_csv(parent_path + "AdjacentDelta.csv")

final_df['Presence of Water Violation'] = final_df['Presence of Water Violation'].str.replace('Yes','1')
final_df['Presence of Water Violation'] = final_df['Presence of Water Violation'].str.replace('No','0')
final_df['Presence of Water Violation'] = pd.to_numeric(final_df['Presence of Water Violation'])

population = final_df["Population"] / final_df["Population"].max()
print(population)
final_df = final_df.select_dtypes(exclude=['object'])
features_df = final_df.drop(columns=["% Smokers", "Population", "Life Expectancy"])
scaler = StandardScaler()
scaler.fit(features_df)
standardized_df = scaler.transform(features_df)
#print(standardized_df)
#print(np.shape(standardized_df))

median_income = final_df["Median Household Income"].median()
df_upper_income = final_df[final_df["Median Household Income"] >= median_income]
df_lower_income = final_df[final_df["Median Household Income"] < median_income]

median_edu = final_df["% Completed High School"].median()
df_upper_edu = final_df[final_df["% Completed High School"] >= median_edu]
df_lower_edu = final_df[final_df["% Completed High School"] < median_edu]

df_lst = [df_upper_income, df_lower_income, df_upper_edu, df_lower_edu]

# Adjacent counties regression

adj_counties = adj_counties.select_dtypes(exclude=['object'])
features_df2 = adj_counties.drop(columns=["% Smokers", "Life Expectancy"])
scaler = StandardScaler()
scaler.fit(features_df2)
standardized_df2 = scaler.transform(features_df2)
#print(standardized_df2)


