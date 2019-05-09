import requests
import config
import re
from lxml import etree


# 获取网页的所有单词
def execute(url):
    print(url)
    response = requests.get(url)
    # 获取单词的正则表达式
    pattern1 = re.compile('[a-zA-Z]+')
    # 去除 html 标签的正则表达式
    pattern2 = re.compile('<script.*?script>|<style.*?style>|<!--.*?-->|<[^>]+>', re.S)
    response = re.sub(pattern2, '', response.text)
    result = re.findall(pattern1, response)
    print(result)
    return result


# 获取该网页所有的内部链接
def get_all_url():
    # domain 与 start_url 需要在 config.py　文件中手动配置
    domain = config.domain
    response = requests.get(config.start_url)
    html = etree.HTML(response.text)
    href = html.xpath('//a/@href')
    result = []
    for item in href:
        if '#' not in item and 'http' not in item and 'javascript' not in item and 'epub' not in item and 'pdf' not in item:
            result.append(domain + item)
    return set(result)


# 统计整个网站的词频
def statistics(result):
    result = [x.lower() for x in result]
    dic = {}
    for item in result:
        dic[item] = result.count(item)
    result_list = sorted(dic.items(), key=lambda kv: (-kv[1], kv[0]))
    with open(config.filename, 'a', encoding='utf8') as f:
        for a in result_list:
            f.write(a[0] + '\t' + str(a[1]) + '\n')


if __name__ == '__main__':
    urls = get_all_url()
    result = []
    for url in urls:
        temp_result = execute(url)
        result += temp_result
    statistics(result)

