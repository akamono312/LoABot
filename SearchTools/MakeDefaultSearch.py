import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import json

# 하나의 항목에 대한 키값을 통해 딕셔너리를 찾아서 같은 딕셔너리의 특정 항목에 대한 키값을 불러오기
def get_category(option: str, key: str):
    with open("jsons/SearchOptions.json", 'r', encoding='utf-8') as file:
        response = json.load(file)
    for i in response["Categories"]:
        if i['name'] == option:
            return i[key]

# 위에서 찾은 딕셔너리의 항목을 jsons/ModifiedSearchOption.json의 형식에 맞게 저장하기
def save_option(option: str, key: str):
    with open("jsons/ModifiedSearchOption.json", 'r', encoding='utf-8') as file:
        modified = json.load(file)
    for i in modified:
        if i['name'] == option:
            i[key] = get_option(option, key)
    with open("jsons/ModifiedSearchOption.json", 'w', encoding='utf-8') as file:
        json.dump(modified, file, ensure_ascii=False, indent='\t')