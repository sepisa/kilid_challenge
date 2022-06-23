import seaborn as sb
from mplfinance.original_flavor import candlestick_ohlc

from database import Database
import pandas as pd
import matplotlib.dates as mpl_dates
import finplot as fplt
import plotly.graph_objects as go
import matplotlib.pyplot as plt
class Plot:

    def __init__(self):
        self.db = None

    def read_table(self):
        self.db = Database()
        df = self.db.read_table()
        return df

    def line_plot(self):
        df = self.read_table()
        # print(df)
        plt.figure(figsize=(12, 6))
        plt.plot(df.GR_DATE, df.CLOSE)
        # set label
        plt.ylabel("Close per day")
        plt.xlabel("date")
        plt.savefig("daily_close.png")

    def candleStick_plot(self):
        df = self.read_table()
        plt.style.use('ggplot')
        df_can = df.loc[:, ['GR_DATE', 'OPEN', 'MAX', 'MIN', 'CLOSE']]
        df_can['GR_DATE'] = pd.to_datetime(df_can['GR_DATE'])
        df_can['GR_DATE'] = df_can['GR_DATE'].apply(mpl_dates.date2num)
        df_can = df_can.astype(float)

        # Creating Subplots
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, df_can.values, width=0.9, colorup='green', colordown='red', alpha=0.8)

        # Setting labels & titles
        ax.set_xlabel('Date')
        ax.set_ylabel('rate')
        fig.suptitle('Daily Candlestick Chart ')

        # Formatting Date
        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        fig.tight_layout()

        plt.savefig('candlestock.png')
