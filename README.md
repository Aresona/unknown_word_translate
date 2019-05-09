# Unknown_word_translate
自动翻译网页上的生词

## 流程

每次看英文文档卡住时都会把原因归结为单词不认识，所以把需要看的网站上的所有单词爬下来，明确找出自己不会的单词，并对症下药。

* 爬取网站所有单词，并统计频次
* 生成临时文件
* 在临时文件中删除不需要再去查询记忆的单词
* 运行脚本，自动翻译所有生词并上传到 github指定目录
* 闲暇时打开网站记忆生词并完成最初始的阅读目的。

## 说明

此项目一共会生成两个文件，第一个文件用来生成所有单词及频次统计，第二个文件则是基于整理过后的第一个文件来生成的，最终生成专属于自己的单词本文件。

## 使用说明

1. 下载项目

```python
git clone git@github.com:Aresona/unknown_word_translate.git
```

2. 打开项目并安装依赖包

```python
pip install -r < requirement.txt
```

3. 修改配置文件 `config.py`

> 分别填入网站域名、初始网页、最终生成的文件名字、git 仓库及文件存放指定位置

4. 运行脚本 `word_frequency_statistics.py`

```python
python word_frequency_statistics.py
```

5. 查看生成的临时文件(不带后缀的 filename),并保留生词
6. 运行脚本 `generate_md.py`

```
python generate_md.py
```

7. 此时即可以在 github 上查看最终结果。
