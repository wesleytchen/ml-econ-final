import pandas as pd
import numpy as np
import os
from pathlib import Path
import cvxpy as cp
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

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

def shuffle_data(data, labels, p):
    indices = np.random.permutation(len(data))
    return data[indices], labels[indices], p[indices]

def split_data(data, labels, p):
    size = len(data)
    index_eighty = int(size*0.8)
    train_data = data[:index_eighty]
    train_labels = labels[:index_eighty]
    train_p = p[:index_eighty]
    test_data = data[index_eighty:]
    test_labels = labels[index_eighty:]
    test_p = p[index_eighty:]
    return train_data, train_labels, train_p, test_data, test_labels, test_p

#for params in params_lst:
X, IV, y, p = params_lst[0]

lams = np.linspace(0,2,10)
error_lst = []
for lam in lams:
    sum_error = 0
    for _ in range(10):
        X_s, IV_s, p_s = shuffle_data(X, IV, p)
        train_X, train_IV, train_p, test_X, test_IV, test_p = split_data(X_s, IV_s, p_s)
        B = cp.Variable((train_X.shape[1], 1))
        objective = cp.Minimize((train_p.T @ (train_IV - train_X @ B) ** 2) + lam * cp.norm1(B))
        constraints = []
        prob = cp.Problem(objective, constraints)
        prob.solve()
        betas = np.array(B.value)
        error = np.linalg.norm((test_IV - test_X @ betas))
        sum_error += error
    error_lst.append(sum_error / 10)
print(error_lst)



