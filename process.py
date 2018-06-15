'''
DISCLAIMER: WATCH OUT FOR FILE AND COLUMN NAMES
'''

import csv
import json
import pandas as pd
import collections
import time

#start timer
start = time.time()

'''
find
ls - a sorted list from lowest to greatest, amount - the payment amount
'''
def find(ls, amount):
	l = len(ls)

	print amount
	#greater than the later
	if(amount >= ls[l - 1]):
		return ls[l - 1]
	elif(amount <= ls[0]):
		return ls[0]
	else:
		for i in range(l - 1):
			k = (ls[i] + ls[i + 1]) / 2.0
			if(amount <= k and amount >= ls[i]):
				return ls[i]
			elif(amount >= k and amount <= ls[i + 1]):
				return ls[i + 1]



'''
future_month
return string that is x month away from date, date is format 'm/d/y time'
'''
def future_month(date, x):
	date_l = list()
	#['month', 'day', 'year']
	date_l = date.split(' ')
	date_l = date_l[0].split('/')


	if((int(date_l[0]) + x) % 12 == 0):
		m = 12
	else:
		m = (int(date_l[0]) + x) % 12

	if(int(date_l[1]))>=28 and m == 2:
		d=28
	elif int(date_l[1])==31 and (m == 4 or m == 6 or m == 9 or m == 11):
		d = 30
	else:
		d = date_l[1]

	y = int(date_l[2]) + ((int(date_l[0]) + x - 1) / 12)

	seq = (str(m), str(d), str(y))
	k = '/'.join(seq)
	return k

'''
plan_data
dictionary key is payment amount, value is payment period
list contains all the payment amounts sorted lowest to highest
plans is the dataframe of plans
'''
def plan_data(dictionary, l, plans):
	#create dictionary and list to match amount from payment data with plans from payment plans
	for index, row in plans.iterrows():
		x = row.loc['Payment Amount']
		dictionary[x] = row.loc['Plan Duration (Months)']
		#add the payment amounts to list, used to find payment
		l.append(x)

	#sort list
	l.sort()

	print l

	return dictionary, l

def main(data, plans, destination): ##The main function that

	# ***CHANGE THIS TO LOCATION OF PAYMENT TRANSACTION CSV FILE***
	df = pd.read_csv(data)

	# ***CHANGE THIS TO LOCATION OF PAYMENT PLAN CSV FILE***
	plans = pd.read_csv(plans)

	'''
	PRINT TESTS
	print('Here are the column names for payment transaction file, make sure they match with the names below lmao\n')
	print(list(df.columns.values))
	print('\n')

	print('Here are the column names for payment plan file, make sure they match with the names below lmao\n')
	print(list(plans.columns.values))
	print('\n')
	'''

	d = {}
	ls = list();

	dictionary, l = plan_data(d, ls, plans)

	#open and modify return file
	f = csv.writer(open(destination, "wb+"))
	f.writerow(["Customer ID", "Date", "Amount"])

	#iterate over each data row and compute new file
	for index, row in df.iterrows():
		print(row)
		idd = row.loc["Customer ID"]
		created = row.loc["Created (UTC)"]
		amount = row.loc['Amount']
		#fee = row.loc["Fee"]
		#refunded = row.loc["Amount Refunded"]
		#status = row.loc["Status"]

		payment_key = find(l, amount)
		payment_period_total = dictionary[payment_key]

		#new_fee = fee / float(payment_period_total)
		new_amount = float(amount) / float(payment_period_total)
		#new_refunded = refunded / float(payment_period_total)
		payment_period_total = int(payment_period_total)


		for i in range(0, payment_period_total):
			new_date_charged = future_month(created, i)
			f.writerow([idd,
				new_date_charged,
				new_amount,
				])


	#end timer
	end = time.time()

	print(end - start)


if __name__ == "__main__":
	prefix = "PA"
	main(prefix+'data.csv', prefix+'plans.csv', prefix+"process_result.csv")
