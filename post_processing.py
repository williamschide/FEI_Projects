import csv
import json
import pandas as pd
import collections
import time
from process import *

def post_processing(input, output):
    #Reading in dataframe sorted by ID
    df = pd.read_csv(input)
    df['Date'] = df['Date'].astype('datetime64[ns]')
    df.sort_values(by = ['Customer ID', 'Date'], inplace = True, ascending=[True, True])
    length = len(df)
    #Establishing the columns I will populate
    df["Churned Value"] = None
    df["Churned Customer"] = None
    df["New Revenue"] = None
    df["New Customers"] = None
    df["Upgrade Value"] = None
    df["Net Churn"] = None
    df["Customer (Metric)"] = None

    #Initalizing first entry to make loop work properly

    df.iat[0,3] = 0
    df.iat[0, 4] = 0
    df.iat[0, 5] = df.iat[0,2]
    df.iat[0, 6] = 1
    df.iat[0, 7] = 0
    df.iat[0, 8] = 0
    df.iat[0, 9] = 1
    #Doing the rest of the entries
    print(df.dtypes)
    for i in range(1, length):
        #Customer metric
        df.iat[i, 9] = 1
        #New/Churn
        if df.iat[i,0] != df.iat[i-1,0] and df.iat[i,1].month !=df.iat[i-1,1].month+1:
            df.iat[i-1, 3] = df.iat[i-1,2]
            df.iat[i-1, 4] = 1
            df.iat[i, 5] = df.iat[i,2]
            df.iat[i, 6] = 1
        else:
            df.iat[i-1, 3] = 0
            df.iat[i-1, 4] = 0
            df.iat[i, 5] = 0
            df.iat[i, 6] = 0

        if df.iat[i-1,3] and df.iat[i-1,5]:
            df.iat[i-1,3] = 0
            df.iat[i-1,4] = 0
            df.iat[i-1,5] = 0
            df.iat[i-1,6] = 0

        #Upgrade
        if df.iat[i,0] == df.iat[i-1,0] and df.iat[i,2] != df.iat[i-1,2]:
            df.iat[i, 7] = df.iat[i-1, 2] - df.iat[i,2]
        else:
            df.iat[i, 7] = 0
        #Net Churn
        df.iat[i-1, 8] = df.iat[i-1, 3] + df.iat[i-1, 7]
        print(df[i-1:i])

    df.to_csv(output)


if __name__ == "__main__":
    prefix = "PA"
    #main(prefix+'data.csv', prefix+'plans.csv', prefix+"process_result.csv")
    post_processing(prefix+"process_result.csv", prefix+"post_process_result.csv")
