import subprocess
from dotenv import load_dotenv
import openai
import os 
import shutil
import time
from tgbot import send_msg 

load_dotenv()
path=os.getcwd()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
while True : 
    models = openai.Model.list()
    sorted_models = sorted(models['data'], key=lambda x: int(x['created']))
    model_name=sorted_models[-1]['id']
    # "openai api fine_tunes.create -t /Users/user/Downloads/bot_data_prepared_v2.jsonl -m davinci --suffix "qq-faq-v1.1" --batch_size 32 --learning_rate_multiplier 0.05"
    cmd=['openai', 'api','fine_tunes.create', '-t',f'{path}/data2.jsonl','-m',model_name,'--suffix','qq-faq','--n_epochs','10','--learning_rate_multiplier','0.4']
    timeout_seconds=300
    try:
        with open(f'{path}/data.jsonl') as f : 
            data=f.readlines()
    except FileNotFoundError : 
        time.sleep(900)
        continue

    except Exception as err : 
        send_msg(err)
        time.sleep(900)
        continue

    if data : 
        print(123)
        source_file = f"{path}/data.jsonl"
        destination_file = f"{path}/data2.jsonl"
        shutil.copy2(source_file, destination_file)
        with open(f'{path}/data.jsonl','w') as f : pass 

        try:    
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 等待程序完成，並在超時時間到達時強制終止
            stdout, stderr = process.communicate(timeout=timeout_seconds)

            result=stdout.decode().split('\n')
            print(result)
            send_msg(result)
            # 檢查程序是否成功執行
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd, stdout, stderr)
            

        except subprocess.TimeoutExpired:
            # 如果程序超時，則終止程序並顯示一條錯誤消息
            process.kill()
            print(f"Timeout reached for command: {' '.join(cmd)}")
            

        except subprocess.CalledProcessError as e:
            # 如果程序返回非零退出代碼，則顯示錯誤消息和詳細信息
            print(f"Error running command: {' '.join(cmd)}")
            print(f"Return code: {e.returncode}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")


        except Exception as e:
            # 其他錯誤處理
            print(f"Error: {str(e)}")

    time.sleep(900)            
