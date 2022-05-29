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

population = np.log(final_df["Population"]) / np.log(final_df["Population"].max())
print(population)
final_df = final_df.select_dtypes(exclude=['object'])
final_df = final_df.drop(columns=["Population", "Life Expectancy"])
feature_cols = final_df.columns
std_final_df = pd.DataFrame(StandardScaler().fit_transform(final_df), columns=feature_cols)
std_final_df["Population"] = population
#scaler = StandardScaler()
#scaler.fit(features_df)
#std_features_array = scaler.transform(features_df)
#print(np.shape(standardized_df))
print(std_final_df)


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


