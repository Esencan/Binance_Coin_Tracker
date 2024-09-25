#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

22 Eylül 2024,
720 günlük haftalık periyoda göre dönen veri sorucunda çıkan destek direç çizgisi 
altında kalan coinleri tarayan bir script.


@author: Emre ESENCAN
"""
import numpy as np
from binance import Client
import pandas as pd


class Find_Coin:

    client = None
    server_time = None
    ticker = None

    

    def __init__(self):
        '''
        Binance Server İle Bağlantı
        '''

        self.client = Client(None, None)
        self.titles = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
          'quo_ass_vol', 'num_of_tra', 'tbbav', 'tbqav', 'ignore']

    def get_data(self, symbol, period, time_interval):
        """

        @param symbol: coin ismi ör: XLMUSDT
        @param period: 1h, 1w gibi periyodalr
        @param time_interval: zaman aralığı
        @return: dataframe
        """
        data = self.client.get_historical_klines(symbol, period, time_interval)
        df = pd.DataFrame(data)
        df.columns = self.titles
        df= df.iloc[:,:6]
        

        df['Tarih_Zaman'] = pd.to_datetime(df['open_time'], unit='ms')
        df = df.astype({'open':'float',
                        'high': 'float',
                         'low': 'float',
                         'close': 'float',
                         'volume': 'float'
                         })
        return df

    def lse(self, x, y):
        """
        @param x: open_time değerleri
        @param y: close coin değerleri
        @return:
        """
        # En küçük kareler yöntemi ile doğru parametrelerini hesapla
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return m, c

    def trand_band(self, close, open):
        """
        @param close: ilgili aralığın kapanış değerleri
        @param open: ilgili aralığın açılış değerleri
        @return:
            value: lse'e göre çıkan doğrunun son değeri
            direnc: oluşan doğrunun üzerine std eklenmesi
            destek: oluşan doğrudan std çıkartılması
        """
        m,c = self.lse(open, close)
        value = m * np.array(open) + c

        # Standart sapma hesaplama
        residuals = np.array(close) - (m*np.array(open) + c)
        std_dev = np.std(residuals)

        # Trend doğrusunun üst ve alt bant değerleri
        direnc = m * np.array(open) + c + std_dev
        destek = m * np.array(open) + c - std_dev

        return value, direnc, destek


    def run(self, symbol, period, time_interval):

        data = self.get_data(symbol, period, time_interval)
        value, direnc, destek = self.trand_band(data['close'], data['open_time'])

        return value[-1], direnc[-1], destek[-1], data['close'].iloc[-1]

