import time
import datetime

while True:
    now = datetime.datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    print(date_time)
    time.sleep(15)