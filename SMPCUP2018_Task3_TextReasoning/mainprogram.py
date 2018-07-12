# -*- coding: utf-8 -*-
# @Author  : Junru_Lu
# @File    : mainprogram.py
# @Software: PyCharm
# @Environment : Python 3.6+

# ES相关包
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import elasticsearch

# 基础包
import jieba
import math
import time

# ------------------预加载------------------ #

# 建立ES实例
es = Elasticsearch()


# ------------------ES相关函数------------------ #

def query_generation(inputs):  # 生成ES查询
    '''
    ES DSL语法:https://es.xiaoleilu.com/054_Query_DSL/70_Important_clauses.html
    全文搜索: https://es.xiaoleilu.com/100_Full_Text_Search/00_Intro.html
    '''
    _query = \
        {
            "query": {
                "bool": {
                    "should": inputs
                }
            }
        }

    return _query


class ElasticSearchClient(object):  # 启动ES
    @staticmethod
    def get_es_servers():
        es_servers = [{
            "host": "localhost",
            "port": "9200"
        }]
        es_client = elasticsearch.Elasticsearch(hosts=es_servers)
        return es_client


class LoadElasticSearch(object):  # 在ES中加载、批量插入数据
    def __init__(self):
        self.index = "my-index"
        self.doc_type = "test-type"
        self.es_client = ElasticSearchClient.get_es_servers()
        self.set_mapping()

    def set_mapping(self):
        """
        设置mapping
        IK插件: https://github.com/medcl/elasticsearch-analysis-ik
        """
        mapping = {
            self.doc_type: {  # 自定义数据种类
                    "source_id": {
                        "type": "string"
                    },
                    "source_sen": {
                        "type": "string"
                    }
                }
            }

        if not self.es_client.indices.exists(index=self.index):
            # 创建Index和mapping
            self.es_client.indices.create(index=self.index, body=mapping, ignore=400)
            self.es_client.indices.put_mapping(index=self.index, doc_type=self.doc_type, body=mapping)

    def add_date_bulk(self, row_obj_list):
        """
        批量插入ES
        """
        load_data = []
        i = 1
        bulk_num = 100000  # 10000条为一批
        for row_obj in row_obj_list:
            action = {
                "_index": self.index,
                "_type": self.doc_type,
                "_source": {
                    'source_id': row_obj.get('source_id', None),
                    'source_sen': row_obj.get('source_sen', None)
                }
            }
            load_data.append(action)
            i += 1
            # 批量处理
            if len(load_data) == bulk_num:
                print('插入', int(i / bulk_num), '批数据')
                success, failed = bulk(self.es_client, load_data, index=self.index, raise_on_error=True)
                del load_data[0:len(load_data)]
                print(success, failed)

        if len(load_data) > 0:
            success, failed = bulk(self.es_client, load_data, index=self.index, raise_on_error=True)
            del load_data[0:len(load_data)]
            print(success, failed)


# -----------------基础函数----------------- #

def list_jacob_distance(lista, listb):
    inner_list = list(set([iword for iword in lista if iword in listb]))
    union_list = list(set([iword for iword in lista if iword not in listb])) + \
                 list(set([iword for iword in listb if iword not in lista])) + inner_list
    union_list = list(set(union_list))
    return float(len(inner_list)) / float(len(union_list))


def search(new_question_words):

    # 封装成es query需要的样式，match_phrase可保证分词后的词组不被再拆散成字
    input_string = [{"match_phrase": {"source_sen": phrase}} for phrase in new_question_words]
    _query_name_contains = query_generation(input_string)  # 生成ES查询
    _searched = es.search(index='my-index', doc_type='test-type', body=_query_name_contains)  # 执行查询

    return _searched['hits']['hits']


# ------------------主函数------------------ #

if __name__ == '__main__':  # 供测试时使用

    start = time.time()

    # 使用时间数据随机初始化索引
    from datetime import datetime
    es.index(index="my-index", doc_type="test-type", body={"any": "data", "timestamp": datetime.now()})

    load_es = LoadElasticSearch()

    row_obj_list = []
    for record in open('data/A数据集.txt', 'r'):
        record_list = record.strip().split('\t')
        try:
            row_obj_list.append({'source_id': record_list[0], 'source_sen': record_list[1]})
        except:
            print(record_list)
            
    load_es.add_date_bulk(row_obj_list)  # 批量加载

    middle = time.time()
    print('ES数据加载与索引建立完成，共耗时：' + str(middle - start))

    w = open('data/final.csv', 'w')
    w.write('test_id,result\n')
    count = 0
    for line in open('data/B数据集.txt', 'r'):
        line_list = line.strip().split("\t")
        line_id = line_list[0]
        line_content = line_list[1]
        candidate_dict = {}
        line_words = jieba.lcut(line_content)

        results = search(line_words)
        for result_index in range(len(results)):
            result = results[result_index]
            result_id = result['_source']['source_id']
            result_score = result['_score']
            result_content = result['_source']['source_sen']
            result_words = jieba.lcut(line_content)

            jacob_score = list_jacob_distance(line_words, result_words)

            u = result_score / 50.0
            v = 1.0 - jacob_score
            n = u + v
            p = u / n
            final_score = (p + 0.5 / n - 0.5 / n * math.sqrt(4 * n * p * (1 - p) + 1)) / (1 + 1 / n)
            candidate_dict[result_id] = final_score

        count += 1
        if count % 100 == 0:
            print("已经检测和匹配完成" + str(count) + "行")

        final_dict = sorted(candidate_dict.items(), key=lambda x: x[1], reverse=True)
        w.write(line_id + ',' + final_dict[0][0] + '\n')
    w.close()

    end = time.time()
    print('数据查询和匹配完毕，共耗时：' + str(end - middle))