import requests
from bs4 import BeautifulSoup
import time
import random
from requests import RequestException


class Get_Exchange_Rate():
    def __init__(self):
        pass

    def get_the_latest_exchange_rate(self, pjname=1316, page=1):  # 默认为美元，页数为1
        url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
        headers = {
            #'Cookie': 'JSESSIONID=0000j3dN9XeSliCoEomXansRlAM:-1',
            'Host': 'srh.bankofchina.com',
            'Referer': 'http: // srh.bankofchina.com / search / whpj / search.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        postdata = {
            'erectDate': '',
            'nothing': '',
            'pjname': pjname,  # 货币代号，默认为美元,具体代号看官网
            'page': page  # 页数，默认为1
        }
        try:
            res = requests.get(url, headers=headers, params=postdata)
            soup = BeautifulSoup(res.text, 'html.parser')
            the_latest_exchange_rate_selector = 'tr:nth-of-type(3) > td'  # 最新汇率的selector
            the_latest_exchange_rate_data = soup.select(the_latest_exchange_rate_selector)
            data = {
                '货币名称': the_latest_exchange_rate_data[0].text,
                '现汇买入价': float(the_latest_exchange_rate_data[1].text),
                '现钞买入价': float(the_latest_exchange_rate_data[2].text),
                '现汇卖出价': float(the_latest_exchange_rate_data[3].text),
                '现钞卖出价': float(the_latest_exchange_rate_data[4].text),
                '中行折算价': float(the_latest_exchange_rate_data[5].text),
                '更新时间': the_latest_exchange_rate_data[6].text
            }
            # print(data)
            return data
        except RequestException:
            print('网络连接出现错误！')

    def get_all_exchange_rate(self, pjname=1316):  # 默认为美元，页数为1
        sleep_time = random.uniform(0.1, 0.3)
        all_exchange_data = [{'更新时间': '1'}]
        url = 'http://srh.bankofchina.com/search/whpj/search.jsp'
        headers = {
            #'Cookie': 'JSESSIONID=0000j3dN9XeSliCoEomXansRlAM:-1',
            'Host': 'srh.bankofchina.com',
            'Referer': 'http: // srh.bankofchina.com / search / whpj / search.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        status = 0  # 标记状态
        for page in range(1, 2000):#2000是随机写的，反正到最后一页会跳出循环
            if status == 1:
                break
            else:
                postdata = {
                    'erectDate': '',
                    'nothing': '',
                    'pjname': pjname,  # 货币代号，默认为美元,具体代号看官网
                    'page': page  # 页数
                }
                try:
                    res = requests.get(url, headers=headers, params=postdata)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    exchange_rate_selector = 'div.BOC_main.publish > table > tr'  # 一页汇率的selector
                    exchange_rate_data = soup.select(exchange_rate_selector)
                    del exchange_rate_data[0]
                    del exchange_rate_data[-1]
                    if all_exchange_data[-1]['更新时间'] == exchange_rate_data[-1].select('td')[6].text:
                        status = 1
                        break
                    else:
                         for i in exchange_rate_data:
                            new_exchange_rate_data = i.select('td')
                            data = {
                                '货币名称': new_exchange_rate_data[0].text,
                                '现汇买入价': float(new_exchange_rate_data[1].text),
                                '现钞买入价': float(new_exchange_rate_data[2].text),
                                '现汇卖出价': float(new_exchange_rate_data[3].text),
                                '现钞卖出价': float(new_exchange_rate_data[4].text),
                                '中行折算价': float(new_exchange_rate_data[5].text),
                                '更新时间': new_exchange_rate_data[6].text
                            }
                            all_exchange_data.append(data)
                except RequestException:
                    print('网络连接出现错误！')
            time.sleep(sleep_time)
        del all_exchange_data[0]
        return all_exchange_data




