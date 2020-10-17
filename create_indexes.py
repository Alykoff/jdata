from elasticsearch import Elasticsearch
import zipfile
import json
import os
from os import listdir
from os.path import isfile, join

current_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = current_dir + "/data"
data_jsonl_dir = current_dir + "/data/jsonl"
mapping_dir = current_dir + "/index_config"
zip_postfix = '.zip'
jsonl_postfix = '.jsonl'

es = Elasticsearch([
    {'host': 'localhost', 'port': 9200, 'use_ssl': False, 'timeout': 60},
])


# noinspection PyShadowingNames,PyShadowingBuiltins
def get_files_in_dir_with_postfix(dir, postfix):
    result = [
        join(dir, f)
        for f in listdir(dir)
        if isfile(join(dir, f)) and f.endswith(postfix)
    ]
    result.sort()
    return result


def unzip_all_zip_files():
    zip_files = get_files_in_dir_with_postfix(data_dir, zip_postfix)
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(data_jsonl_dir)


# noinspection PyShadowingNames
def rm_all_data_files():
    try:
        jsonl_files = get_files_in_dir_with_postfix(data_jsonl_dir, jsonl_postfix)
        for jsonl_file in jsonl_files:
            os.remove(jsonl_file)
    except FileNotFoundError:
        pass


def get_index_name(file_name):
    return file_name.split('/')[-1][0:-22]


# noinspection PyShadowingNames
def get_mapping_info_for_index(index_name):
    mapping_name = mapping_dir + '/' + index_name + '.json'
    with open(mapping_name, 'r') as file:
        return json.load(file)['mappings']


rm_all_data_files()
unzip_all_zip_files()
jsonl_files = get_files_in_dir_with_postfix(data_jsonl_dir, jsonl_postfix)

for index_name in {get_index_name(f) for f in jsonl_files}:
    print("delete index: " + index_name)
    es.indices.delete(index=index_name, ignore=404)
    print("create index: " + index_name)
    es.indices.create(index=index_name, body={
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        },
        "mappings": get_mapping_info_for_index(index_name)
    })
    es.cluster.put_settings(body={
        "persistent": {
            "cluster": {
                "routing": {
                    "allocation": {
                        "disk": {
                            "threshold_enabled": False
                        }
                    }
                }
            }
        }
    })

num_files = len(jsonl_files)
counter_of_file = 0
for jsonl_file in jsonl_files:
    print('load percent: ' + str(round(counter_of_file / num_files * 100, 2)) + '%')
    counter_of_file += 1
    index_name = get_index_name(jsonl_file)
    print(index_name)
    count_line = 0
    # end_line = 100
    with open(jsonl_file, 'r') as f:
        # try:
        while True:
            count_line += 1
            # if count_line >= end_line:
            #     print('Break by end line condition: ' + str(end_line))
            #     break
            line = f.readline()
            if line is None or line == '':
                break
            es.index(index=index_name, body=line, request_timeout=60)
        print("num of inserting lines: " + str(count_line))
        # except:
        #     print("num of inserting lines in errors: " + str(count_line))

print('done')
