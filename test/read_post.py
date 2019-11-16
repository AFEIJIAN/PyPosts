# automated test script for pyposts framework

# import required library
import pyposts as py
# import getpass for hidden password input
from getpass import getpass
# for delaying
from time import sleep
# used for decode post into dict for verification
from json import JSONDecoder
# datetime object to create datetime object
from datetime import datetime as dt
# wonderful exit upon completion
from sys import exit

"""
function verify_single

Verify if src post info,
is same with exp post info

src = The source post info
exp = Expected post info

designed to reduce lines of code on other function

return 1 if same, return -1 if not
"""
def verify_single(src, exp):
	if src == exp:
		return 1
	else:
		return -1

"""
function verify

Verify if post src is same as exp

src = The source used to verification, must be a dict
exp = Expected result, must be a dict

if same, 1 will be return
otherwise, -1 will be return
"""
def verify(src, exp):
	# dict key names used for verifications
	types = ['str_id','author','title','content']
	for x in types:
		if src[x] != exp[x]:
			break
			return -1
	# if everything same, it will reach here
	return 1

"""
function read

Use all Post Reading API from PyPosts to read (acquire) post

pm = The PostManager object created from function insert()
pid = The Post ID
"""
def read(pm, pid):
	# post used for verification
	postv = dict(
		str_id="demo_post",
		author=1,
		title="A demo post!",
		content="Hooray! A demo post!"
	)
	print("There are 4 API for Post Reading, we only test 3 of it, we will test one by one.\n")
	print("Another API will be tested in write_post.py\n")
	sleep(1)
	print("Testing 1 of 3: GetPostById\n")
	sleep(2)
	print("Using Post ID for reference...\n")
	# use Post ID for reference
	post = pm.GetPostById(id=pid, use_str=False, json=False)
	# verify result
	result = verify(post, postv)
	# if no error found, it will bypass statements
	if result == -1:
		print("Something error in here, exiting...\n")
		exit()
	
	# test using String ID
	print("Using Post String ID for reference...\n")
	sleep(1)
	post = pm.GetPostById(id="demo_post", use_str=True, json=False)
	# verify
	result = verify(post, postv)
	if result == -1:
		print("Something error in here, exiting...")
		exit()
	
	# use Post ID for reference but request for JSON string as result
	print("Using Post ID for reference but acquiring JSON string this time...\n")
	post = pm.GetPostById(id=pid, use_str=False, json=True)
	# verify, decode post from JSON into dict first
	result = verify(
		JSONDecoder().decode(post),
		postv
	)
	if result == -1:
		print("Something error in here, exiting...")
		exit()
	
	# use Post String ID for reference but request for JSON string as result
	print("Using Post String ID for reference but acquiring JSON string this time...\n")
	post = pm.GetPostById(id="demo_post", use_str=True, json=True)
	# verify, decode post first
	result = verify(
		JSONDecoder().decode(post),
		postv
	)
	if result == -1:
		print("Something error in here, exiting...")
		exit()
	
	# proceeding to second test
	# types of post information to be acquired
	test_types = ['title', 'author', 'posted_date', 'content', 'str_id', 'id']
	print("Testing 2 of 3: GetPostInfoById")
	sleep(2)
	for types in test_types:
		if types == "posted_date":
			print("posted_date doesn't have value for verification, since it use the datetime when you insert the post.")
			print("As long as result appear, it's considered as successful.\n")
			sleep(2)
		print("Acquiring {} from database...".format(types))
		sleep(1)
		print("Using Post ID as reference\n")
		post = pm.GetPostInfoById(pid, types, use_str=False)
		# check if current testing types is posted_date or Post ID
		if types != "posted_date" or types != "id":
			result = verify_single(post, postv[types])
			if result == -1:
				print("Something error in here, exiting...")
				exit()
		
		if types == "id":
			if result != pid:
				print("Something error in here, exiting...")
				exit()
		
		# store posted_date for post reading
		if types == "posted_date":
			posted_date = result
		

	print("Using Post String ID for reference...\n")
	sleep(2)
	for types in test_types:
		print("Acquiring {} from database...\n".format(types))
		sleep(1)
		post = pm.GetPostInfoById("demo_post", types, use_str=True)
		if types != "posted_date" or types != "id":
			result = verify_single(post, postv[types])
			if result == -1:
				print("Something error in here, exiting...")
				exit()
	
	print("Testing 3 of 3: GetPostByPostedDate")
	# convert datetime into string first
	posted_date = dt.strptime(posted_date, "%Y-%m-%d %H:%M:%S")
	# acquire post, since we only used 1 demo post for testing
	# therefore amount of post is limited to 1
	print("Using posted_date acquired before\n")
	# testing without json
	post = pm.GetPostByPostedDate(posted_date, 1, json=False)
	# verify result
	result = verify(post, postv)
	if result == -1:
		print("Something error in here, exiting...")
		exit()
	sleep(2)
	print("Using same posted_date but request JSON String as output this time...\n")
	post = pm.GetPostByPostedDate(posted_date, 1, json=True)
	# verify result, but decode JSON string first
	result = verify(
		JSONDecoder().decode(post),
		postv
	)
	if result == -1:
		print("Something error in here, exiting...")
		exit()
	
	print("Testing performed successful! No errors were found! Proceeding to demo post removal...")

	# remove demo post from database
	result = pm.RemovePostById(pid)

	if result == 1:
		print("Post removed successfully! Closing the PostManager object...")

	# close the PostManager
	pm.close()

	print("Everything is OK! Bye!")
	exit()
	


"""
function insert

Use API AddPost from PyPosts.PostManager to insert post
and call read() after this

mysql_info = The dict containing the MySQL server and database info
"""
def insert(mysql_info):
	print("We are going to insert a post into the database you provided us.")
	sleep(1)
	print("Creating a PostManager object...")
	# create a PostManager object
	pm = py.PostManager(
		mysql_info['host'],
		mysql_info['port'],
		mysql_info['user'],
		mysql_info['passwd'],
		mysql_info['db']
	)
	print("Inserting...")
	result = pm.AddPost(
		str_id="demo_post",
		author=1,
		title="A demo post!",
		content="Hooray! A demo post!"
		)
	if isinstance(result, int):
		print("Inserting completed! Proceeding to reading test!")
	
	read(pm, result)


"""
function prompt_mysql

Prompt user for MySQL server and database information
and call insert() after this

"""
def prompt_mysql():
	print("Regarding server host, we default to localhost (127.0.0.1), because remote server isn't supported.")
	host = '127.0.0.1'
	# ask user for mysql server port number
	port = input("MySQL Server Port, default is 3306: ")
	if bool(port):
		# if user provided port, we will convert to int
		port = int(port)
	else:
		# otherwise, we will provide them
		port = 3306
	# ask for database username
	user = input("Your database username: ")
	# raise error if user leave empty
	if bool(user) != True:
		raise ValueError("You must provide MySQL database username!")
	# ask for database user password
	print("Password of the database user")
	passwd = getpass(prompt="Input is hidden so just type and press Enter: ")
	# do not raise ValueError in case the user doesn't have password
	db = input("The database name: ")
	# raise ValueError if user doesn't provide
	if bool(db) != True:
		raise ValueError("You must provide Database name!")
	
	# assign values into a mysql dict
	mysql_info = dict(
		host=host,
		port=port,
		user=user,
		passwd=passwd,
		db=db
	)
	insert(mysql_info)
	

"""
function start

Show the required information about the test
and call prompt_mysql() after user pressed Enter
"""
def start():
	print("Before we starting this test, we information about your MySQL Server and the database information.")
	print("We will write a post first, and read it, then delete finally")
	input("Press Enter if you are ready, otherwise press CTRL+C to exit.")
	prompt_mysql()


# run the startup function
start()