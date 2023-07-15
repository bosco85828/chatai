import time
import schedule
from datetime import datetime, timezone , timedelta
from sqldb import del_tables

if __name__ == "__main__" : 
    schedule.every().day.at("00:00").do(del_tables)

    while True : 
        schedule.run_pending()
        time.sleep(60)