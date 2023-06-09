import os 
import json
with open('YZ.txt') as f : 
    data=f.readlines()
    for i in range(len(data)) :
        with open(f'YZ-rawdata/{i}.txt','w+') as t : 
            text=json.loads(data[i])
            t.write('{}\n'.format(text['prompt']))
            t.write('{}\n'.format(text['completion']))
