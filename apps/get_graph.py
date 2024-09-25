#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GUI ile grafik oluşturma il ilgili yapılan çalışma
19 Eylül 2024
"""



import numpy as np
import pandas_ta as ta
import matplotlib.pyplot as plt
from binance import Client
import pandas as pd
import datetime

class getGraph:

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

    def get_server_time(self, format):
        """
        @param format: "%d-%m-%Y %H:%M:%S" şeklinde verilmeli
        @return:
        """
        time_res = self.client.get_server_time()  # Dönen değer dictinory formatında key 'serverTime'
        # Unix zamanını alıp başka bir değişkene atama
        unix_timestamp = time_res['serverTime'] / 1000  # Unix zaman damgasını saniye cinsine dönüştürüyoruz
        # Unix zaman damgasını datetime nesnesine dönüştürme
        dt_object = datetime.datetime.fromtimestamp(unix_timestamp)
        # Belirtilen formatta tarih ve saat bilgisini yazdırma
        server_time = dt_object.strftime(format)
        return server_time
        
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
        return df
    

    def calculate_sma(self, df, length):
        df['sma_50'] = ta.sma(df['close'], length=length)      
        return df
    
    def calculate_bbs(self, df):
        # Bollinger bantlarını hesaplayalım ve sonuçları yeni sütunlara ekleyelim
        bbs = ta.bbands(df['close'])
        df['bb_upper'] = bbs['BBU_5_2.0']
        df['bb_middle'] = bbs['BBM_5_2.0']
        df['bb_lower'] = bbs['BBL_5_2.0']
        return df

    def calculate_stochastic(self, data, stochrsi_period, stochrsi_k, stochrsi_d):

        # StochRSI hesaplama
        # stochrsi_period = 14
        # stochrsi_k = 3
        # stochrsi_d = 3

        stochrsi = ta.stochrsi(data['close'], length=stochrsi_period, k=stochrsi_k, d=stochrsi_d, append=True)
        data = pd.concat([data, stochrsi], axis=1)
        return data

    def draw_graph(self, data, time_label, title, indicators):

        plt.figure(figsize=(20,10), dpi=100)
        
        m, c= self.lse(data['open_time'], data['close'])

        # grafik çizimi
        plt.plot(data['Tarih_Zaman'], data['close'], color='blue', label=time_label)
        
        #SMA çizimi
        if indicators[2] == True:
            plt.plot(data['Tarih_Zaman'], data['sma_50'], color='orange', label='SMA-50')

        #Bollinger Bands Çizimi
        if indicators[1] == True:
            plt.plot(data['Tarih_Zaman'], data['bb_upper'], label='Üst Bollinger Bandı')
            plt.plot(data['Tarih_Zaman'], data['bb_middle'], label='Orta Bollinger Bandı')
            plt.plot(data['Tarih_Zaman'], data['bb_lower'], label='Alt Bollinger Bandı')

        # #Stochastik RSI çizimi
        #plt.plot(data['Tarih_Zaman'], data['STOCHRSIk_14_14_3_3'], label='StochRSI_k')
        #plt.plot(data['Tarih_Zaman'], data['STOCHRSId_14_14_3_3'], label='StochRSI_d')

        if indicators[0] == True:
            # Trend doğrusunu çizme
            plt.plot(data['Tarih_Zaman'], m*np.array(data['open_time']) + c, 'r', label='Trend Doğrusu')
            
            # Standart sapma hesaplama
            residuals = np.array(data['close']) - (m*np.array(data['open_time']) + c)            
            std_dev = np.std(residuals)
            
            # Trend doğrusunun üst ve alt bantlarını çizme
            plt.plot(data['Tarih_Zaman'], m*np.array(data['open_time']) + c + std_dev, color="green", label='Üst Bant')
            plt.plot(data['Tarih_Zaman'], m*np.array(data['open_time']) + c - std_dev, color="green", label='Alt Bant')
        
        plt.xticks(data['Tarih_Zaman'][::5], rotation=80)
        # move ticks
        plt.tick_params(axis='y', which='both', labelleft=False, labelright=True)
        plt.xlabel('Zaman')
        plt.ylabel('Coin Değeri')
        plt.title('Trend Doğrusu ve Bantlar ' + title)
        
        plt.grid(True)
        plt.legend()
        server_time = self.get_server_time("%d-%m-%Y-%H_%M_%S")

        #plt.savefig('graphs/'+ time_label + '_' +server_time+'_'+title, dpi=300)
        plt.show()
    
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

    def run(self, symbol, period, date1, date2, title, indicators):

        data = self.get_data(symbol, period, date1, date2)
        data = self.calculate_bbs(data)
        data = self.calculate_stochastic(data,14,3,3)
        data = self.calculate_sma(data, 20)

        self.draw_graph(data, symbol, title, indicators)
        return data
