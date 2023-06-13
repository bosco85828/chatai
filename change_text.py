import os 
import json
with open('JLB.txt') as f : 
    data=f.readlines()
    for i in range(len(data)) :
        with open(f'JLB-rawdata/{i}.txt','w+') as t : 
            text=json.loads(data[i])
            t.write('{}\n'.format(text['prompt']))
            t.write('{}\n'.format(text['completion']))
