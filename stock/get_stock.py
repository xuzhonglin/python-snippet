#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/6/11 9:43
@Author   : colinxu
@File     : get_stock.py
@Desc     : 
"""
import requests
import datetime


class SinaStock:
    def __init__(self):
        pass

    def get_stock(self, stock_code):
        result = []
        if type(stock_code) == list:
            stock_code = ','.join(stock_code)
        url = 'http://hq.sinajs.cn/list=' + stock_code
        resp = requests.get(url)
        for stock_item in resp.text.split(';'):
            if 'var hq_str_' not in stock_item: continue
            stock_str = stock_item.replace('"', '').replace("\n", '')
            stock_str = stock_str.replace(';', '').replace('var hq_str_', '').replace('=', ',')
            stock_list = stock_str.split(',')
            stock_temp = {
                'name': stock_list[1],
                'code': stock_list[0],
                'open': stock_list[2],
                'last_close': stock_list[3],
                'price': stock_list[4],
                'change_rate': '%.2f' % ((float(stock_list[4]) - float(stock_list[2])) / float(stock_list[2]) * 100),
                'high': stock_list[5],
                'low': stock_list[6],
                'volume': stock_list[9],
                'amount': stock_list[10],
                'date': stock_list[31],
                'time': stock_list[32]
            }
            result.append(stock_temp)
            print(stock_temp)
        return result

    def get_day_line(self, stock_code: str, scale: int = 240):
        url = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={}&scale={}&ma=no' \
              '&datalen=1000'
        url = url.format(stock_code, scale)
        resp = requests.get(url)
        return resp.json()

    # 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    def _getdate(self, beforeOfDay):
        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=-beforeOfDay)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y%m%d')
        return re_date


if __name__ == '__main__':
    # stock = SinaStock()
    # stock.get_stock('sh603056')
    # stock.get_day_line('sh603056')
    from pyecharts.charts import Bar

    bar = Bar()
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    # render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
    # 也可以传入路径参数，如 bar.render("mycharts.html")
    bar.render()
