import os
import json
import shutil
import config
import youdao_transapi
from git import Repo as repo


# 翻译生词 
def translate_word():
    with open(filename, 'r', encoding='utf8') as f:
        for line in f.readlines():
            word = line.replace('\n', '').split('\t')[0]
            result = youdao_transapi.connect(word)
            result = json.loads(result)
            l = []
            try:
                l.append(result['basic']['us-phonetic'])
            except:
                pass
            try:
                l.append(result['basic']['uk-phonetic'])
            except:
                pass
            try:
                result = result['basic']['explains'] + l
                result_list = line.split('\t')
                for item in result:
                    result_list.insert(1, item + '\t')
                write_word(result_list)
            except:
                result_list = line.split('\t')
                write_word(result_list)


# 生成临时翻译文件，主要是为了获取最长的列数
def write_word(result):
    with open('./temp_' + filename, 'a', encoding='utf8') as f:
        f.write(result[0] + '\t')
        for item in result[1:]:
            f.write(item)


# 获取翻译后 临时文件的最长列数
def get_list_count():
    with open('./temp_' + filename, 'r', encoding='utf8') as f:
        count = 0
        for item in f.readlines():
            result_list = item.split('\t')
            if len(result_list) > count:
                count = len(result_list)
        return count


# 生成 md 文件
def generate_md(count):
    with open(filename + '.md', 'a', encoding='utf8') as f:
        f.write('|' * (count+1) + '\n')
        f.write('|--' * count + '|\n')
        with open('./temp_' + filename, 'r', encoding='utf8') as r:
            for item in r.readlines():
                for seg in item.split('\t'):
                    f.write('|' + seg.replace('\n', '|\n'))


# 这里加了一个remove_file,本来在支持完脚本后删除，但一旦出错后再调翻译接口有点浪费，所以这里建议手动删除
def github_upload(filename):
    # remove_file = 'temp_' + filename
    filename = filename + '.md'
    if os.path.exists(filename):
        repository = repo.clone_from(url=config.repository, to_path=config.path)
        shutil.move(filename, config.path)
        # os.remove(remove_file)
        index = repository.index
        index.add(items=[filename])
        index.commit('Upload ' + filename)
        remote = repository.remote()
        remote.push()
    else:
        print('file does\'nt exist')


if __name__ == '__main__':
    filename = config.filename
    translate_word()
    count = get_list_count()
    generate_md(count)
    github_upload(filename)
