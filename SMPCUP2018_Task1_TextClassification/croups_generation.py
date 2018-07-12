# -*- coding: utf-8 -*-
# @Author  : Junru_Lu
# @File    : croups_generation.py
# @Software: PyCharm
# @Environment : Python 3.6+

# 基础包
import pandas as pd
import json
import jieba
import re


def get_seg(strs):  # 清除数据中换行符，生成char数据，word数据或拼接数据
    strs_new = re.subn('\r|\n', '', strs)[0]
    # return ' '.join(list(strs_new))
    # return ' '.join(jieba.lcut(strs_new))
    return ' '.join(list(strs_new) + jieba.lcut(strs_new))


def label_to_int(label):  # 将标签映射为数字，便于训练
    if label == '人类作者':
        return 0
    elif label == '自动摘要':
        return 1
    elif label == '机器作者':
        return 2
    else:
        return 3


def data_generation(inputfile, outputfile, type, labelornot):  # 分别为训练集和验证集(测试集)生成数据，返回值为输出文件的路径
    File = open(outputfile, "w")
    if labelornot is True:
        data_dict = {'content': {}, 'label': {}}  # 将数据存储成嵌套字典的格式，便于直接用pandas生成DataFrame
        for line in open(inputfile, 'r'):
            index = json.loads(line)['id']
            data_dict['content'][index] = json.loads(line)['内容']
            data_dict['label'][index] = str(label_to_int(json.loads(line)['标签']))
        data = pd.DataFrame(data_dict)
        data['seg_content'] = data['content'].apply(get_seg)  # 对每一行用apply方法调用预定义函数
        for i in range(len(data)):
            line = data.iloc[i]['label'] + '\t' + data.iloc[i]['seg_content']
            if type == 'cnn':  # 分别安装不同模型对数据不同格式的要求进行输出处理
                File.write(line + "\n")
            elif type == 'fast':
                File.write(r'__label__' + line + "\n")
            else:
                return "模型类型错误"
    else:
        data_dict = {'content': {}}  # 验证集数据生成的特点是没有标签或随机定义标签
        for line in open(inputfile, 'r'):
            index = json.loads(line)['id']
            data_dict['content'][index] = json.loads(line)['内容']
        data = pd.DataFrame(data_dict)
        data['seg_content'] = data['content'].apply(get_seg)
        for i in range(len(data)):
            line = data.iloc[i]['seg_content']
            if type == 'cnn':
                File.write('0\t' + line + "\n")
            elif type == 'fast':
                File.write(line + "\n")
            else:
                return "模型类型错误"
    File.close()
    return outputfile

cnn_train_data_path = data_generation('data/train.txt', 'textcnn/cnn_data/train_new_seg.txt', 'cnn', labelornot=True)
cnn_valid_data_path = data_generation('data/valid.txt', 'textcnn/cnn_data/valid_new_seg.txt', 'cnn', labelornot=False)
cnn_test_data_path = data_generation('data/test.txt', 'textcnn/cnn_data/test_new_seg.txt', 'cnn', labelornot=False)
fast_train_data_path = data_generation('data/train.txt', 'fast_data/train_new_seg.txt', 'fast', labelornot=True)
fast_valid_data_path = data_generation('data/valid.txt', 'fast_data/valid_new_seg.txt', 'fast', labelornot=False)
fast_test_data_path = data_generation('data/test.txt', 'fast_data/test_new_seg.txt', 'fast', labelornot=False)