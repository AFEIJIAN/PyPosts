import mysql.connector as sql
from getpass import getpass

def create(mysql_conn):
    cur = mysql_conn.cursor()
    print("Creating table 'posts'.")
    cur.execute("create table posts ( \
    id int, \
    str_id varchar(255), \
    author int, \
    title TEXT, \
    content LONGTEXT, \
    posted_date DATETIME, \
    last_modified DATETIME, \
    modified tinyint(1)) \
                ")
    print("Creating table 'authors'.")
    cur.execute("create table authors (id int, username TEXT, author TEXT)")
    mysql_conn.commit()
    print("Tables created, proceeding to closing connection.")
    mysql_conn.close()
    print("Your MySQL DB is ready!")

print("""Welcome to MySQL DB setup tool for PyPosts! Make sure your MySQL server and database are within condition below:
MySQL Server
1. Accessible
2. Not a remote server (Localhosted)
3. Database user is accessible

MySQL DB
1. Database user is accessible
2. Database user has read and write permission
3. Database user can create tables

Press enter if you are done, press ctrl+c if you haven't done yet!
""")
input()
print("Seems you are ready! Right now we need some information about your MySQL Server!")
print("MySQL Server Host is default to '127.0.0.1', PyPosts doesn't support remote server right now!")
mysql_port = int(input("Your MySQL Server Port, default is 3306: "))
mysql_user = input("Your MySQL DB User's username: ")
if bool(mysql_user) != True:
    raise ValueError("MySQL DB User's username can't be empty!")
print("MySQL DB User's Password")
mysql_passwd = getpass(prompt="Input is hidden so just type it and enter: ")
mysql_db = input("Your MySQL DB Name: ")
if bool(mysql_db) != True:
    raise ValueError("MySQL DB Name can't be empty!")

mysql_conn = sql.connect(host='127.0.0.1',
                        port=mysql_port,
                        user=mysql_user,
                        passwd=mysql_passwd,
                        database=mysql_db
                        )
create(mysql_conn)