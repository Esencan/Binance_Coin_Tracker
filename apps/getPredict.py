#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI ile grafik oluşturma il ilgili yapılan çalışma

Emre ESENCAN
21 Eylül 2024

Arima modeli ile periyod kadar sonrası için öngörü hesapala işlemi
"""


from binance import Client
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA



class getPredict:

	def __init__(self):
		'''
		Binance Server İle Bağlantı
		'''

		self.client = Client(None, None)
		self.titles = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
		  'quo_ass_vol', 'num_of_tra', 'tbbav', 'tbqav', 'ignore']

	def get_data(self, symbol, period, date1, date2):
		"""

		@param symbol: coin ismi ör: XLMUSDT
		@param period: 1h, 1w gibi periyodalr
		@param time_interval: zaman aralığı
		@return: dataframe
		"""
		data = self.client.get_historical_klines(symbol, period, date1, date2)
		df = pd.DataFrame(data)
		df.columns = self.titles
		df= df.iloc[:,:6]

		#===> Tarihi x ekseninde gözükecek şekilde ayarlamalıyı
		# Unix zaman damgasını datetime nesnesine dönüştürme
		df['Tarih_Zaman'] = pd.to_datetime(df['open_time'], unit='ms')

		df = df.astype({'open':'float',
		                'high': 'float',
		                 'low': 'float',
		                 'close': 'float',
		                 'volume': 'float'
		                 })
		ticker = self.client.get_ticker(symbol=symbol)
		predict = self.model_ARIMA(df['close'], 1)
		return predict.iloc[0], ticker['lastPrice']


	def model_ARIMA(self, close, predict_step):

		# fit model
		model = ARIMA(close, order=(5, 1, 0))
		model_fit = model.fit()
		predict = model_fit.forecast(predict_step)
		return predict