from forex_python.converter import CurrencyRates
from forex_python.converter import CurrencyCodes
import datetime as dt
import pandas as pd

def get_currencies_range(since_date, to_date, step = 1):
	c = CurrencyRates()
	currencies, dates = [], []
	time_delta = dt.timedelta(days = step)
	index = 0
	while since_date < to_date:
		try:
			currency = c.get_rates("USD", since_date)
			currencies.append(currency)
			dates.append(since_date)
			since_date = since_date + time_delta
			print(index, currencies[index], since_date, to_date)
			index += 1
		except:
			pass
	return currencies, dates

def currencies_to_df(currencies, dates):
	df = pd.DataFrame()
	for i in range(len(currencies)):
		aux_dict = dict(map(lambda kv: (kv[0], [kv[1]]), currencies[i].items()))
		dfaux = pd.DataFrame(aux_dict, index = pd.Index([dates[i]]))
		df = pd.concat(objs = [df, dfaux], sort = True)
	return df

def append_symbols_names(dataframe):
	symbols = dataframe.columns
	cc = CurrencyCodes()
	named_symbols = []
	for symbol in symbols:
		name = ""
		try:
			name = cc.get_currency_name(symbol)
		except:
			pass
		if name != None:
			named_symbols.append(str(symbol) + " " + str(name))
		else:
			named_symbols.append(str(symbol))
	dataframe.columns = named_symbols
	return dataframe

def currency_range_csv(since, to):
	for i in range(since, to):
		d1 = dt.datetime(i, 1, 1)
		currencies, dates = get_currencies_range(d1, dt.datetime(i + 1, 1, 1))
		df = currencies_to_df(currencies, dates)
		df = append_symbols_names(df)
		df_aux = pd.read_csv("USD_currency.csv", index_col = 0)
		df = pd.concat(objs = [df_aux, df], sort = True)
		df.to_csv("USD_currency.csv", mode = "w")

if __name__ == "__main__":
	currencies, dates = get_currencies_range(
		dt.datetime(1999, 1, 4), dt.datetime(2000, 1, 1))
	df = append_symbols_names(currencies_to_df(currencies, dates))
	df.to_csv("USD_currency.csv", mode = "w")
	currency_range_csv(2000, 2021)

	#plt.plot(dates, currencies)
	#plt.title("USD vs MXN")
	#plt.ylabel("Currency")
	#plt.xlabel("Date")
	#plt.grid(True)
	#plt.show()