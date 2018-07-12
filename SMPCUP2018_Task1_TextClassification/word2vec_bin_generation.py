# -*- coding: utf-8 -*-
# @Author  : Junru_Lu
# @File    : word2vec_bin_generation.py
# @Software: PyCharm
# @Environment : Python 3.6+

# 基础包
import word2vec

# w = open('word2vec_data/new_seg_char.txt', 'w')
# w = open('word2vec_data/new_seg_word.txt', 'w')
w = open('word2vec_data/new_seg.txt', 'w')  # 拼接训练、验证和预测数据集为词向量语料（字/词/字+词）
for train_line in open('fast_data/train_new_seg.txt', 'r'):
    w.write(train_line)
for valid_line in open('fast_data/valid_new_seg.txt', 'r'):
    w.write(valid_line)
for test_line in open('fast_data/test_new_seg.txt', 'r'):
    w.write(test_line)
w.close()

word2vec.word2vec('word2vec_data/new_seg.txt', 'word2vec_data/word2vec_all.bin', size=128, verbose=True)