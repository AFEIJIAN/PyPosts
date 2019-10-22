from pyposts import PostManager
from mysql import connector as sql

def prepare():
    return {'post_content':"My New Post stored in PyPosts framework!",
            'post_title':'My First Posts!',
            'post_id':1,
            'posted_date':'2019-08-04 12:41:00',
            'last_modified':'NULL',
            'author':1,
            'modified':0}

def insert(post):
    # according to issue #8 , this script will prompt for MySQL Server details
    conn = sql.connect(host='127.0.0.1', port=3306, user='py', passwd='py1234', database='pyposts')
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title,content,posted_date,last_modified,author,modified,id) VALUES ('{}','{}','{}',{},{},{},{})".format(post['post_title'],post['post_content'],post['posted_date'],post['last_modified'],post['author'],post['modified'],post['post_id']))
    conn.commit()
    conn.close()

def get_post():
    # according to issue #8 , this script will prompt for MySQL Server details
    pm = PostManager('127.0.0.1',3306,'py','py1234','pyposts')
    # according to issue #8, output must be user-friendly
    # testing: pm.GetPostById
    print("Testing: pm.GetPostById without json.")
    result = pm.GetPostById(1)
    if bool(result):
        for x,y in result.items():
            print(x+' : '+str(y))
    else:
        print("Result is None.")
        # according to issue #8, output must be user-friendly
    print("Testing: pm.GetPostById with json.")
    result = pm.GetPostById(1,json=True)
    if bool(result):
        print(result)
    else:
        print("Result is None.")

def get_post_id(id):
    # according to issue #8 , this script will prompt for MySQL Server details
    pm = PostManager('127.0.0.1',3306,'py','py1234','pyposts')
    # Testing: pm.GetPostInfoById
    Type = ['title','author','posted_date','content']
    for x in Type:
        print()
        # according to issue #8, output must be user-friendly
        print("Testing: pm.GetPostInfoById with Type = "+x)
        result = pm.GetPostInfoById(id, x)
        print()
        print(result)
        print()

def insert_author():
    # according to issue #8 , this script will prompt for MySQL Server details
    conn = sql.connect(host='127.0.0.1', port=3306, user='py', passwd='py1234', database='pyposts')
    cur = conn.cursor()
    cur.execute("INSERT INTO authors (author,id,username) VALUES ('test',1,'test')")
    conn.commit()
    conn.close()

def get_author():
    # according to issue #8 , this script will prompt for MySQL Server details
    pm = PostManager('127.0.0.1',3306,'py','py1234','pyposts')
    # according to issue #8, output must be user-friendly
    print("Testing pm.GetAuthorNameById with friendly=True")
    result = pm.GetAuthorNameById(1,friendly=True)
    print(result)
    # according to issue #8, output must be user-friendly
    print("Testing pm.GetAuthorNameById with friendly=False")
    result = pm.GetAuthorNameById(1,friendly=False)
    print(result)

### Post Section Test ###
post = prepare()
insert(post)
#get_post()
get_post_id(1)


### Author Section Test ###
#insert_author()
#get_author()
