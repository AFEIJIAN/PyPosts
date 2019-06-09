"""Two processing types

1. Pre-Process
2. Request processing

"""
from sys import exc_info
import mysql.connector as sql

def pre(server_obj, auth_key):
    try:
        conn = sql.connect(
            host=server_obj.mysql_host,
            port=server_obj.mysql_port,
            user=server_obj.mysql_user,
            passwd=server_obj.mysql_passwd,
            database=server_obj.mysql_db
        )

    except Exception:
        print("Error occured while trying to connect to MySQL Server: \n{}".exc_info())
        # return user
        return None

    cursor = conn.cursor()
    cursor.execute('SELECT auth_key,username FROM users WHERE auth_key="{}"'.format(auth_key))

    try:
        result = cursor.fetchone()

    # catch unread result error
    except sql.errors.InternalError:
        conn.close()
        # return user
        return "ERR_MULTI_USER"

    if result[0] == auth_key:
        conn.close()
        # return user
        return result[1]

    else:
        conn.close()
        # return user
        return "USER_NOT_FOUND"

#def process():