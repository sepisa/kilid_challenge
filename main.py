from database import Database
from plots import Plot
import requests
from bs4 import BeautifulSoup
import json


class Crawler:

    def __init__(self):
        self.db = None

    def generate_db(self):
        self.db = Database()
        self.db.create_database()
        self.db.connect_to_database()
        self.db.create_table()


    def crawl(self):
        url = """https://api.accessban.com/v1/market/indicator/summary-table-data/price_dollar_rl?lang=fa&order_dir=asc&
        draw=1&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&
        columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&
        columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=2&
        columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&
        columns[3][data]=3&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&
        columns[4][data]=4&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&
        columns[5][data]=5&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&
        columns[6][data]=6&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&
        columns[7][data]=7&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&
        start=0&length=365&search=&order_col=&order_dir=&from=&to=&convert_to_ad=1&_=1655879640219"""
        res = requests.get(url)
        response = json.loads(res.content)
        for item in response['data']:
            start_value = int(item[0].replace(',', ''))
            min_value = int(item[1].replace(',', ''))
            max_value = int(item[2].replace(',', ''))
            end_value = int(item[3].replace(',', ''))

            soup = BeautifulSoup(item[4], 'html.parser') 
            span = soup.find("span")
            change_value = span.text if span.text != '-' else 0 

            soup = BeautifulSoup(item[5], 'html.parser') 
            span = soup.find("span")
            change_percent = float(span.text.replace('%', '')) if span is not None else 0

            date = item[6]

            self.db.insert(start_value, min_value, max_value, end_value, change_value, change_percent, date)
        return



    def plots(self):
        self.plt = Plot()
        # self.plt.line_plot()
        self.plt.candleStick_plot()
if __name__ == '__main__':
    crawler = Crawler()
    crawler.generate_db()
    crawler.crawl()
    crawler.plots()