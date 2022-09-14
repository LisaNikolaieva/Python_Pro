import datetime
import resize
import time

from celery import Celery
import sqlite3


app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def task1(image_path):
    resize.resizer(image_path)
    con = sqlite3.connect("db1.db")
    cur = con.cursor()
    cur.execute(f"""UPDATE task_state SET status='done' WHERE file_name='{image_path}' """)
    con.commit()
    con.close()

    return True
