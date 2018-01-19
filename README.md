
# 依赖python版本 #

```
Python 2.7.13
```

# 依赖python包

```
pip install -r requirements.txt
```

# 运行代码

** 可以按以下几种运行方式运行 **

```
python index.py
python index.py txt/smsm.txt
python index.py txt/smsm.txt 127.0.0.1:39721
```

# 本工程作用
  ```
  根据CJJ提供的TXT文献资料，提取出所有的文献title并到google学术去搜索下载对应的pdf，然后分析解析其中的文章引用关系，最后生成到summary.txt中
  ```

# 需要额外建几个文件夹,注意:

```
请确保工程根目录下已经创建了pdf文件夹，download文件夹，txt文件夹，summary文件夹
```
