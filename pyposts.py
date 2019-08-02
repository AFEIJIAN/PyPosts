from pyramid.config import Configurator
from wsgiref.simple_server import make_server
# mysql connector to interact with MySQL Server
import mysql.connector as sql
# required JSON to return post content
from json import JSONEncoder

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
    type = The requested content type, there are four types:
        1. title
        2. author (The ID of the post author)
        3. date (Date of the post posted, see below for more info)
        4. content (The post's content)

        for date, only digit and underscore is accepted, example: 09_06_2019 if the date is 9 June 2019
    """
    def GetPostInfoById(self, id, type)


    """
    method GetPostById

    Find post according to the ID provided

    id = the post ID
    json =  1. If json is False, then a python dictionary is returned
                but if json is True, then a encoded JSON is returned
            2. Default is False
    
    Value will be returned:
    1. post_title (The post's title)
    2. posted_date (The posted date)
    3. last_modified (The last day of the post modified)
    4. post_author (The ID of the post's author)
    5. modified (does the post was modified? true or false only)
    """
    def GetPostById(self, id, json=False)


    """
    method GetAuthorById

    Find author name according to the ID provided
    id = the Author ID

    """
    def GetAuthorNameByID(self, id)

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