import requests
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient
from requests import RequestException
sys.setrecursionlimit(1000000)


class Coinmarketcap_Rankings_spider(object):
    def __init__(self):
        pass

    def Market_Cap_Top100_spider(self):
        def clean_market_cap_data(i):
            a = i.text.split('$')[1].split('\n')[0].split(',')
            b = ''
            for j in a:
                b = b + j
            market_cap = int(b)
            return market_cap
        # 处理market_cap的数据，化成int型

        def clean_circulating_supplys_data(i):
            a = i.text.split('\n')[1].split(',')
            b = ''
            for j in a:
                b = b + j
            circulating_supply = int(b)
            return circulating_supply
        # 处理circulating_supplys的数据，化成int

        url = 'https://coinmarketcap.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        name_selector = 'tr > td.no-wrap.currency-name > a'
        market_cap_selector = 'tr > td.no-wrap.market-cap.text-right'
        price_selector = 'tr > td:nth-of-type(4) > a'
        volume_24h_selector = 'tr > td:nth-of-type(5) > a'
        circulating_supply_selector = 'tr > td.no-wrap.text-right.circulating-supply > span'
        change_24h_selector = 'td.no-wrap.percent-change'
        # 每个标签的selector
        names = soup.select(name_selector)
        market_caps = soup.select(market_cap_selector)
        prices = soup.select(price_selector)
        volumes_24h = soup.select(volume_24h_selector)
        circulating_supplys = soup.select(circulating_supply_selector)
        changes_24h = soup.select(change_24h_selector)
        volume_data = []
        for i in range(0, len(names)):
            data = {
                'name': names[i].text,
                'market_cap': clean_market_cap_data(market_caps[i]),
                'price': float(prices[i].text.split('$')[1]),
                'volume_24h': clean_market_cap_data(volumes_24h[i]),
                'circulating_supply': clean_circulating_supplys_data(circulating_supplys[i]),
                'change_24h': float(changes_24h[i].text.split('%')[0]) / 100
            }
            volume_data.append(data)
        return volume_data

    def Exchanges_Top100_Adjusted_Volume(self):
        def clean_volumes_data(i):
            a = i.text.split('$')[1].split('\n')[0].split(',')
            b = ''
            for j in a:
                b = b + j
            market_cap = int(b)
            return market_cap
        # 处理数据，化成int型
        url = 'https://coinmarketcap.com/rankings/exchanges/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        name_selector = 'tr > td.no-wrap.currency-name > a'
        adjusted_volume_24h_selector = 'tr > td:nth-of-type(3)'
        volume_24h_selector = 'tr > td:nth-of-type(4)'
        volume_7d_selector = 'tr > td:nth-of-type(5)'
        volume_30d_selector = 'tr > td:nth-of-type(6)'
        no_markets_selector = 'tr > td:nth-of-type(7)'
        change_24h_selector = 'tr > td.no-wrap.percent-change'
        names = soup.select(name_selector)
        adjusted_volumes_24h = soup.select(adjusted_volume_24h_selector)
        volumes_24h = soup.select(volume_24h_selector)
        volumes_7d = soup.select(volume_7d_selector)
        volumes_30d = soup.select(volume_30d_selector)
        no_markets = soup.select(no_markets_selector)
        changes_24h = soup.select(change_24h_selector)
        volume_data = []
        for i in range(0, len(names)):
            data = {
                'name': names[i].text,
                'adjusted_volume_24h': clean_volumes_data(adjusted_volumes_24h[i]),
                'volume_24h': clean_volumes_data(volumes_24h[i]),
                'volume_7d': clean_volumes_data(volumes_7d[i]),
                'volume_30d': clean_volumes_data(volumes_30d[i]),
                'no_markets': int(no_markets[i].text),
                'change_24h': float(changes_24h[i].text.split('%')[0]) / 100
            }
            volume_data.append(data)
        return volume_data

    def Exchanges_Top100_Reported_Volume(self):
        def clean_volumes_data(i):
            a = i.text.split('$')[1].split('\n')[0].split(',')
            b = ''
            for j in a:
                b = b + j
            market_cap = int(b)
            return market_cap
        # 处理数据，化成int型
        url = 'https://coinmarketcap.com/rankings/exchanges/reported/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        name_selector = 'tr > td.no-wrap.currency-name > a'
        volume_24h_selector = 'tr > td:nth-of-type(3)'
        volume_7d_selector = 'tr > td:nth-of-type(4)'
        volume_30d_selector = 'tr > td:nth-of-type(5)'
        no_markets_selector = 'tr > td:nth-of-type(6)'
        change_24h_selector = 'tr > td.no-wrap.percent-change'
        names = soup.select(name_selector)
        volumes_24h = soup.select(volume_24h_selector)
        volumes_7d = soup.select(volume_7d_selector)
        volumes_30d = soup.select(volume_30d_selector)
        no_markets = soup.select(no_markets_selector)
        changes_24h = soup.select(change_24h_selector)
        volume_data = []
        for i in range(0, len(names)):
            data = {
                'name': names[i].text,
                'volume_24h': clean_volumes_data(volumes_24h[i]),
                'volume_7d': clean_volumes_data(volumes_7d[i]),
                'volume_30d': clean_volumes_data(volumes_30d[i]),
                'no_markets': int(no_markets[i].text),
                'change_24h': float(changes_24h[i].text.split('%')[0]) / 100
            }
            volume_data.append(data)
        return volume_data

    def Exchanges_All_24h_Volume(self):
        def pop(list, n):
            for i in range(0, n):
                del list[0]
            return list

        # group必须为空列表，list为未分组数据
        def grouping(list, group):
            try:
                if len(list) > 1:
                    for j in range(0, len(list) - 1):
                        if int(list[j][0].text) < int(list[j + 1][0].text):
                            pass
                        else:
                            new_group = list[0:j + 1]
                            group.append(new_group)
                            new_list = pop(list, j + 1)
                            grouping(new_list, group)
            except IndexError:
                pass

        def clean_volumes_data(i):
            a = i.text.split('$')[1].split(',')
            b = ''
            for j in a:
                b = b + j
            market_cap = int(b)
            return market_cap
        url = 'https://coinmarketcap.com/exchanges/volume/24-hour/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        exchange_name_selector = 'tr > td > h3 > a'
        get_all_data_selector = 'tr'
        exchanges_names = soup.select(exchange_name_selector)
        # 所有交易所名称
        data = soup.select(get_all_data_selector)
        ungroup_datas = []
        for i in data:
            data = i.select('td')
            if len(data) == 6:
                ungroup_datas.append(data)
        # 提取出所有未按交易所分组的24h交易数据加入到ungroup_datas中
        group_datas = []
        grouping(ungroup_datas, group_datas)
        # 数据已经分组完毕
        del exchanges_names[-1]
        # 去掉最后一个交易所，与前一行的数据进行对齐
        volume_data = []
        if len(group_datas) == len(exchanges_names):
            for j in range(0, len(exchanges_names)):
                for i in group_datas[j]:
                    data = {
                        'exchange': exchanges_names[j].text,
                        'ranking': i[0].text,
                        'currency': i[1].text,
                        'pair': i[2].text,
                        'volume_24h': clean_volumes_data(i[3]),
                        'price': float(i[4].text.split('$')[1]),
                        'volume_percent': float(i[5].select('span')[0].text) / 100
                    }
                    volume_data.append(data)
            for count in range(0, counts):
                print(volume_data[count])
        else:
            print('数据不匹配！请检查代码')
        return volume_data

    def Cryptocurrencies_All_24h_Volume(self):
        # 此函数作用为更新列表，n为更新次数
        def pop(list, n):
            for i in range(0, n):
                del list[0]
            return list

        # group必须为空列表，list为未分组数据
        def grouping(list, group):
            try:
                if len(list) > 1:
                    for j in range(0, len(list) - 1):
                        if int(list[j][0].text) < int(list[j + 1][0].text):
                            pass
                        else:
                            new_group = list[0:j + 1]
                            group.append(new_group)
                            new_list = pop(list, j + 1)
                            grouping(new_list, group)
            except IndexError:
                pass

        def clean_volumes_data(i):
            a = i.text.split('$')[1].split(',')
            b = ''
            for j in a:
                b = b + j
            market_cap = int(b)
            return market_cap

        url = 'https://coinmarketcap.com/currencies/volume/24-hour/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        currencies_name_selector = 'tr > td > h3 > a'  # 数字货币名称
        percent_volume_selector = 'tr > td > h3 > span'  #
        get_all_data_selector = 'tr'
        currencies_names = soup.select(currencies_name_selector)
        percent_volume = soup.select(percent_volume_selector)
        data = soup.select(get_all_data_selector)
        ungroup_datas = []
        for i in data:
            data = i.select('td')
            if len(data) == 6:
                ungroup_datas.append(data)
        # 提取出所有未按币名称分组的24h交易数据加入到ungroup_datas中
        group_datas = []
        grouping(ungroup_datas, group_datas)
        # 数据已经分组完毕
        del currencies_names[-1]
        volume_data = []
        if len(group_datas) == len(currencies_names):
            for j in range(0, count):
                for i in group_datas[j]:
                    data = {
                        'currency_name': currencies_names[j].text,
                        'ranking': i[0].text,
                        'source': i[1].text,
                        'pair': i[2].text,
                        'volume_24h': clean_volumes_data(i[3]),
                        'price': float(i[4].text.split('$')[1]),
                        'volume_percent': float(i[5].select('span')[0].text) / 100
                    }
                    volume_data.append(data)
        else:
            print('数量不匹配！检查代码！')
        return volume_data

    def Cryptocurrencies_All_30d_Volume(self):
        def clean_volumes_data(i):
            try:
                a = i.split('\n')[1].split('$')[1].split(',')
                b = ''
                for j in a:
                    b = b + j
                market_cap = int(b)
                return market_cap
            except IndexError:
                return 0
        count = 20
        url = 'https://coinmarketcap.com/currencies/volume/monthly/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        # headers头，Cookie可去掉
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        all_data_select = 'tr'
        datas = soup.select(all_data_select)
        clean_datas = []
        volume_data = []
        for i in datas:
            td = i.select('td')
            if len(td) == 6:
                clean_datas.append(td)
        for j in clean_datas:
            data = {
                'ranking': int(j[0].text.split('\n')[1]),
                'name': j[1].text.split('\n')[2],
                'symbol': j[2].text,
                'volume_1d': clean_volumes_data(j[3].text),
                'volume_7d': clean_volumes_data(j[4].text),
                'volume_30d': clean_volumes_data(j[5].text)
            }
            volume_data.append(data)
        return volume_data







