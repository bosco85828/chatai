import requests
from dotenv import load_dotenv
import os 

load_dotenv()
TG_TOKEN=os.getenv('TG_TOKEN')
TG_CHAT=os.getenv('TG_CHAT')

def send_msg(msg):
    # 填入 Bot 的 token
    token = TG_TOKEN
    # 填入頻道 ID 
    chat_id= TG_CHAT
    
    url=f"https://api.telegram.org/bot{token}/sendMessage?"
    data={
        "chat_id":chat_id,
        "text":msg
    }

    result=requests.post(url,json=data).json()
    return result

if __name__ == "__main__":
    
    send_result=send_msg("test")
    print(send_result)
    if not send_result['ok']:
        print(send_result['description'])




