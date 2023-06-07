import pymysql
from dotenv import load_dotenv
import os 
from tgbot import send_msg 
load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD_2')
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

def insert_token(table_name,token,prompt):
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
            sql = f"INSERT INTO {table_name} (prompt,token_count) VALUES ('{prompt}',{token})"
            cursor.execute(sql)
            connection.commit()
            print("資料插入成功！")
            break

        except Exception as err :
            # print(err)
            err_code,err_msg = err.args 
            if str(err_code) == "1146" : 
                sql_2 = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, prompt LONGTEXT ,   token_count int,  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
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


def search_id(table_name,prompt):
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

        sql = f"SELECT ID from {table_name} where prompt REGEXP '{prompt}'"

        cursor.execute(sql)
        results= cursor.fetchall()

        if results : 
            for result in results : 
                print(result[0])
        
        else : 
            print("Desn't exits.")
    
    except Exception as e :
        print("搜尋資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()


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


if __name__ == "__main__":
    # change_info('TEST22_train','後天去哪','JCpark','3')
    # insert_info('Bosco_train','晚餐吃什麼','還沒想好')
# search_id("JLB_train",'.*是誰.*')
    # print(get_maxid("TEST20_train"))
    # print(insert_token('test123',333))
    pass