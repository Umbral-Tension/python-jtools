import jconsole as jc
import json

import os.path
BASEDIR = os.path.dirname(__file__)
filepath = os.path.join(BASEDIR, 'list of dictionaries.json')
with open(filepath, 'r') as f:
    samp = json.load(f)

#fix handling of set objects, fix indent multiply by 0 problem
#jc.test('candor', [2, 3, ['a', 'b', 'c'], 4, 6], {'apple': 'camp'})

jc.test(samp)


 