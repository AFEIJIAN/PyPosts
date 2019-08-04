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
# form of date and time:
# in digit only and date separated by dashes while time separated by colons,
# which is same as MySQL "DATETIME" data type
# YYYY-MM-DD HH:MM:SS
# example: "2019-06-09 03:05:06" if the date is 9 June 2019 and time is 03:05 AM and 6 Seconds
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
        3. posted_date (Date of the post posted, see below for more info)
        4. content (The post's content)

        for date, please refer to the comments on line 43 - line 47
    """
    def GetPostInfoById(self, id, Type):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT {} FROM posts WHERE id={}".format(Type, str(id)))
        content = cursor.fetchone()
        # when bool(content) == True, means value is found
        if bool(content):
            if Type == "posted_date":
                posted_date = "{}-{}-{} {}:{}:{}".format(
                                                        content[0].year,
                                                        content[0].month,
                                                        content[0].day,
                                                        content[0].hour,
                                                        content[0].minute,
                                                        content[0].second
                                                        )
            else:
                return content[0]
        # otherwise, None will be returned because result wasn't found
        else:
            return None


    """
    method GetPostById

    Find post according to the ID provided

    id = the post ID
    json =  1. If json is False, then a python dictionary is returned
                but if json is True, then a encoded JSON is returned
            2. Default is False
    
    Python dictionary or JSON will be returned with values below:
    1. title (The post's title)
    2. content (The post's content)
    2. posted_date (The posted date)
    3. last_modified (The last day of the post modified)
    4. author (The ID of the post's author)
    5. modified (does the post was modified? true or false only)
    6. id (Post id)
    """
    def GetPostById(self, id, json=False):
        cursor = self.mysql_conn.cursor()
        cursor.execute("SELECT title,content,posted_date,last_modified,author,modified FROM posts WHERE id={}".format(str(id)))
        result = cursor.fetchone()
        # if result is found, acquire post infos and store in dictionary
        if bool(result):
            # create a dictionary for post infos
            post = dict()
            # assign values to dictionary via assignments
            # post id
            post['id'] = id
            # post title
            post['title'] = result[0]
            # post content
            post['content'] = result[1]
            # posted date
            post['posted_date'] = "{}-{}-{} {}:{}:{}".format(
                                                        result[2].year,
                                                        result[2].month,
                                                        result[2].day,
                                                        result[2].hour,
                                                        result[2].minute,
                                                        result[2].second
                                                        )
            # last modified date
            post['last_modified'] = result[3]
            # post author
            post['author'] = result[4]
            # does post modified?, only return 0 or 1
            post['modified'] = result[5]

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


    """
    method GetAuthorById

    Find author name according to the ID provided
    id = the Author ID
    friendly = if it is true, the friendly version of the author name will be returned,
                otherwise their username is returned

    """
    def GetAuthorNameById(self, id, friendly=False):
        cursor = self.mysql_conn.cursor()
        if bool(friendly):
            cursor.execute("SELECT author FROM authors WHERE id={}".format(str(id)))
            username = cursor.fetchone()
            # if result found, author's friendly name is returned
            if bool(username):
                return username[0]
            # if result not found, None is returned
            else:
                return None
        else:
            cursor.execute("SELECT username FROM authors WHERE id={}".format(str(id)))
            author = cursor.fetchone()
            # return username if found
            if bool(author):
                return author[0]
            else:
                # as usual, return None if data not found
                return None

    # constructor / blueprint
    """
    mysql_host = Host of MySQL server
    mysql_port = Port of MySQL Server
    mysql_user = User for the database of the MySQL Server
    mysql_passwd = Password of the MySQL User
    mysql_db = Name of the MySQL Database
    """
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_passwd, mysql_db):
        self.mysql_host = mysql_host
        if bool(mysql_port):
            self.mysql_port = int(mysql_port)
        else:
            self.mysql_port = 3306
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
    This must called before closing your program
    """
    def close(self):
        self.mysql_conn.close()