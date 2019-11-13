# pyramid web framework, not using right now
#from pyramid.config import Configurator
#from wsgiref.simple_server import make_server

# mysql connector to interact with MySQL Server
import mysql.connector as sql
# Encoder and Decoder from JSON to process post content
from json import JSONEncoder,JSONDecoder
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


"""
PostManager does what it said,
it help you get the post content according to id and type

form of date and time:
in digit only and date separated by dashes while time separated by colons,
which is same as MySQL "DATETIME" data type, please refer to MySQL Documentation
YYYY-MM-DD HH:MM:SS
example: "2019-06-09 03:05:06" if the date is 9 June 2019 and time is 03:05:06 AM
"""
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
		cursor.execute("SELECT id,str_id,title,content,posted_date,last_modified,author,modified FROM posts WHERE posted_date <= '{}'".format(date))
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
	method AddPost

	Add post into defined MySQL database by passing arguments
	to function

	str_id = post's string id
	author = id of the post's author
	title = post's title
	content = post's content

	Please note that some values will assign by default
	when store into database:

	post_id = Defined by framework itself
	posted_date = use the datetime when this function being called
	last_modified = None
	modified = 0 (represent False in MySQL)

	when post is saved successfully, a post id will be returned
	"""
	def AddPost(self, str_id, author, title, content):
		# data type checks for arguments
		# isinstance(arguments, required_datatype)
		# raise TypeError if invalid
		if isinstance(str_id, str) == False:
			raise TypeError("str_id must be a string.")

		if isinstance(author, int) == False:
			raise TypeError("Author must be their id in integer.")

		if isinstance(title, str) == False:
			raise TypeError("Post's title must be a string.")

		if isinstance(content, str) == False:
			raise TypeError("Post's content must be a string.")
		
		# create buffered cursor
		cursor = self.mysql_conn.cursor(buffered=True)


		# How post id is calculated:
		# 1. Get all the post ids and add it to a list
		# 2. Sort it to arrange ascendingly
		# 3. Add 1 to last (which is largest number) and it will be the new post id

		# start with finding post's ID
		# get all post id
		cursor.execute("SELECT id FROM posts")
		result = cursor.fetchall()

		# accquire all ids and add it to a list
		ids = list()
		for x in result:
			ids.append(x[0])
		
		# sort the list so the numbers become ascendingly arranged
		ids.sort()

		# calculate and assign post id
		post_id = ids[-1]+1

		# execute query
		cursor.execute("INSERT INTO posts (id, str_id, author, title, posted_date, last_modified, modified, content) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
			post_id,
			str_id,
			author,
			title,
			# posted_date will use current date and time
			# with microsecond changed into 0
			str(dt.now().replace(microsecond=0)),
			"NULL",
			0,
			content
		))
		# commit result
		self.mysql_conn.commit()

		# close the cursor to clear it's buffer
		cursor.close()

		# return post's id
		return post_id
	

	"""
	method AddPostByJSON

	Add post into defined MySQL Database from JSON string

	json = the JSON string, which is the object in JavaScript

	json string only requires 4 object attributes (case sensitive), which are:
	1. title - Post's title, must be string
	2. str_id - Post's String ID, must be string
	3. content - Post's content, must be string
	4. author - Post's author ID, must be integer

	example of JSON string acquired by calling GetPostById(json=True),
	(with auto assigned values removed):

	{
		"title": "My First Posts!",
		"str_id": null,
		"content": "My New Post stored in PyPosts framework!",
		"author": 1
	}

	If post saved successfully, a post id will be returned
	* Post ID calculate method will same as method above, 'AddPost()'
	"""
	def AddPostByJSON(self, json):
		# data type check for argument
		# raise error if invalid and inform what type data
		# they are providing
		if isinstance(json, str) == False:
			raise TypeError("JSON string must be a string.")
		
		# create buffered cursor
		cursor = self.mysql_conn.cursor(buffered=True)

		# decode json string into python dict
		post = JSONDecoder().decode(json)

		# start with finding post's ID first
		# acquire all post's IDs
		cursor.execute("SELECT id FROM posts")

		# fetch all result
		result = cursor.fetchall()

		# create a list to store all ids
		ids = list()

		# add all ids into the list
		for x in result:
			ids.append(x)

		# sort all the list so that the ids arranged ascendingly
		ids.sort()

		# calculate and assign post id
		post_id = ids[-1]+1

		# now insert post into defined MySQL database
		cursor.execute("INSERT INTO posts (id, str_id, author, title, posted_date, last_modified, modified, content) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
			post_id,
			post['str_id'],
			post['author'],
			post['title'],
			# use current date and time with microsecond changed to 0
			str(dt.now().replace(microsecond=0)),
			"NULL",
			0,
			post['content']
		))

		# commit query
		self.mysql_conn.commit()

		# close the cursor to clear the buffer
		cursor.close()

		# return the post id
		return post_id
	

	"""
	method UpdatePostInfo

	Update the referred post's info specified using the value provided

	id = post's id, to use string id, set use_str to True

	use_str = If set to True, id can filled with a string id and will be used
				for post lookup, default is False

	Type = type of post's information wanted to update, acceptable values are
	1. title - the post's title
	2. content - the post's content
	3. author - the post's author ID
	4. str_id - the post's string ID

	value = The value used to update the post's info

	*except value types mentioned above, other values can't be updated manually,
	which might lead to posts lookup error in the future

	This function only update each post's info on each call, to update multiple,
	use UpdatePost() or UpdatePostByJSON() (See below)

	If no error occurs, this function will return 1 upon completion
	"""
	def UpdatePostInfo(self, id, Type, value, use_str=False):
		# list of valid values type can be updated, used for verification
		valid_type = ['title','content','author','str_id']

		# data type checks and value verification
		# raise error if invalid
		if isinstance(Type, str) == False:
			raise TypeError("Value type specified must be a string.")
			# if it is string, then check if value is valid
		else:
			if Type not in valid_type:
				# if type is not in valid_type, then they might try to update something
				# can't be updated, give them an error
				raise ValueError("Invalid value type, acceptable are {}".format(str(valid_type)))

		if isinstance(value, str) == False:
			raise TypeError("Value must be a string.")
		
		# check if string ID will be used
		if use_str:
			# if used, check if post string ID is a string
			if isinstance(id, str) == False:
				raise TypeError("Post string ID must be a string.")
		
		else:
			# if not, check if post ID is an integer
			if isinstance(id, int) == False:
				raise TypeError("Post ID must be an integer.")
		
		# execute query to update post info
		# if using string ID as reference
		if use_str:
			cursor.execute("UPDATE posts SET '{}'='{}' WHERE str_id='{}'".format(
				Type,
				value,
				id
			))
		
		# if using post ID as reference
		else:
			cursor.execute("UPDATE posts SET '{}'='{}' WHERE id='{}'".format(
				Type,
				value,
				id
			))

		# commit current update first
		self.mysql_conn.commit()

		# after value updated, mark the post is modified and set last_modified date
		# with current datetime with microsecond changed to 0

		# when str_id is updated, we will use 'value' instead of 'id',
		# this is because 'id' is the old value used for reference just now
		if Type == "str_id":
			cursor.execute("UPDATE posts SET modified=1 AND last_modified='{}' WHERE str_id='{}'".format(
				str(dt.now().replace(microsecond=0)),
				value
			))
		
		else:
			# otherwise, still using the post's id for reference
			cursor.execute("UPDATE posts SET modified=1 AND last_modified='{}' WHERE id={}".format(
				str(dt.now().replace(microsecond=0)),
				id
			))
		
		# commit final MySQL query
		self.mysql_conn.commit()

		# close the cursor to clear it's buffer
		cursor.close()

		# return 1 as successful
		return 1

	
	"""
	method GetAuthorById

	Find author name according to the ID provided
	id = the Author ID
	friendly = if set to True, the friendly version of the author name will be returned,
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
	mysql_port = Port of MySQL Server, it should be int, we will convert it into int in case
					it is string
	mysql_user = User for the database of the MySQL Server
	mysql_passwd = Password of the MySQL User
	mysql_db = Name of the MySQL Database
	"""
	def __init__(self, mysql_host, mysql_port, mysql_user, mysql_passwd, mysql_db):
		# check if mysql server port is provided,
		# when mysql_port has value, bool() will return True
		# if yes we will convert it into int, in case developer provide string
		if bool(mysql_port):
			mysql_port = int(mysql_port)

		# if no we will use the default port, which is 3306
		else:
			mysql_port = 3306

		self.mysql_conn = sql.connect(host=mysql_host,
								 port=mysql_port,
								 user=mysql_user,
								 passwd=mysql_passwd,
								 database=mysql_db)
	
	"""
	method close, close the PostManager

	Actually this is just a method to tell that PostManager can be stopped
	what it does was just close the MySQL Server connection object
	This must called before closing your program
	"""
	def close(self):
		self.mysql_conn.close()