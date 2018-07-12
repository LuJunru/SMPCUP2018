本项目是针对[SMP CUP 2018任务三文本溯源](https://biendata.com/competition/smpetst2018/)的代码实现，主要架构为Elasticsearch检索+基于ES分值和Jacob距离的Wilson公式重排序。Elasticsearch是为了加速在大数据环境下的检索效率。当使用ES时，本项目仅需(准备数据时间5-6min，检测并写出结果时间13-18min)便可完成任务三。

# 环境
## Python3.6
- elasticsearch6.1.1
- jieba0.39
- math

## Elasticsearch
- Java：java version "1.8.0_111"。本项目是在mac os环境下完成的，该环境内置了java。如果要在linux或windows下使用es，需先配置java8。
- 网络：无需登陆的Wi-Fi网络，不能是类似校园网的账号网络，手机热点网络可以。联网不会调用搜索引擎等第三方服务，只是为了配合搭建ES环境。

# 使用
## 启动elasticsearch服务
- cmd：在cmd进入到本项目的elasticseatch-6.0.1文件夹下，输入命令 bin/elasticsearch
- 教程：本项目提供一个录屏视频说明es服务的使用，详见百度网盘(链接:https://pan.baidu.com/s/1H1tMW6cJx8hdBhuuidMlyA；密码:9an9)

## 主程序
- es：在运行主程序前，务必确保elasticsearch服务已经启动
- cmd：在cmd进入到本项目主路径下，输入命令 python3 mainprogram.py
- Pycharm等第三方编译器：若不使用cmd环境，则在编译器中直接运行mainprogram.py即可

# 效果
- 本项目在任务三F1上分值为0.67，与第一名0.79差距较大。但项目实现的最大优势在于时间，本项目匹配速度约为一般队伍的80～100倍。

# 其它
- 请邮件联系 lujunru31415926@163.com 咨询关于本项目的任何问题