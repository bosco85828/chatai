import json
import pymysql
from dotenv import load_dotenv
import os 
import time
from datetime import datetime , timezone , timedelta
import requests

load_dotenv()

SQL_PASSWORD=os.getenv('SQL_PASSWORD')
SQL_DOMAIN=os.getenv('SQL_DOMAIN')
TG_TOKEN=os.getenv('TG_TOKEN')
TG_CHAT=os.getenv('CHATAI_TG_CHAT')


# print(SQL_PASSWORD)

table_name_list=[ "ETY_token" , "JLB_token" , "YZ_token" , "PYQ_token" , "SYTY_token"]

def get_total_token(table_name):
    connection = pymysql.connect(
            host=SQL_DOMAIN,
            user='root',
            password=SQL_PASSWORD,
            database='chatai',
            charset='utf8mb4'
        )
    cursor = connection.cursor()
    # sql=f"select sum(token_count) as total_token from {table_name} "
    sql=f"select sum(token_count) from {table_name} where DATE(created_at) = '{yesterday}'"
    try : cursor.execute(sql)
    except Exception as err : 
        print(err)
        return err

    result=cursor.fetchone()
    print(result)
    if result : 
        return str(result[0])
    
    else : 
        return None 
    

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
    global yesterday
    while True : 
        yesterday=(datetime.now(timezone.utc)- timedelta(days=1)).strftime('%Y-%m-%d')
        # yesterday=datetime.now(timezone.utc).strftime('%Y-%m-%d')
        result_dict={}    
        for table in table_name_list : 
            result=get_total_token(table)
            result_dict[table]=result
        
        str_result_dict=json.dumps(result_dict).replace(',','\n')
        msg=f"""
    以下為 AIchat 各商戶 {yesterday} 使用總 Token:
    {str_result_dict} """

        print(msg)
        send_msg(msg)

        time.sleep(86400)


        

