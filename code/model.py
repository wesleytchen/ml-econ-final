import pandas as pd
import numpy as np
import os
from pathlib import Path
import cvxpy as cp
from sklearn.preprocessing import StandardScaler

abspath = os.path.abspath(os.getcwd())
finpath = Path(abspath).resolve().parent
parent_path = str(finpath) + '/'

final_df = pd.read_csv(parent_path + "FinalDF.csv")
adj_counties = pd.read_csv(parent_path + "AdjacentDelta.csv")
final_df["Population"] = np.sqrt(final_df["Population"]) / np.sqrt(final_df["Population"].max()) #Ask about specific transformation for weighting to use here

def standardize_df(df):
    df = df.select_dtypes(exclude=['object'])
    df = df.drop(columns=["Life Expectancy"])
    feature_cols = df.columns[2:]
    std_final_df = pd.DataFrame(StandardScaler().fit_transform(df.iloc[:, 2:]), columns=feature_cols)
    pop_df = df["Population"]
    return std_final_df, pop_df


median_income = final_df["Median Household Income"].median()
df_upper_income = final_df[final_df["Median Household Income"] >= median_income]
df_lower_income = final_df[final_df["Median Household Income"] < median_income]
#print(df_upper_income["Population"])
#print(df_lower_income.shape)

# Here, our dataframes are not the same shapes because % Completed High School has many values at the median,
# but the number of observations in the dataframes are 1197 for the upper bracket and 1209 for the lower bracket,
# which we found to be acceptable for running our regression analysis on
median_edu = final_df["% Completed High School"].median()
df_upper_edu = final_df[final_df["% Completed High School"] > median_edu]
df_lower_edu = final_df[final_df["% Completed High School"] <= median_edu]

# Adjacent counties regression

adj_counties = adj_counties.select_dtypes(exclude=['object'])
adj_counties = adj_counties.drop(columns=["Life Expectancy"])


# Standardizing values and creating all the matrices we need to run Lasso

df_lst = [final_df, df_upper_income, df_lower_income, df_upper_edu, df_lower_edu] #Want to add adj_counties to this list after Population column is added
params_lst = []
for frame in df_lst:
    std_frame, pop_df = standardize_df(frame)
    label_df = std_frame["% Smokers"]
    IV_df = std_frame["Cig Tax Rate"]
    features_df = std_frame.drop(columns=["% Smokers", "Cig Tax Rate"])
    p = np.array([pop_df]).T
    X = np.array(features_df)
    IV = np.array([IV_df]).T
    y = np.array([label_df]).T
    values = [X, IV, y, p]
    params_lst.append(values)
    print(y.shape)
    print(IV.shape)
    print(X.shape)
    print(p.shape)


for params in params_lst:
    X, IV, y, p = params
    lam = 0.02
    B = cp.Variable(X.shape[1])
    objective = cp.Minimize(cp.norm2(y - B @ X) ** 2 @ p + lam * cp.norm1(B))
    print(np.shape(B))



