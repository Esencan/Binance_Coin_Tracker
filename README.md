DESCRIPTION

EsencanCoinTracker simply fetches real-time data from Binance and can plot a graph for the desired coin. It can add indicators that are in the development and improvement stages to the plotted graph. It performs predictions for the next period based on the ARIMA forecasting model. Additionally, it lists coins suitable for purchase by analyzing all coins traded in the spot market on Binance or those you have prepared yourself.

FINDING COINS

Data is analyzed using LSE (Least Square Estimation) to obtain the main trend information based on the period. Resistance and support levels are created by calculating the standard deviation values of the data and adding these standard deviations to the main trend information. If the current value falls below the support level, the coin is listed as suitable for purchase.

FORECASTING

For a selected coin, predictions are made using the ARIMA forecasting model for a specific time range and period. For example, if the period is marked as 1 day, it predicts the value for the next day. It should be noted that the accuracy of the forecast depends on how optimally the past data is selected. It is important to remember that this is a forecast and everything can change instantly in live markets.

INDICATORS

More indicators will be added during the development process. Currently, trend lines, Bollinger bands, and average indicators have been designed. In the developing process, it will be possible for users to select parameters for these indicators.

REQUIREMENTS LIBRARY

binance, PyQt5, numpy, pandas, matplotlib, statsmodels
