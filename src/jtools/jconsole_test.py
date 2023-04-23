import jconsole as jc
import json

import os.path
BASEDIR = os.path.dirname(__file__)


with open(os.path.join(BASEDIR, '../../resources/mixed_list_dict.json'), 'r') as f:
    mixed_list_dict = json.load(f)

with open(os.path.join(BASEDIR, '../../resources/deep_nested_dict.json'), 'r') as f:
    deep_nested_dict = json.load(f)

with open(os.path.join(BASEDIR, '../../resources/list of dictionaries.json'), 'r') as f:
    list_of_dicts = json.load(f)


jc.test(mixed_list_dict)

jc.test(list_of_dicts)

jc.test(deep_nested_dict)
 