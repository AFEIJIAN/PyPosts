# import required libraries
# PostManager from PyPosts
from pyposts import PostManager

# exit function
from sys import exit

# getpass utility, let user type password
# without input being echoed
from getpass import getpass

# function to perform delays
# we don't let output return faster
# without let user see it, rapid text output
# even can causes users dizzy!
from time import sleep


"""
function rmPost

Remove Added Post via the API inside the
PostManager object, pm provided

pm = PostManager object
pid = Post ID, if posts is remove using RemoveBulkPostById,
		set array to True in order to pass a list to this function

array = Set True if pid is a list(array), otherwise set False

str_id = Set True if pid is Post String IDs, otherwise set False

This function return result received from PostManager API
"""
def rmPost(pm, pid, array=False, str_id=False):
	# check if function receive an array/list

	# if yes, we are testing RemoveBulkPostById
	if array:
		print("Testing RemoveBulkPostById...\n")
	
	# otherwise, we are testing RemovePostById
	else:
		print("Testing RemovePostById...\n")
	
	sleep(2)

	# check if pid contains String ID and is an array
	if str_id and array:
		# if yes, then we are testing RemoveBulkPostById with
		# String ID as reference
		print("Using Post String ID as reference...\n")
		result = pm.RemoveBulkPostById(pid, use_str=True)
	
	# what if str_id is not True? We use Post IDs as reference
	elif array:
		print("Using Post ID as reference...\n")
		result = pm.RemoveBulkPostById(pid, use_str=False)
	
	# if array is not set to True but only str_id do?
	# we will test RemovePostById with Post ID as reference
	elif str_id:
		print("Using Post String ID as reference...\n")
		result = pm.RemovePostById(pid, use_str=True)
	
	# what if array and str_id is not True? we will test
	# RemovePostById and use Post ID as reference
	else:
		print("Using Post ID as reference...\n")
		result = pm.RemovePostById(pid, use_str=False)
	
	# check if result is received
	if bool(result):
		# check if result is an integer
		if isinstance(result, int):
			# if yes, return it
			return result
		
		# otherwise, exit
		else:
			print("Invalid result received! Exiting...")
			exit()

"""
function RunTest

Prepare posts used for testing and
run test by calling and passing
arguments to rmPost (above)
and verify its result

pm = PostManager object

Before this function ends, it will call
exit() itself to quit gracefully
"""
def RunTest(pm):
	# single post used for
	# RemovePostById
	post = """
	{
		"str_id":"demo_post",
		"title":"A Demo Post",
		"content":"Welcome to my demo post!",
		"author":1
	}
	"""

	# start testing RemovePostById
	# using Post ID as reference
	# add single demo post and receive it's post ID
	pid = pm.AddPostByJSON(post)
	# check if pid is received
	if bool(pid):
		# if yes, call rmPost to test
		result = rmPost(pm, pid, array=False, use_str=False)
		# check if result is not 1
		if result != 1:
			# if result is not 1, means there's an error,
			# exit it
			print("Invalid result received! Exiting...\n")
			exit()
	
	sleep(2)
		
	# ReAdd the single demo post
	# still testing RemovePostById but
	# with Post String ID as reference
	pid = pm.AddPostByJSON(post)
	# check if pid is received
	if bool(pid):
		# if yes, call rmPost to test
		result = rmPost(pm, "demo_post", array=False, use_str=True)
		# check if result is not 1
		if result != 1:
			# if result is not 1, means there's an error
			# exit it
			print("Invalid result received! Exiting...\n")
			exit()
	
	sleep(2)
	
	# start testing RemoveBulkPostById

	# list of demo posts with different String IDs
	posts = [
		"""
	{
		"str_id":"demo_post_1",
		"title":"A Demo Post",
		"content":"Welcome to my demo post!",
		"author":1
	}
	""",
	"""
	{
		"str_id":"demo_post_2",
		"title":"A Demo Post (2)",
		"content":"Welcome to my demo post!",
		"author":1
	}
	""",
	"""
	{
		"str_id":"demo_post_3",
		"title":"A Demo Post (3)",
		"content":"Welcome to my demo post!",
		"author":1
	}
	""",
	"""
	{
		"str_id":"demo_post_4",
		"title":"A Demo Post (4)",
		"content":"Welcome to my demo post!",
		"author":1
	}
	"""
	]

	# create an empty list to store Post IDs
	pids = list()
	# add them one by one using loop
	for loop in range(len(posts)):
		pid = pm.AddPostByJSON(posts[loop])
		# check if each pid is available
		if not bool(pid):
			# if not, exit
			print("Error occured while adding demo post {}! Exiting...\n".format(loop))
			exit()
		
		# append pid to the list
		pids.append(pid)
	
	# call rmPost to test
	# using Post IDs as reference
	result = rmPost(pm, pids, array=True, use_str=False)
	# check if result is not 1
	if result != 1:
		# if not 1, means there's an error, exit
		print("Invalid value received! Exiting...\n")
		exit()
	
	sleep(2)

	# ReAdd posts via loop
	for loop in range(len(posts)):
		pid = pm.AddPostByJSON(posts[loop])
		# we don't use Post IDs this time, just leave it
		if not bool(pid):
			# if bool() return False, means there's an error
			print("Error occured while adding demo post {}! Exiting...\n".format(loop))
			exit()

	# list of a demo post String IDs
	pids = ["demo_post_1", "demo_post_2", "demo_post_3", "demo_post_4"]
	
	# call rmPost again to test
	# using String IDs as reference this time
	result = rmPost(pm, pids, array=True, use_str=True)
	# check if result is not 1
	if result != 1:
		# if not 1, means there's an error, exit
		print("Invalid value received! Exiting...\n")
		exit()
	
	# if execution reach here, means all test runs well
	# inform user about it
	print("Luckily! There's no problems on Post Deletion!")
	# close PostManager
	pm.close()
	# inform user we are exiting...
	print("Exiting... GoodBye!")
	exit()


"""
function prompt

Ask user for MySQL Server and Database info,
then create a PostManager object and run the test

This also acts as the main function of script
"""
def prompt():
	# inform user about prerequiresites
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
	input("Press Enter if you are ready, press CTRL+C or CTRL+Z to exit")
	print("We will ask for MySQL Information right now.\n")
	print("We had default MySQL Server Host to 127.0.0.1 because remote server is not supported.\n")
	# ask for Server Port number
	port = input("MySQL Server Port: ")
	# check if user provided port number
	if not bool(port):
		# if not, default to 3306
		port = 3306
	
	# ask for Database username
	user = input("MySQL Database Username: ")
	# check if user provided username
	if not bool(user):
		# if not, inform user and exit this script
		print("You must provide a Database Username! Exiting...\n")
		exit()
	
	# ask for (Database) user password
	print("MySQL Database User Password,")
	passwd = getpass(prompt="Input is hidden so just type it and press Enter: ")
	# we don't check if password is empty, in case they don't set password

	# ask for database name
	db = input("Database name: ")
	# check if user provided database name
	if not bool(db):
		# if not, inform user and exit
		print("You must provide a Database Name, Exiting...\n")
		exit()
	
	# now everything collected, create a PostManager object
	print("Creating a PostManager object...\n")
	pm = PostManager(
		mysql_host="127.0.0.1",
		mysql_port=port,
		mysql_user=user,
		mysql_passwd=passwd,
		mysql_db=db
	)
	# inform user that object has created
	# and proceeding to test
	print("Object created, proceeding to testing...\n")
	sleep(2)
	# call testing function
	RunTest(pm)


# call the main function
prompt()