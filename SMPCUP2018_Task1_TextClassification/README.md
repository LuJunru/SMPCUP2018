本项目是针对[SMP CUP 2018任务一文本分类](https://biendata.com/competition/smpeupt2018/)的代码实现，主要架构为Fasttext+WordCNN+CharCNN+基于分数平均的模型融合。其中CNN部分参考了[这个工程](https://github.com/norybaby/sentiment_analysis_textcnn)。此外，因为Fasttext在验证和测试集上效果不佳，所以模型融合是只针对多个CNN模型的融合。

# 环境
## Python3.6
- jieba、json、pandas、numpy、tensorflow、re、fasttext、word2vec、os、csv

# 使用
## 数据预处理
```
$ python3 croups_generation.py
```

## 训练词向量
```
$ python3 word2vec_bin_generation.py
```

## 模型训练、验证与预测
### Fasttext
```
$ python3 fasttext.py
```
### WordCNN/CharCNN
```
$ python3 textcnn/cnn_train.py
$ python3 textcnn/cnn_predict.py
```

## 模型融合
```
$ python3 cnns_avg_integration.py
```
# 效果
```
$ fasttext: 训练集F10.94，验证集F10.90
$ charcnn: 训练集F10.99，验证集F10.979
$ wordcnn: 训练集F10.99，验证集F10.976
$ avgmodel: 训练集F1N/A，验证集F10.984，测试集F10.9839
```

# 其它
- 比赛经验：1.服务器上要配好GPU；2.模型融合可以显著提高效果，但是一定要用差异性强的模型进行融合，我们最欠缺的就是没有加入TextRNN等模型
- 请邮件联系 lujunru31415926@163.com 咨询关于本项目的任何问题