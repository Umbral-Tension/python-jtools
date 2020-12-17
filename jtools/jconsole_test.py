import jconsole as jc
import json


with open('./sample.json', 'r') as f:
    samp = json.load(f)

#fix handling of set objects, fix indent multiply by 0 problem
#jc.test('candor', [2, 3, ['a', 'b', 'c'], 4, 6], {'apple': 'camp'})

jc.test(jc.dir_('teststring'))


 