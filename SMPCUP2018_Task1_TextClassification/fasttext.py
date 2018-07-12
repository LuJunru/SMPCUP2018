# -*- coding: utf-8 -*-
# @Author  : Junru_Lu
# @File    : fasttext.py
# @Software: PyCharm
# @Environment : Python 3.6+

# 基础包
import json
import fasttext

train_data_path = 'fast_data/train_new_seg.txt'
predict_data_path = 'fast_data/valid_new_seg.txt'

model_name = 'fasttext.bin'
inputf = train_data_path
classifier = fasttext.supervised(input_file=inputf, output=model_name)
result = classifier.test(train_data_path)  # 由于默认参数中epoch较小，故不用太担心过拟合
print('P@1:', result.precision)
print('R@1:', result.recall)
print('Number of examples:', result.nexamples)

predictions = classifier.predict_proba(list(open(predict_data_path, 'r').read().strip().split('\n')))
w = open('fast_data/fasttext_valid_prediction.csv', 'w')
valid_ids = [json.loads(content)['id'] for content in open('data/valid.txt', 'r').readlines()]
for valid_id in range(len(valid_ids)):
    # 若想要输出4个标签的概率：w.write(str(valid_ids[valid_id]) + "," + str(predictions[valid_id]) + "\n")
    w.write(str(valid_ids[valid_id]) + "," + str(predictions[valid_id][0][0]) + "\n")
w.close()