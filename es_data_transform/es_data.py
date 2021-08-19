#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/4/6 15:33
@Author   : colinxu
@File     : es_data.py
@Desc     : 
"""
import json
import os
import time
import requests

SETTINGS = '/_settings'
SEARCH = '/_search'


class ESData:
    size = 10000

    def __init__(self, url, index_name, index_type):
        self.url = url + "/" + index_name + "/" + index_type
        self.base_url = url
        self.index_name = index_name
        self.index_type = index_type
        self.condition = {}
        # self.settings = self.get_index_settings()


    def set_export_condition(self, condition: dict):
        """
        设置导出的查询条件
        :param condition: 条件
        :return:
        """
        self.condition = condition

    def export_data(self):
        """
        导出数据
        :return:
        """
        print("开始导出...")
        begin = time.time()
        try:
            os.remove(self.index_name + "_" + self.index_type + ".json")
        except:
            pass
        headers = {
            'Content-Type': 'application/json'
        }
        msg = requests.post(self.url + "/_search", data=json.dumps(self.condition), headers=headers)
        obj = msg.json()
        total = obj["hits"]["total"]
        print('导出数据，共：' + str(total))
        # 设置max_size
        if total > 10000:
            self.update_max_size(1000001)
        cur = 0
        while cur < total:
            msg = requests.post(self.url + "/_search" + "?from=" + str(cur) + "&size=" + str(self.size)
                                , data=json.dumps(self.condition), headers=headers)
            self.write_to_file(msg)
            cur = cur + self.size + 1
        # 导出完成，还原max_size FIXME 还原原来的max_size
        if total > 10000:
            self.update_max_size(10000)
        print("导出完成!耗时:" + str(time.time() - begin) + "s")

    def import_data(self):
        """
        导入数据
        :return:
        """
        print("开始导入...")
        begin = time.time()
        # self.update_es_blocks(False)
        data_list = []
        # 读取数据
        with open(self.index_name + "_" + self.index_type + ".json", "r", encoding='utf-8') as f:
            for line in f:
                line = json.loads(line)
                if '_type' in line:
                    line.pop('_type')
                if '_index' in line:
                    line.pop('_index')
                if '_score' in line:
                    line.pop('_score')
                data_list.append(line)
        self.write_to_es_batch(data_list)
        # self.update_es_blocks(True)
        print("导入完成!耗时：" + str(time.time() - begin) + "s")

    def write_to_es(self, data):
        """
        向es写入数据 单条写入
        :param data:
        :return:
        """
        headers = {
            'Content-Type': 'application/json'
        }
        id = data['_id']
        data = data['_source']
        payload = json.dumps(data).encode('utf-8')
        req = requests.put(self.url + '/' + id, data=payload, headers=headers)
        if req.status_code == 201 or req.status_code == 200:
            return True, data
        elif req.status_code == 200:
            print('插入失败，存在重复数据：' + req.text)
        else:
            print('插入失败：' + req.text)
            return False, req.text

    def write_to_es_batch(self, data_list: list):
        """
        向es写入数据 批量写入
        :param data_list:
        :return:
        """
        from concurrent.futures import ThreadPoolExecutor
        startTime = time.time()
        threadPool = ThreadPoolExecutor(max_workers=15, thread_name_prefix="thread")
        for result, data in threadPool.map(self.write_to_es, data_list):
            pass
            # if not result:
            #     print('插入失败：' + str(data))
        endTime = time.time()
        print('执行耗时：{}'.format(endTime - startTime))
        return True

    def write_to_file(self, msg):
        """
        将数据写入文件
        :param msg:
        :return:
        """
        obj = msg.json()
        values = obj["hits"]["hits"]
        with open(self.index_name + "_" + self.index_type + ".json", "a", encoding='utf-8') as f:
            for val in values:
                a = json.dumps(val, ensure_ascii=False)
                f.write(a + "\n")

    def update_max_size(self, max_size):
        """
        修改结果窗口大小
        :param max_size: 大小
        :return:
        """
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'index.max_result_window': max_size
        }
        payload = json.dumps(payload).encode('utf-8')
        try:
            # self.update_es_blocks(False)
            rep = requests.put(self.base_url + '/' + self.index_name + '/_settings', data=payload, headers=headers)
            print(rep.text)
        except Exception as ex:
            print(ex)
        finally:
            pass
            # self.update_es_blocks(True)

    def update_es_blocks(self, is_blocks):
        """
        更新读写锁
        :param is_blocks: 是否只读
        :return:
        """
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "index.blocks.read_only_allow_delete": is_blocks
        }
        payload = json.dumps(payload).encode('utf-8')
        rep = requests.put(self.base_url + '/' + self.index_name + '/_settings', data=payload, headers=headers)
        print(rep.text)

    def get_index_settings(self):
        resp = self._http_get(self.index_name+'/'+SETTINGS)
        return resp.json()[self.index_name]['settings']

    def delete_all_data(self):
        """
        删除所有数据
        :return:
        """
        pass

    def _http_put(self, url, data):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(data).encode('utf-8')
        try:
            return requests.put(self.base_url + url, data=payload, headers=headers)
        except Exception as ex:
            print(ex)
        finally:
            pass
            # self.update_es_blocks(True)

    def _http_post(self, url, data):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(data).encode('utf-8')
        try:
            return requests.post(self.base_url + url, data=payload, headers=headers)
        except Exception as ex:
            print(ex)
        finally:
            pass

    def _http_get(self, url):
        try:
            return requests.get(self.base_url + url)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    es_api = 'http://10.230.39.46:9200'
    # real_t_omr_ywdb_master real_t_omr_ywdb_trend real_t_omr_ywdb_cust_bill
    es_index = 'real_time_ka360_income_trend_bak'
    es_type = 'info'
    export_condition = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "product_name": "精准重货"
                        }
                    }
                ]
            }
        }
    }
    es = ESData(es_api, es_index, es_type)
    # es.set_export_condition(export_condition)
    # es.export_data()
    es.import_data()
