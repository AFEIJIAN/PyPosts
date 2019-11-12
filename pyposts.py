# pyramid web framework, not using right now
#from pyramid.config import Configurator
#from wsgiref.simple_server import make_server

# mysql connector to interact with MySQL Server
import mysql.connector as sql
# required JSON to return post content
from json import JSONEncoder
# for path modification
from os.path import dirname,abspath
# for error output
from sys import exc_info,exit
# datetime object, used for post writing and data type verification
from datetime import datetime as dt

# object panel aren't necessary right now, commented
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
# which is same as MySQL "DATETIME" data type, please refer to MySQL Documentation
# YYYY-MM-DD HH:MM:SS
# example: "2019-06-09 03:05:06" if the date is 9 June 2019 and time is 03:05:06 AM
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

        for date, please refer to the comments on line 43 - line 50
    """
    def GetPostInfoById(self, id, Type):
        cursor = self.mysql_conn.cursor(buffered=True)
        cursor.execute("SELECT {} FROM posts WHERE id={}".format(Type, str(id)))
        
        content = cursor.fetchone()

        # when bool(content) == True, means value is found
        if bool(content):
            # if result is a date, change its microsecond to 0 and convert it into string
            if Type == "posted_date":
                posted_date = str(content[0].replace(microsecond=0))
                # close the cursor first to clear buffer
                cursor.close()
                return posted_date

            else:
                # close the cursor first to clear buffer
                cursor.close()
                return content[0]

        # otherwise, None will be returned because result wasn't found
        else:
            # close the cursor first to clear buffer
            cursor.close()
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
        cursor = self.mysql_conn.cursor(buffered=True)
        cursor.execute("SELECT str_id,title,content,posted_date,last_modified,author,modified FROM posts WHERE id={}".format(str(id)))
        # fetch result
           result = cursor.fetchone()
        
        # if result is found, acquire post infos and store in dictionary
        if bool(result):
            # create a dictionary for post infos
            post = dict()
            # assign values to dictionary via assignments
            # post id
            post['id'] = id
            # post string id
            post['str_id'] = result[0]
            # post title
            post['title'] = result[1]
            # post content
            post['content'] = result[2]
            # posted date, will change microsecond to 0 at the same time
            post['posted_date'] = str(result[3].replace(microsecond=0))
            # last modified date
            post['last_modified'] = result[4]
            # post author
            post['author'] = result[5]
            # does post modified?, only return 0 or 1
            if result[6] == 1:
                # if it is 1, it means True
                post['modified'] = True
            elif result[6] == 0:
                # if it is 0, it means False
                post['modified'] = False
            else:
                # otherwise, it would be None (invalid value)
                post['modified'] = None

            # if json=True, encode to json string
            if json:
                post_json = JSONEncoder(indent=4).encode(post)
                # close the cursor first to clear buffer
                cursor.close()
                return post_json

            else:
                # otherwise just return the python dictionary
                # close the cursor first to clear buffer
                cursor.close()
                return post
        else:
            # same as method above, None will be returned if result isn't found
            # close the cursor first to clear buffer
            cursor.close()
            return None



    """
    method GetPostByPostedDate
    Return posts with amounts request via Python Dictionary or JSON
    
    1. date, must be a Python's datetime.datetime object
    2. amount, amount of post required, if not provided, unlimited result will be returned
    3. json, result will encode into JSON string if json=True, default is False
    """
    def GetPostByPostedDate(self, date, amount, json=False):
        # data type checks for arguments
        if isinstance(date, dt) == False:
            # raise error if invalid
            raise TypeError("Date must be a valid datetime object.")
        if isinstance(amount, int) == False:
            # raise error if invalid
            raise TypeError("Amount must be an integer.")

        cursor = self.mysql_conn.cursor(buffered=True)
        # convert Python's datetime into string form (which is compatible with MySQL DATETIME)
        # and change it's microsecond to 0
        date = str(date.replace(microsecond=0))
        cursor.execute("SELECT id,str_id,title,content,posted_date,last_modified,author,modified FROM posts WHERE posted_date <= {}".format(date))
        # fetch result
        result = cursor.fetchall()
        
        # if result is found, count if results is more or less than requested
        if bool(result):
            result_count = len(result)
            # if result is more than requested
            posts = dict()
            if result_count > amount:

                # will not remove unwanted results from list right now, because this function will
                # not occupy large memory for a long time (in case result is large)
                # but unwanted result removal might support in the future releases

                # assign post information to the nested dict's keys
                for loop in range(result_count):
                    # convert date into string
                    # will change microsecond to 0 at the same time
                    result[loop][4] = str(result[loop][4].replace(microsecond=0))

                    # check if last_modified date is None or not
                    if bool(result[loop][5]) != True or result[loop][5] != None:
                        # if not means it is a valid date, convert it to string then
                        # will change microsecond to 0 at the same time
                        result[loop][5] = str(result[loop][5].replace(microsecond=0))
                    else:
                        # otherwise, change it's value into None
                        result[loop][5] = None

                    # create a nested dictionary
                    posts[result[loop][4]] = dict()
                    # make a pointer (reference) of the nested dictionary for easier code reading
                    cur_post = posts[result[loop][4]]

                    # assign post information to the nested dict's keys
                    # post id
                    cur_post['id'] = result[loop][0]
                    # post string id
                    cur_post['str_id'] = result[loop][1]
                    # post title
                    cur_post['title'] = result[loop][2]
                    # post content
                    cur_post['content'] = result[loop][3]
                    # post's posted date
                    cur_post['posted_date'] = result[loop][4]
                    # post's last modified date
                    cur_post['last_modified'] = result[loop][5]
                    # post author, represented by their ids
                    cur_post['author'] = result[loop][6]
                    # post modified attribute
                    if result[loop][7] == 1:
                        # if it is 1, means true
                        cur_post['modified'] = True
                    elif result[loop][7] == 0:
                        # if it is 0, means false
                        cur_post['modified'] = False
                    else:
                        # otherwise, it is None (Invalid value)
                        cur_post['modified'] = None

                    # if list index reached the post amount requested, break the loop
                    if loop == (amount-1):
                        break



            # elif result is equal to or less than requested
            elif result_count <= amount:
                for x in result:
                    # convert datetime object into string
                    # will change their microsecond to 0 at the same time
                    # posted_date
                    x[4] = str(x[4].replace(microsecond=0))
                    # checks if last_modified is None or a valid date
                    if bool(x[5]) == True or x[5] != None:
                        # if it is a valid date, convert it into a string
                        x[5] = str(x[5].replace(microsecond=0))


                    # create a nested dictionary
                    posts[x[4]] = dict()
                    # make a pointer (reference) of the current nested dictionary
                    cur_post = posts[x[4]]

                    # assign post information to the nested dict's keys
                    # post id
                    cur_post['id'] = x[0]
                    # post string id
                    cur_post['str_id'] = x[1]
                    # post title
                    cur_post['title'] = x[2]
                    # post content
                    cur_post['content'] = x[3]


                    # post's posted date
                    cur_post['posted_date'] = x[4]
                    # post's last modified date
                    cur_post['last_modified'] = x[5]
                    # post author
                    cur_post['author'] = x[6]
                    # post modified attribute (True or False)
                    if x[7] == 1:
                        # if it is 1, it means True
                        cur_post['modified'] = True
                    elif x[7] == 0:
                        # if it is 0, it means False
                        cur_post['modified'] = False
                    else:
                        # otherwise, it means None (invalid value)
                        cur_post['modified'] = None

            # if json=True, encode to json string
            if json:
                posts_json = JSONEncoder(indent=4).encode(posts)
                # close the cursor first to clear buffer
                cursor.close()
                return posts_json

            else:
                # otherwise just return the python dictionary
                # close the cursor first to clear buffer
                cursor.close()
                return posts
        else:
            # same as method above, None will be returned if result isn't found
            # close the cursor first to clear buffer
            cursor.close()
            return None
    

    """
    method GetPostByModifiedDate

    Get post according to the modified date (date) provided
    date = Modified date, it must be a Python.datetime.datetime object
    amount = Amount of posts needed
    json = If set to True, result will convert into JSON string,
            otherwise Python dictionary will be returned

    This function will return Python dictionary which contains all
    posts information, or JSON string if json is set to True

    In case no posts were found, None will be returned
    """
    def GetPostByModifiedDate(self, date, amount, json=False):
        # data type checks for arguments
        if isinstance(date, dt) == False:
            # raise error if invalid
            raise TypeError("Date must be a valid datetime object.")
        if isinstance(amount, int) == False:
            # raise error if invalid
            raise TypeError("Amount must be an integer.")
        
        cursor = self.mysql_conn.cursor(buffered=True)
        # replace microsecond to 0 and change date object into string
        date = str(date.replace(microsecond=0))
        # execute query
        cursor.execute("SELECT id,str_id,title,author,content,posted_date,last_modified,modified FROM posts WHERE last_modified <= '{}'".format(date))

        # fetch all result
        result = cursor.fetchall()

        # if result found
        if bool(result):
            result_count = len(result)
            # if result is more than requested
            # create a dict to store posts
            posts = dict()
            if result_count > amount:
                for loop in range(result_count):                    
                    # create a nested dict in it
                    posts[result[loop][7]] = dict()
                    # make a pointer (reference) of it for easier code reading
                    cur_post = posts[result[loop][7]]

                    # convert dates into strings
                    # and change their microsecond to 0
                    
                    # posted_date
                    result[loop][5] = str(result[loop][5].replace(microsecond=0))

                    # check if last_modified is a valid date
                    if bool(result[loop][6]) == True or result[loop][6] == None:
                        # if it is not None, then it is a valid date
                        # convert it into string then
                        result[loop][6] = str(result[loop][6].replace(microsecond=0))

                    else:
                        # otherwise it must be a None or invalid value,
                        # just call it None
                        result[loop][6] = None

                    # assign the post information to the nested dict's keys
                    # post id
                    cur_post['id'] = result[loop][0]
                    # post string id
                    cur_post['str_id'] = result[loop][1]
                    # post title
                    cur_post['title'] = result[loop][2]
                    # post author
                    cur_post['author'] = result[loop][3]
                    # post content
                    cur_post['content'] = result[loop][4]
                    # post's posted date
                    cur_post['posted_date'] = result[loop][5]
                    # post's last modified date
                    cur_post['last_modified'] = result[loop][6]

                    # post modified attribute
                    if result[loop][7] == 1:
                        # if it is 1, means true
                        cur_post['modified'] = True
                    elif result[loop][7] == 0:
                        # if it is 0, means false
                        cur_post['modified'] = False
                    else:
                        # otherwise, it is None (Invalid value)
                        cur_post['modified'] = None
                    
                    # if list index reached request amount, break the loop
                    if loop == (amount-1):
                        break

            # if result is same or less than requested
            elif result_count <= amount:
                for x in result:
                    # create a nested dict
                    posts[x[7]] = dict()
                    # make a pointer (reference) of it for easier code reading
                    cur_post = posts[x[7]]

                    # convert dates into string and
                    # change their microsecond to 0 at the same time
                    # posted_date
                    x[5] = str(x[5].replace(microsecond=0))

                    # check if last_modified is a valid datetime object
                    if bool(x[6]) == True or x[6] != None:
                        # if it is not None, then it is a valid date
                        # convert it into string then
                        x[6] = str(x[6].replace(microsecond=0))

                    else:
                        # otherwise it must be a None or invalid value,
                        # just call it None
                        x[6] = None

                    # assign post information to the nested dict's keys
                    # post id
                    cur_post['id'] = x[0]
                    # post string id
                    cur_post['str_id'] = x[1]
                    # post title
                    cur_post['title'] = x[2]
                    # post author
                    cur_post['author'] = x[3]
                    # post content
                    cur_post['content'] = x[4]
                    # post's posted date
                    cur_post['posted_date'] = x[5]
                    # post's last modified date
                    cur_post['last_modified'] = x[6]

                    # post modified attribute
                    if x[7] == 1:
                        # if it is 1, means true
                        cur_post['modified'] = True
                    elif x[7] == 0:
                        # if is is 0, means false
                        cur_post['modified'] = False
                    else:
                        # otherwise, it is a invalid value so we called it None
                        cur_post['modified'] = None


            if json:
                # if json set to True, convert it into JSON string
                posts_json = JSONEncoder(indent=4).encode(posts)
                # close the cursor first to clear buffer
                cursor.close()
                return posts_json

            else:
                # otherwise just return the dict
                # close the cursor first to clear buffer
                cursor.close()
                return posts

        # if no result found, return None
        else:
            # close the cursor first to clear buffer
            cursor.close()
            return None

    
    """
    method GetAuthorById

    Find author name according to the ID provided
    id = the Author ID
    friendly = if it is true, the friendly version of the author name will be returned,
                otherwise their username is returned

    """
    def GetAuthorNameById(self, id, friendly=False):
        cursor = self.mysql_conn.cursor(buffered=True)
        if bool(friendly):
            cursor.execute("SELECT author FROM authors WHERE id={}".format(str(id)))

            username = cursor.fetchone()

            # if result found, author's friendly name is returned
            if bool(username):
                # close the cursor first to clear buffer
                cursor.close()
                return username[0]
            # if result not found, None is returned
            else:
                # close the cursor first to clear buffer
                cursor.close()
                return None
        else:
            cursor.execute("SELECT username FROM authors WHERE id={}".format(str(id)))
            
            author = cursor.fetchone()

            # return username if found
            if bool(author):
                # close the cursor first to clear buffer
                cursor.close()
                return author[0]
            else:
                # as usual, return None if data not found
                # close the cursor first to clear buffer
                cursor.close()
                return None

    """
    Object Constructor, will be called when object is being built

    Before PostManager can be used, MySQL Server Host's Info must be provided via

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
        # vulnerable, see #6
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