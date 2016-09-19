import pymysql

def connection():
    conn = pymysql.connect(host='localhost',
                           database='flask',
                           user='root',
                           password='mysql123')
    c = conn.cursor()

    return c, conn
