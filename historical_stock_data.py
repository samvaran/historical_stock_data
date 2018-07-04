import pandas as pd
import datetime
import quandl

# Created by Samvaran Sharma - July 3, 2018
# 0) Ensure pandas and quandl are both installed (run 'pip install pandas' and 'pip install quandl' in command line if not)
# 1) Sign up for a Quandl account and set your API key
# 2) Set the list of symbols you want to download (or download the default S&P 500 by using the included csv)
# 3) Run 'python historical_stock_data.py' in the command line

YOUR_API_KEY = '<your API key>' #Replace this with your Quandl API key here
SYMBOL_LIST = 'snp500_symbols.csv' #Replace this with a list of strings of ticker symbols or the filename of a different csv
OUTPUT_CSV = 'historical_stock_data.csv' #Output csv filename
START_DATE = datetime.date(2000, 1, 1) #Start date for data you want to fetch
END_DATE = datetime.date.today() #End date for data you want to fetch

quandl.ApiConfig.api_key = YOUR_API_KEY
if type(SYMBOL_LIST) == type('string'):
	SYMBOL_LIST = pd.read_csv(SYMBOL_LIST)
	SYMBOL_LIST = [x[0] for x in SYMBOL_LIST.values]

print('\nconnecting to Quandl with your API key ' + YOUR_API_KEY + '...')
print('fetching historical stock data for ' + str(len(SYMBOL_LIST)) + ' symbols: ')

all_data = []
for sym in SYMBOL_LIST:
	print(sym + '...')
	query = 'WIKI/' + sym
	try:
		data = quandl.get(query, 
			              returns='pandas', 
			              start_date=START_DATE,
			              end_date=END_DATE,
			              collapse='daily',
			              order='asc')
		data.insert(0, 'Symbol', data.shape[0] * [sym])
		all_data.append(data)
	except Exception as ex:
		print('   query for ' + sym + ' FAILED: ' + str(ex))
print('   ...complete!')

print('\nconcatenating data...')
all_data = pd.concat(all_data)
all_data.rename(columns=lambda x: x.replace('.',''), inplace=True)
all_data.rename(columns=lambda x: x.replace('-',''), inplace=True)
all_data.rename(columns=lambda x: x.replace(' ',''), inplace=True)
print('   ...complete!')

print(' ')
print(all_data)

print('\nsaving data to csv...')
all_data.to_csv(OUTPUT_CSV)
print('   ...complete!')