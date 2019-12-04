# write post including update post
# also test GetPostByModifiedDate

# required libraries
# PostManager from PyPosts
from pyposts import PostManager
# delay function
from time import sleep
# exit function
from sys import exit
# getpass utility, hide input echoing when
# user typing passwords
from getpass import getpass



"""
function update_post

Update the demo post by changing str_id from "demo_post" into "modified_post"
on the defined database in the PostManager

pm = PostManager Object
post = The JSON string containing post's information

This function MUST wait for function "write_post" called before itself
being called
"""
def update_post(pm, post):
	# a list of testing method, used for looping
	test_list = ['UpdatePost','UpdatePostByJSON','UpdatePostInfo']
	print("Post Update will be tested by add a demo post, update it and remove it again, \
	and this will be repeated until all update methods are called.\n")
	# relax first before test
	sleep(2)
	print("Using Post ID for reference...\n")
	# use loops for easier development
	for loop in test_list:
		# add post first
		pid = pm.AddPostByJSON(post)
		# check if post added successfully
		if not pid:
			# if result not 1, means error occured, exit
			print("Cannot add post! Exiting...")
			exit()

		print("Testing {}...\n".format(loop))
		# relax
		sleep(2)

		if loop == "UpdatePost":
			# update the post
			result = pm.UpdatePost(
				id=pid,
				author_id=1,
				title="A Modified Post",
				str_id="modified_post",
				content="This is a modified post!",
				use_str=False
				)
		
		elif loop == "UpdatePostByJSON":
			# update the post using provided JSON string
			# declared a JSON string
			post = """
			{{
			"id":{},
			"str_id":"modified_post",
			"author_id":1,
			"title":"A modified post!",
			"content":"Welcome to my demo post! :D"
			}}
			""".format(pid)
			# change post content into "A Modified Post"
			result = pm.UpdatePostByJSON(post, use_str=False)
		
		elif loop == "UpdatePostInfo":
			print("This will only update Post String ID.\n")
			result = pm.UpdatePostInfo(id=pid, Type="str_id", value="modified_post", use_str=False)
		
		# check if result is available
		if bool(result):
			# check if result is 1
			if result == 1:
				# if yes, means post updated
				print("Post Updated!")
			
			# otherwise, it must not 1
			else:
				print("Can't update post! Exiting...")
				exit()
		
		# delete all post by using RemovePostById
		result = pm.RemovePostById(id="modified_post", use_str=True)
		# check if result is available
		# if bool() return True means value is available
		if bool(result):
			# check if result contains 1
			# if yes, means removal success
			if result != 1:
				print("Error occured during post removal! Exiting...")
				exit()

	sleep(2)
	print("Using Post String ID as reference...\n")
	# loop over for easier development
	for loop in test_list:
		# add post first
		result = pm.AddPostByJSON(post)
		# check if post added successfully
		if not result:
			# if result not 1, means error occured, exit
			print("Cannot add post! Exiting...")
			exit()

		print("Testing {}...\n".format(loop))
		# relax
		sleep(2)

		if loop == "UpdatePost":
			# update the post
			result = pm.UpdatePost(
				id="demo_post",
				author_id=1,
				title="A Modified Post",
				str_id="modified_post",
				use_str=True
				)
		
		elif loop == "UpdatePostByJSON":
			# update the post using provided JSON string
			# declared a JSON string
			post = """
			{
			"id":"demo_post",
			"str_id":"modified_post",
			"author_id":1,
			"titl":"A modified post!",
			"content":"Welcome to my demo post! :D"
			}
			"""
			# change post content into "A Modified Post"
			result = pm.UpdatePostByJSON(post, use_str=True)
		
		elif loop == "UpdatePostInfo":
			print("This will only update Post String ID.\n")
			result = pm.UpdatePostInfo(id="demo_post", Type="str_id", value="modified_post", use_str=True)
		
		# check if result is available
		if bool(result):
			# check if result is 1
			if result == 1:
				# if yes, means post updated
				print("Post Updated!")
			
			# otherwise, it must not 1
			else:
				print("Can't update post! Exiting...")
				exit()

		# delete all post by using RemovePostById
		result = pm.RemovePostById(id="modified_post", use_str=True)
		# check if result is available
		# if bool() return True means value is available
		if bool(result):
			# check if result contains 1
			# if yes, means removal success
			if result != 1:
				print("Error occured during post removal! Exiting...")
				exit()

	
	# inform testers that no problem at writing and updating
	print("Luckily! There's no problems at Post Writing and Updating!\n")
	sleep(1)
	# close PostManager object
	pm.close()
	# say goodbye!
	print("Exiting... Goodbye!")
	exit()



"""
function write_post

Write a demo post into defined MySQL Database in PostManager

pm = PostManager Object
"""
def write_post(pm):
	# testing method AddPost
	print("Testing method AddPost... if we receive a post ID from API, it means adding complete!\n")
	# add the demo post and get the Post ID from API
	# we always use the same str_id value so that all demo post can removed in once
	pid = pm.AddPost(
		str_id="demo_post",
		author=1,
		title="A demo post!",
		content="Welcome to my demo post! :D"
	)
	# if bool() return True, means value is available
	if bool(pid):
		# check if pid is an integer
		# if isinstance() return true means pid contains integer
		if isinstance(pid, int):
			print("Post Added! The Post ID is: {}\n".format(pid))
		
		# otherwise, it must be an invalid value
		else:
			print("Oh no! We received an non-int value, exiting...")
			exit()
	
	# otherwise, it means either invalid or no value is returned
	else:
		print("Oh no! We can't add post, exiting...")
		exit()

	# relax for 2 seconds...
	sleep(2)

	# testing method AddPostByJSON
	print("Testing method AddPostByJSON... hope we will receive post ID from API again!\n")
	post = """
	{"str_id":"demo_post",
	"author":1,
	"title":"A demo post!",
	"content":"Welcome to my demo post! :D"}
	"""
	pid = pm.AddPostByJSON(post)

	# if bool() return True, which means value is available
	if bool(pid):
		# check if pid is an integer
		# if isinstance() return True, pid contains an integer
		if isinstance(pid, int):
			print("Post Added! The Post ID is {}\n".format(pid))
		
		# otherwise, it must be an invalid value
		else:
			print("Oh no! We received an non-int value, exiting...")
			exit()
	
	# if not True, means either invalid or no value returned
	else:
		print("Oh no! We can't add post, exiting...")
		exit()
	

	# relax again, oh no this API developer must be very lazy! :D
	sleep(2)

	# if code reach here, means test success

	# delete all post by using RemovePostById
	result = pm.RemovePostById(id="modified_post", use_str=True)
	# check if result is available
	# if bool() return True means value is available
	if bool(result):
		# check if result contain 1
		# if yes, means removal success
		if result == 1:
			print("Post Removed!\n")

	# otherwise, there must be an error...
	else:
		print("Error occured during post removal! Exiting...")
		exit()
		
	
	print("All Post write testing completed! Proceeding to Post Update Test...\n")
	update_post(pm, post)

"""
function prompt

Ask tester for MySQL Server and Database information
and create a PostManager object with it, after creation
it will call the first test function, write_post

It also act as main function for script
"""
def prompt():
	# inform user about prerequisites
	print("""
	Please make sure you have these information from MySQL Server:

	1. MySQL Hostname
	2. MySQL Port Number
	3. MySQL Database Username
	4. MySQL Database User Password
	5. MySQL Database Name (Where the Database is configured)

	The provided MySQL Database User must able to:
	
	1. Read all tables
	2. Write all tables
	3. Update all tables
	4. Remove all tables
	5. Modify all tables

	MySQL Server Stats
	1. Running

	Please run 'create_tables.py' to configure the Database if you haven't yet.
	""")
	input("Press Enter if you are ready, press ctrl+c or ctrl+z to exit")
	print("We will asking for MySQL Server Details right now.\n")
	sleep(1)
	print("MySQL Server Host has been default to 127.0.0.1, we don't support remote server right now.\n")
	# ask for server port number
	port = input("MySQL Server Port: ")
	# check if user provided port number
	if bool(port) != True:
		# if not, use the default, 3306
		port = 3306

	# ask for database username
	user = input("Database username:")
	# check if user provided database username
	if bool(user) != True:
		# if not, raise error
		raise ValueError("MySQL Database Username must not empty!")
	
	# ask for database user password
	print("Password for database user,")
	passwd = getpass(prompt="Input is hidden so just type it and press Enter: ")
	# we don't check for empty password, because they may not setup passwords

	# ask for database name
	db = input("Database name: ")
	# check if user provided database name
	if bool(db) != True:
		# if not, raise error
		raise ValueError("Database name must not empty!")


	print("Creating PostManager object...")
	sleep(1)
	# create a PostManager object
	pm = PostManager(
		mysql_host="127.0.0.1",
		mysql_port=port,
		mysql_user=user,
		mysql_passwd=passwd,
		mysql_db=db
		)

	# inform tester that object has been created
	print("Object created, proceeding to first test, the write test.")
	# call writing test
	write_post(pm)

# call the main function
prompt()