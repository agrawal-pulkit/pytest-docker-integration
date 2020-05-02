import time
import MySQLdb
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def db_connection():
    try:
        db_conn = MySQLdb.connect(host='mysql',user='ipa',passwd='password',db='ipa')
        cursor = db_conn.cursor()
        return db_conn,cursor
    except MySQLdb.Error as e:
        print("Exception in db connection: ", e)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def add(a, b):
    return a+b

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/mysql')
def hello_mysql():
    _, cursor = db_connection()
    print("cursor: ", cursor)
    sql = "show tables"
    cursor.execute(sql)
    fetch_data = cursor.fetchall()
    return 'TABELS : {}\n'.format(fetch_data)