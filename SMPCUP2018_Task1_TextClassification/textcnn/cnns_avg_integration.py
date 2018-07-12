# -*- coding: utf-8 -*-
# @Author  : Junru_Lu
# @File    : cnns_avg_integration.py
# @Software: PyCharm
# @Environment : Python 3.6+

# 基础包
import json
import pandas as pd
import numpy as np


def num_to_label(num):  # 将数字编号的索引重新转回给定标签
    if num == 3.0:
        return '人类作者'
    elif num == 2.0:
        return '自动摘要'
    elif num == 1.0:
        return '机器作者'
    else:
        return '机器翻译'

char_cnn = pd.read_csv(open('cnn_data/cnn_char_prediction.csv', 'r'), header=None).transpose().get_values().tolist()
word_cnn = pd.read_csv(open('cnn_data/cnn_word_prediction.csv', 'r'), header=None).transpose().get_values().tolist()

w = open('cnn_data/cnn_merged_prediction.csv', 'w')
valid_ids = [json.loads(content)['id'] for content in open('../data/valid.txt', 'r').readlines()]
for valid_id in range(len(valid_ids)):
    w.write(str(valid_ids[valid_id]) + "," +
            num_to_label(float(np.argmax(np.add(char_cnn[valid_id], word_cnn[valid_id])))) + "\n")
w.close()