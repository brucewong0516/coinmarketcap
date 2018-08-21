import requests
from bs4 import BeautifulSoup
import sys
import json
from requests import RequestException
from numpy import NaN
import time
sys.setrecursionlimit(1000000)


class Coinmarketcap_spider(object):
    def __init__(self):
        pass

    class Rankings(object):
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

        def Exchanges_Top100_Adjusted_Volume_spider(self):
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
            try:
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                data_selector = 'tr'
                data = soup.select(data_selector)
                del data[0]
                name_selector = 'td.no-wrap.currency-name > a'
                adjusted_volume_24h_selector = 'td:nth-of-type(3)'
                volume_24h_selector = 'td:nth-of-type(4)'
                volume_7d_selector = 'td:nth-of-type(5)'
                volume_30d_selector = 'td:nth-of-type(6)'
                no_markets_selector = 'td:nth-of-type(7)'
                change_24h_selector = 'td.no-wrap.percent-change'
                volume_data = []
                for i in data:
                    try:
                        name = i.select(name_selector)[0].text
                    except IndexError:
                        name = NaN
                    try:
                        adjusted_volume_24h = clean_volumes_data(i.select(adjusted_volume_24h_selector)[0])
                    except IndexError:
                        adjusted_volume_24h = NaN
                    try:
                        volume_24h = clean_volumes_data(i.select(volume_24h_selector)[0])
                    except IndexError:
                        volume_24h = NaN
                    try:
                        volume_7d = clean_volumes_data(i.select(volume_7d_selector)[0])
                    except IndexError:
                        volume_7d = NaN
                    try:
                        volume_30d = clean_volumes_data(i.select(volume_30d_selector)[0])
                    except IndexError:
                        volume_30d = NaN
                    try:
                        no_markets = int(i.select(no_markets_selector)[0].text)
                    except IndexError:
                        no_markets = NaN
                    try:
                        change_24h = float(i.select(change_24h_selector)[0].text.split('%')[0]) / 100
                    except IndexError:
                        change_24h = NaN
                    except ValueError:
                        change_24h = NaN
                    data = {
                        'name': name,
                        'adjusted_volume_24h': adjusted_volume_24h,
                        'volume_24h': volume_24h,
                        'volume_7d': volume_7d,
                        'volume_30d': volume_30d,
                        'no_markets': no_markets,
                        'change_24h': change_24h
                    }
                    volume_data.append(data)
                return volume_data
            except RequestException:
                print('请求Exchanges_Top100_Adjusted_Volume时网络连接出现错误！')

        def Exchanges_Top100_Reported_Volume_spider(self):
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
            try:
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                data_selector = 'tr'
                data = soup.select(data_selector)
                del data[0]
                name_selector = 'td.no-wrap.currency-name > a'
                volume_24h_selector = 'td:nth-of-type(3) > a'
                volume_7d_selector = 'td:nth-of-type(4) > a'
                volume_30d_selector = 'td:nth-of-type(5) > a'
                no_markets_selector = 'td:nth-of-type(6)'
                change_24h_selector = 'td.no-wrap.percent-change'
                volume_data = []
                for i in data:
                    try:
                        name = i.select(name_selector)[0].text
                    except IndexError:
                        name = NaN
                    try:
                        volume_24h = clean_volumes_data(i.select(volume_24h_selector)[0])
                    except IndexError:
                        volume_24h = NaN
                    try:
                        volume_7d = clean_volumes_data(i.select(volume_7d_selector)[0])
                    except IndexError:
                        volume_7d = NaN
                    try:
                        volume_30d = clean_volumes_data(i.select(volume_30d_selector)[0])
                    except IndexError:
                        volume_30d = NaN
                    try:
                        no_markets = int(i.select(no_markets_selector)[0].text)
                    except IndexError:
                        no_markets = NaN
                    try:
                        change_24h = float(i.select(change_24h_selector)[0].text.split('%')[0]) / 100
                    except IndexError:
                        change_24h = NaN
                    except ValueError:
                        change_24h = NaN
                    data = {
                        'name': name,
                        'volume_24h': volume_24h,
                        'volume_7d': volume_7d,
                        'volume_30d': volume_30d,
                        'no_markets': no_markets,
                        'change_24h': change_24h
                    }
                    volume_data.append(data)
                return volume_data
            except RequestException:
                print('请求Exchanges_Top100_Reported_Volume时网络出现错误！')
                return 0

        def Exchanges_All_24h_Volume_spider(self):
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
            try:
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
                else:
                    print('数据不匹配！请检查代码')
                return volume_data
            except RequestException:
                print('请求Exchanges_All_24h_Volume是网络连接出现错误！')
                return 0

        def Cryptocurrencies_All_24h_Volume_spider(self):
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

            def clean_price_data(i):
                a = i.text.split('$')[1].split('\n')[0].split(',')
                if len(a) == 1:
                    return float(a[0])
                else:
                    b = ''
                    for j in a:
                        b = b + j
                    return float(b)

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
                for j in range(0, len(currencies_names)):
                    for i in group_datas[j]:
                        data = {
                            'currency_name': currencies_names[j].text,
                            'ranking': i[0].text,
                            'source': i[1].text,
                            'pair': i[2].text,
                            'volume_24h': clean_volumes_data(i[3]),
                            'price': clean_price_data(i[4]),
                            'volume_percent': float(i[5].select('span')[0].text) / 100
                        }
                        volume_data.append(data)
            else:
                print('数量不匹配！检查代码！')
            return volume_data

        def Cryptocurrencies_All_30d_Volume_spider(self):
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

    class Trending(object):
        def __init__(self):
            pass

        def gainers_and_losers_spider(self):
            def clean_volume_data(i):
                a = i.split('$')[1].split(',')
                b = ''
                for j in a:
                    b = b + j
                market_cap = int(b)
                return market_cap

            # 这个函数的作用是为了将volume处理成int形式

            def get_1h_7d_24h_data(x, y, data):
                new_list = []
                for i in data[x:y]:
                    list = i.select('td')
                    rankings = int(list[0].text.split('\n')[1])
                    name = list[1].select('a')[0].text
                    symbol = list[2].text
                    volume = clean_volume_data(list[3].select('a')[0].text)
                    price = float(list[4].select('a')[0].text.split('$')[1])
                    percent = float(list[5].text.split('%')[0]) / 100
                    a = {
                        'rankings': rankings,
                        'name': name,
                        'symbol': symbol,
                        'volume': volume,
                        'price': price,
                        'percent': percent
                    }
                    new_list.append(a)
                return new_list
            # x，y是切片位置，data是需要切片的集合，这个函数的作用是为了按照1h，7d，24h的时间跨度分别切分并将数据整理成dic形式

            url = 'https://coinmarketcap.com/gainers-losers/'
            headers = {
                'User-Agent': 'Mozi lla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            try:
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                selector = 'tr'
                data = soup.select(selector)
                del data[0]
                del data[30]
                del data[60]
                del data[90]
                del data[120]
                del data[150]
                # 这6个del是为了清除多余的没用的数据
                gainers_1h = get_1h_7d_24h_data(0, 30, data)
                gainers_7d = get_1h_7d_24h_data(30, 60, data)
                gainers_24h = get_1h_7d_24h_data(60, 90, data)
                losers_1h = get_1h_7d_24h_data(90, 120, data)
                losers_7d = get_1h_7d_24h_data(120, 150, data)
                losers_24h = get_1h_7d_24h_data(150, 180, data)
                gainers_losers_data = {
                    'gainers_1h': gainers_1h,
                    'gainers_7d': gainers_7d,
                    'gainers_24h': gainers_24h,
                    'losers_1h': losers_1h,
                    'losers_7d': losers_7d,
                    'losers_24h': losers_24h
                }
                return gainers_losers_data
            # 返回字典形式，keys为上面6个，每个key内是列表，列表内是字典
            except RequestException:
                print('网络连接出现错误！')
                return 0

    class Tools(object):
        def __init__(self):
            pass

        def global_charts_spider(self):
            marketcap_total_url = 'https://graphs2.coinmarketcap.com/global/marketcap-total/'
            marketcap_altcoin_url = 'https://graphs2.coinmarketcap.com/global/marketcap-altcoin/'
            dominance_url = 'https://graphs2.coinmarketcap.com/global/dominance/'
            headers = {
                'origin': 'https://coinmarketcap.com',
                'referer': 'https://coinmarketcap.com/charts/',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            try:
                marketcap_total_res = requests.get(marketcap_total_url, headers=headers)
                marketcap_total_data = json.loads(marketcap_total_res.text)
            except RequestException:
                marketcap_total_data = {}
                print('请求marketcap_total时网络连接出现错误！')
            try:
                marketcap_altcoin_res = requests.get(marketcap_altcoin_url, headers=headers)
                marketcap_altcoin_data = json.loads(marketcap_altcoin_res.text)
            except RequestException:
                marketcap_altcoin_data = {}
                print('请求marketcap_altcoin时网络连接出现错误！')
            try:
                dominance_res = requests.get(dominance_url, headers=headers)
                dominance_data = json.loads(dominance_res.text)
            except RequestException:
                dominance_data = {}
                print('请求dominance时网络连接出现错误！')
            global_charts_data = {
                'marketcap_total_data': marketcap_total_data,
                'marketcap_altcoin_data': marketcap_altcoin_data,
                'dominance_data': dominance_data
            }
            return global_charts_data


if __name__ == '__main__':
    spider1 = Coinmarketcap_spider().Rankings().Market_Cap_Top100_spider()
#    time.sleep(0.5)
#    spider2 = Coinmarketcap_spider().Rankings().Cryptocurrencies_All_24h_Volume_spider()
#    time.sleep(0.5)
#    spider3 = Coinmarketcap_spider().Rankings().Cryptocurrencies_All_30d_Volume_spider()
#    time.sleep(0.5)
#    spider4 = Coinmarketcap_spider().Rankings().Exchanges_All_24h_Volume_spider()
#    time.sleep(0.5)
#    spider5 = Coinmarketcap_spider().Rankings().Exchanges_Top100_Adjusted_Volume_spider()
#    time.sleep(0.5)
#    spider6 = Coinmarketcap_spider().Rankings().Exchanges_Top100_Reported_Volume_spider()
#    time.sleep(0.5)
#    spider7 = Coinmarketcap_spider().Tools().global_charts_spider()
#    time.sleep(0.5)
#    spider8 = Coinmarketcap_spider.Trending().gainers_and_losers_spider()
#    print(spider1)
#    print(spider2)
#    print(spider3)
#    print(spider4)
#    print(spider5)
#    print(spider6)
#    print(spider7)
    print(spider1)