import shutil
source_file = "/Users/user/Desktop/script/chatai/data.jsonl"
destination_file = "/Users/user/Desktop/script/chatai/data2.jsonl"
shutil.copy2(source_file, destination_file)
with open('data.jsonl','w') as f : pass 
