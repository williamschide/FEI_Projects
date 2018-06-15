import csv
import json
import pandas as pd
import collections
from process import *
from post_processing import post_processing
import sys


#Goal: Take this data frame and turn it into a summary data frame by Months

#Reading in the prefix
prefix = sys.argv[1]
#Argument should be true if customer ID is string, else false if string
if sys.argv[2] == "String":
    option = True
else:
    option = False
main(prefix+'data.csv', prefix+'plans.csv', prefix+"process_result.csv")
post_processing(prefix+"process_result.csv", prefix+"post_process_result.csv")



#Columns I want: MRR, change in MRR (as a %), Customer Churn, New Customers, Customers
#Churned customers, Net Churned (look into what this means), ask Jonathan for more

#Creating the groupings
df = pd.read_csv(prefix+"post_process_result.csv", index_col = "Date")
df.index =  pd.to_datetime(df.index, format='%Y/%m/%d') #Setting date index
groupings = df.groupby(pd.Grouper(freq='M')) #Creating month groupings

#Can get any aggregate in the way below, now figure out a way to write it into the CSV
#Perhaps you can convert the groups directly to CSV
aggregates = groupings.sum()


#Comment this in or out depending if Customer ID is a name or number, on if name, off if number
if option:
    aggregates.insert(1, "Customer ID", 1)


#Adding new columns
aggregates["ARPU"] = None
aggregates["Customer Churn Rate"] = None
aggregates["LTV"] = None
aggregates["Net Churn Rate"] = None
aggregates["MRR"] = None
'''Column guide:
0-Null
1-ID
2-Amount
3-Churned value
4-Churned customers
5-New Revenue
6-New customers
7-Upgrade value
8-Net churn
9-Customer Metric
10-ARPU
11-Customer Churned Rate
12-LTV
13-Net Churn rate
14-MRR
'''

#Initalizing first entry to make loop work properly
print(aggregates.columns)
aggregates.iat[0, 10] = aggregates.iat[0,2] / aggregates.iat[0,9]
aggregates.iat[0, 11] = 0
aggregates.iat[0, 12] = 0
aggregates.iat[0, 13] = 0
aggregates.iat[0, 14] = aggregates.iat[0,5]
length = len(aggregates)

#Loop to populate new entries
for i in range(1, length):
    #ARPU
    aggregates.iat[i, 10] = aggregates.iat[i, 2]/aggregates.iat[i, 9]
    #Customer Churn rate
    aggregates.iat[i, 11] = aggregates.iat[i, 4]/aggregates.iat[i-1, 9]
    #LTV
    aggregates.iat[i, 12] = aggregates.iat[i, 10]/aggregates.iat[i, 11]
    #MRR
    aggregates.iat[i, 14] = aggregates.iat[i-1, 2]-aggregates.iat[i-1, 3]-aggregates.iat[i-1, 7]
    #Net Churn Rate
    aggregates.iat[i, 13] = aggregates.iat[i, 8]/aggregates.iat[i-1, 14]


#Saving what I want

result = aggregates[['Amount','ARPU','Churned Customer', "Customer (Metric)", "New Customers", "Customer Churn Rate", "LTV", "MRR", "Net Churn Rate"]].copy()
#Normalizing percentages, renaming columns
result['Net Churn Rate'] = result['Net Churn Rate'].apply(lambda x: x*100)
result['Customer Churn Rate'] = result['Customer Churn Rate'].apply(lambda x: x*100)
result.columns = ['Total Revenue', 'ARPU', "Cancellations", "Customers", "New Customers", "Customer Churn Rate (%)", "LTV ($)", "MRR ($)", "Net Churn Rate (%)"]
print(result)
#Saving to CSV
result.to_csv(prefix+"SaaS_Metrics.csv")
