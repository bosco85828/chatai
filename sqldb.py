import pymysql
from dotenv import load_dotenv
import os 
from tgbot import send_msg 
import secrets

load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD')
SQL_DOMAIN=os.getenv('SQL_DOMAIN')
print(SQL_PASSWORD)


def insert_info(table_name,prompt,completion):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )

    # # 創建 cursor 對象
    # cursor = connection.cursor()

    # # 定義插入資料的 SQL 語句
    # sql = f"INSERT INTO {table_name} (prompt, completion) VALUES ('{prompt}', '{completion}')"

    # 插入的資料值
    # data = ('Hello', 'World')
    while True : 
        try:
            cursor = connection.cursor()
            sql = f"INSERT INTO {table_name} (prompt, completion) VALUES ('{prompt}', '{completion}')"
            # 執行 SQL 語句並插入資料
            cursor.execute(sql)

            # 提交事務
            connection.commit()

            print("資料插入成功！")
            break

        except Exception as e:
            # print('test123')
            # if "doesn't exist" in str(e) : 
            #     sql_2 = f"CREATE TABLE {table_name} (   id INT AUTO_INCREMENT PRIMARY KEY,   prompt LONGTEXT,   completion LONGTEXT,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )"
            #     cursor.execute(sql_2)
            #     connection.commit()
            #     print(f"{table_name} 不存在，已創建該表。")
            #     continue

            # 發生錯誤時回滾事務
            # connection.rollback()
            print("資料插入失敗：", str(e)) 
            send_msg("資料插入失敗："+str(e))
            cursor.close()
            connection.close()
            break
    
    # 關閉 cursor 和連接
    cursor.close()
    connection.close()

def insert_token(table_name,token,prompt,completion):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    while True : 
        try : 
            cursor = connection.cursor()
            sql = f"INSERT INTO {table_name} (prompt,completion,token_count) VALUES ('{prompt}','{completion}',{token})"
            cursor.execute(sql)
            connection.commit()
            print("資料插入成功！")
            break

        except Exception as err :
            # print(err)
            err_code,err_msg = err.args 
            if str(err_code) == "1146" : 
                sql_2 = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, prompt LONGTEXT , completion LONGTEXT ,   token_count int, chatroom_id varchar ,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
                cursor.execute(sql_2)
                connection.commit()
                print(f"{table_name} 不存在，已創建該表。")
                continue
            
            else : 
                connection.rollback()
                print("資料插入失敗：", str(err)) 
                send_msg("資料插入失敗："+str(err))
                cursor.close()
                connection.close()
                break

    # 關閉 cursor 和連接
    cursor.close()
    connection.close()
            

def del_tables():
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    try : 
        cursor = connection.cursor()
        sql = f"show tables"
        cursor.execute(sql)
        tables=cursor.fetchall()
        print(tables)
        if tables : 
            for table in tables:
                table_str=table[0]
                sql=f"delete from {table_str} where DATE(created_at) <= DATE_SUB(CURDATE(),INTERVAL 15 day)"
                cursor.execute(sql)
                print(table_str + "刪除成功")
            connection.commit()
            print("刪除以下 table 超過 15 天資料:{}".format(tables))


    except Exception as err : 
        
        
        error_code,error_msg=err.args
        print(error_code)
        print(err)
        

    finally:
        cursor.close()
        connection.close()


def get_maxid(table_name):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    try : 
        cursor = connection.cursor()
        sql = f"SELECT COUNT(ID) FROM {table_name}"
        cursor.execute(sql)
        result=cursor.fetchone()

        if result : 
            count=result[0]
            # print(count)
            return count

        else : 
            print("表格中沒有資料")

    except Exception as err : 
        print(type(err.args))
        
        error_code,error_msg=err.args
        print(error_code)
        print("查詢資料時發生錯誤：", str(err))
        send_msg("查詢資料時發生錯誤："+str(err))
        if str(error_code) == "1146" : 
            sql_2 = f"CREATE TABLE {table_name} (   id INT AUTO_INCREMENT PRIMARY KEY,   prompt LONGTEXT,   completion LONGTEXT,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )"
            cursor.execute(sql_2)
            connection.commit()
            print(f"{table_name} 不存在，已創建該表。")

        

    finally:
        cursor.close()
        connection.close()


def search_context(table_name,chatroom_id):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )

    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()

        sql = f"SELECT prompt,completion from {table_name} where chatroom_id = '{chatroom_id}' order by created_at ASC"

        cursor.execute(sql)
        results= cursor.fetchall()
        # print(results)
        context=[]
        if results : 
            for result in results : 
                # msg={
                #     'user':{"role": "user", "content": result[0]},
                #     'assistant':{"role": "assistant", "content": result[1] },
                # }
                context.append({"role": "user", "content": result[0]})
                context.append({"role": "assistant", "content": result[1]})
                

                # print('prompt:'+result[0])
                # print('completion:'+result[1])
        
        else : 
            print("Desn't exits.")
            return None
    
    except Exception as e :
        print("搜尋資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()
    
    return context 


def change_info(table_name,prompt,completion,_id):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()
        sql=f"UPDATE {table_name} SET prompt='{prompt}', completion='{completion}' WHERE ID={_id}"

        cursor.execute(sql)
        connection.commit()

        print("成功修改")
    
    except Exception as err :
        connection.rollback()
        print("修改資料時發生錯誤：", str(err))

    finally : 
        cursor.close()
        connection.close()


def get_total_token(table_name):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    sql=f"select sum(token_count) as total_token from {table_name} "
    cursor.execute(sql)
    result=cursor.fetchone()
    if result : 
        print(result[0])


def generate_chatroom_id(length,table_name):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='chatai',
        charset='utf8mb4'
    )
    
    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()
        while True : 
            chatroom_id = secrets.token_hex(length)  
            sql = f"SELECT * from {table_name} where chatroom_id = '{chatroom_id}' order by created_at ASC"

            cursor.execute(sql)
            results= cursor.fetchall()
            # print(results)
            
            if results : 
                continue 
            
            else : 
                break
    
    except Exception as e :
        print("搜尋資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()
    
    return chatroom_id

if __name__ == "__main__":
    # print(search_context("JLB_token",'d40116b1eb2bea69'))
    # print(search_id("JLB_token",'d40116b1eb29'))
    # print(insert_token('JLB_token',token=255,prompt='早餐吃什麼',completion='義大利麵',chatroom_id='a3382732d882df65'))
    # print(insert_token('JLB_token',token=255,prompt='午餐吃什麼',completion='炒飯',chatroom_id='a3382732d882df65'))
    # print(insert_token('JLB_token',token=255,prompt='晚餐吃什麼',completion='雞胸肉',chatroom_id='a3382732d882df65'))
    # print(generate_chatroom_id(length=8,table_name='JLB_token'))
    # change_info('TEST22_train','後天去哪','JCpark','3')
    # insert_info('Bosco_train','晚餐吃什麼','還沒想好')
# search_id("JLB_train",'.*是誰.*')
    # print(get_maxid("TEST20_train")) 
    # print(insert_token('test123',333))
    pass