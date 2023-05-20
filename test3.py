import os 
with open('test.txt') as f : 
    data=f.readlines()
    for i in range(len(data)) :
        with open(f'{i}.txt','w+') as t : 
            t.write(data[i])
