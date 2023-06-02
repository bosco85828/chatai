import pymysql
from dotenv import load_dotenv
import os 

load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD')
print(SQL_PASSWORD)
def insert_info(table_name,prompt,completion):
    # 建立與 MySQL 伺服器的連接
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password=SQL_PASSWORD,
        database='chatai'
    )

    # 創建 cursor 對象
    cursor = connection.cursor()

    # 定義插入資料的 SQL 語句
    sql = f"INSERT INTO {table_name} (prompt, completion) VALUES ('{prompt}', '{completion}')"

    # 插入的資料值
    # data = ('Hello', 'World')
    while True : 
        try:
            # 執行 SQL 語句並插入資料
            cursor.execute(sql)

            # 提交事務
            connection.commit()

            print("資料插入成功！")
            break

        except Exception as e:

            if "doesn't exist" in str(e) : 
                sql_2 = f"CREATE TABLE {table_name} (   id INT AUTO_INCREMENT PRIMARY KEY,   prompt LONGTEXT,   completion LONGTEXT,   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )"
                cursor.execute(sql_2)
                connection.commit()
                print(f"{table_name} 不存在，已創建該表。")
                continue

            # 發生錯誤時回滾事務
            connection.rollback()
            print("資料插入失敗：", str(e)) 
            break
    
    # 關閉 cursor 和連接
    cursor.close()
    connection.close()

def get_maxid(table_name):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password=SQL_PASSWORD,
        database='chatai'
    )
    try : 
        cursor = connection.cursor()
        sql = f"SELECT COUNT(ID) FROM {table_name}"
        cursor.execute(sql)
        result=cursor.fetchone()

        if result : 
            count=result[0]
            print(count)
            return count

        else : 
            print("表格中沒有資料")

    except Exception as err : 
        print("查詢資料時發生錯誤：", str(err))

    finally:
        cursor.close()
        connection.close()


def search_id(table_name,prompt):
    # 建立與 MySQL 伺服器的連接
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password=SQL_PASSWORD,
        database='chatai'
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
        host='127.0.0.1',
        user='root',
        password=SQL_PASSWORD,
        database='chatai'
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

if __name__ == "__main__":
    change_info('JLB_train','這是修改過後的','修改的id3','3')
# insert_info('Bosco_train','晚餐吃什麼','還沒想好')
# search_id("JLB_train",'.*是誰.*')
    # get_maxid("JLB_train")