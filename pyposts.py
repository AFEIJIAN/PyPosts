# pyramid web framework
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
# mysql connector to interact with MySQL Server
import mysql.connector as sql
# required JSON to return post content
from json import JSONEncoder
# for path modification
from os.path import dirname,abspath
# for error output
from sys import exc_info,exit

# object aren't necessary right now, commented
"""
# consist web management panel
class panel:
    # constructor
    def __init__(self, webapp_port, mysql_host, mysql_port=3306, mysql_user, mysql_passwd, mysql_db, log_file_obj):
        self.mysql_host = mysql_host
        self.mysql_port = int(mysql_port)
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_db = mysql_db
        self.webapp_port = int(webapp_port)
        conf = Configurator()
        # index = login page
        conf.add_route('index',"/")
        conf.add_view(self.index, route_name='index')
        # panel = web panel, web app
        conf.add_route('panel','/panel')
        conf.add_view(self.panel, route_name='panel')
        self.app = conf.make_wsgi_app()
    
    # listening function
    def run(self):
        self.app = make_server('127.0.0.1', self.webapp_port, self.app)
        self.app.serve_forever()
"""

# PostManager does what it said,
# it help you get the post content according to id and type
#
# form of dates:
# in digit only and separated by underscore,
# example: 09_06_2019 if the date is 9 June 2019
class PostManager:
    
    ############################
    ### Post Related Method  ###
    ############################

    """
    method GetPostInfoById

    Find post content according to the type and ID provided
    id = The Post ID
    Type = The requested content type, there are four types:
        1. title
        2. author (The ID of the post author)
        3. date (Date of the post posted, see below for more info)
        4. content (The post's content)

        for date, only digit and underscore is accepted, example: 09_06_2019 if the date is 9 June 2019
    """
    def GetPostInfoById(self, id, Type):
        # check if MySQL server connection is still established
        if self.mysql_conn.is_connected:
            cursor = self.mysql_conn.cursor()
            cursor.execute("SELECT {} FROM Posts WHERE id={}".format(Type, str(id)))
            content = cursor.fetchone()
            # when bool(content) == True, means value is found
            if bool(content):
                return content[0]
            # otherwise, None will be returned because result wasn't found
            else:
                return None
        else:
            # raise error if MySQL Server has disconnected
            raise Exception("MySQL Server has been disconnected.")


    """
    method GetPostById

    Find post according to the ID provided

    id = the post ID
    json =  1. If json is False, then a python dictionary is returned
                but if json is True, then a encoded JSON is returned
            2. Default is False
    
    Value will be returned:
    1. title (The post's title)
    2. content (The post's content)
    2. posted_date (The posted date)
    3. last_modified (The last day of the post modified)
    4. author (The ID of the post's author)
    5. modified (does the post was modified? true or false only)
    """
    def GetPostById(self, id, json=False):
        if self.mysql_conn.is_connected():
            cursor = self.mysql_conn.cursor()
            cursor.execute("SELECT title,posted_date,last_modifed,author,modified FROM Posts WHERE id={}".format(str(id)))
            result = cursor.fetchone()
            if bool(result):
                try:
                    # this post's content storage is TEMPORARY only, planned to archive whole post content and infos
                    # post content's file is saved with id as the name of file with extension '.pypt'
                    #
                    # then all post files is stored in folder 'posts' from parent folder 'pyposts' which is under the same directory
                    post_content = open(dirname(abspath(__file__))+'/pyposts/posts/{}.pypt'.format(str(id)),'r').read()
                
                # if current process's user can't access to file, return None and output Error MSG
                except FileNotFoundError:
                    print(exc_info())
                    return None
                
                # if current process's user can't access to file, return None and output Error MSG
                except PermissionError:
                    print(exc_info())
                    return None
 
                # create a dictionary for post infos
                post = dict()
                # assign values to dictionary via assignments
                # post id
                post['id'] = id
                # post title
                post['title'] = result[0]
                # post content
                post['content'] = post_content
                # posted date
                post['posted_date'] = result[1]
                # last modified date
                post['last_modified'] = result[2]
                # post author
                post['author'] = result[3]
                # does post modified?
                post['modified'] = result[4]

                # if json=True, encode to json string
                if json:
                    post_json = JSONEncoder(indent=4).encode(post)
                    return post_json

                else:
                    # otherwise just return the python dictionary
                    return post
            else:
                # same as method above, None will be returned if result isn't found
                return None
        else:
            raise Exception("MySQL Server has been disconnected.")


    """
    method GetAuthorById

    Find author name according to the ID provided
    id = the Author ID

    """
    def GetAuthorNameByID(self, id):
        if self.mysql_conn.is_connected:
            cursor = self.mysql_conn.cursor()
            cursor.execute("SELECT name FROM Authors WHERE id={}".format(str(id)))
            author = cursor.fetchone()
            # return author name if found
            if bool(author):
                return author[0]
            else:
                # as usual, return None if data not found
                return None
        else:
            raise Exception("MySQL Server has been disconnected.")

    # constructor / blueprint
    """
    mysql_host = Host of MySQL server
    mysql_port = Port of MySQL Server
    mysql_user = User for the database of the MySQL Server
    mysql_passwd = Password of the MySQL User
    mysql_db = Name of the MySQL Database
    """
    def __init__(self, mysql_host, mysql_port=3306, mysql_user, mysql_passwd, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_port = int(mysql_port)
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_db = mysql_db
        self.mysql_conn = sql.connect(host=self.mysql_host,
                                 port=self.mysql_port,
                                 user=self.mysql_user,
                                 passwd=self.mysql_passwd,
                                 database=self.mysql_db)
    
    """
    method close, close the PostManager

    Actually this is just a method to tell that PostManager can be stopped
    what it does was just close the MySQL Server connection object
    This must be called before closing your program
    """
    def close(self):
        self.mysql_conn.close()