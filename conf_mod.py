from sys import exit,exc_info
from os.path import abspath

# function to simplify file open operations
def open_file(dir,types,error_level=0):
	if types == 'server':
		try:
			server_conf_obj = open(dir,'r')
			return server_conf_obj

		except FileNotFoundError:
			if error_level == 0:
				return -1

			else:
				print("Exiting, cannot find the config file provided: {}".format(abspath('./'+dir)))
				exit()

		except PermissionError:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, access denied when trying to access provided config file: {}".format(abspath('./'+dir)))
					exit()

				except NameError:
					print('Exiting, access denied when trying to access provided server config file.')
					exit()

		except Exception:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, unknown errors occured when trying to read this config file: {}\nHere is the error:\n{}".format(abspath('./'+dir),exc_info()))
					exit()

				except NameError:
					print("Exiting, unknown errors occured when trying to read this server config file, Here is the error:\n{}".format(exc_info()))
					exit()

	elif types == 'mysql_admin':
		try:
			mysql_admin_obj = open(dir,'r')
			return mysql_admin_obj

		except FileNotFoundError:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, cannot find the config file provided: {}".format(abspath('./'+dir)))
					exit()

				except NameError:
					print('Exiting, cannot find MySQL admin config file specified.')
					exit()

		except PermissionError:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, access denied when trying to access provided config file: {}".format(abspath('./'+dir)))
					exit()

				except NameError:
					print("Exiting, access denied when trying to access provided MySQL admin config file.")
					exit()

		except Exception:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, unknown errors occured when trying to read this config file: {}\nHere is the error:\n{}".format(abspath('./'+dir),exc_info()))
					exit()

				except NameError:
					print("Exiting, unknown errors occured when trying to read this MySQL admin config file. Here is the error:\n{}".format(exc_info()))
					exit()

	elif types == 'log_file':
		try:
			log_file_obj = open(dir,'w')
			return log_file_obj

		except FileNotFoundError:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, cannot find the log file provided: {}".format(abspath('./'+dir)))
					exit()

				except NameError:
					print("Exiting, cannot find the log file provided.")
					exit()

		except PermissionError:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, access denied when trying to access provided log file: {}".format(abspath('./'+dir)))
					exit()

				except NameError:
					print("Exiting, access denied when trying to access provided log file.")
					exit()

		except Exception:
			if error_level == 0:
				return -1

			else:
				try:
					print("Exiting, unknown errors occured when trying to read this log file: {}\nHere is the error:\n{}".format(abspath('./'+dir),exc_info()))
					exit()

				except NameError:
					print("Exiting, unknown errors occured when trying to read this log file, Here is the error:\n{}".format(exc_info()))
					exit()
	else:
		# error_level = 1, important process is running so will not call exit()
		if error_level == 0:
			return -1

		else:
			exit()


# designed for process boot, quit automatically if errors found
class conf_processor:
	def __init__(self,
	single_file=False,
	file_type=None,
	server_conf_obj=None,
	mysql_admin_obj=None,
	log_file_obj=None):
		if single_file  == True:
			if file_type == 'server':
				self.mysql_admin = None
				self.log_file = None
				self.server_conf = server_conf_obj
			elif file_type == 'mysql_admin':
				self.server_conf = None
				self.log_file = None
				self.mysql_admin= mysql_admin_obj
			elif file_type == 'log_file':
				self.server_conf = None
				self.mysql_admin = None
				self.log_file = log_file_obj
		else:
			self.server_conf = server_conf_obj
			self.mysql_admin= mysql_admin_obj
			self.log_file = log_file_obj

	# parse each line of config file and add it to a list
	def parser(self,conf_file_obj):
		# append every line of config file to list 'out'
		# error for code below
		out = list(read.replace("\n","") for read in conf_file_obj)
		# check if 'out' is a list
		if out == list(out):
			# use seek(0) to go back to first line of file (so other function can read again)
			conf_file_obj.seek(0)
			return out
		else:
			out = "ERR"
			return out

	# check whether a directive is exist, and split with symbol '=' to acquire value
	# directive name must be same (Case-sensitive)
	# for example: 'SSL=ON' = ['SSL','ON']
	def check_directives(self,directive_name,parsed_conf_file_list):
		if parsed_conf_file_list == list(parsed_conf_file_list):
			new_parsed_file_list = list(x.split("=") for x in parsed_conf_file_list)
			for x in new_parsed_file_list:
				if directive_name in x[0]:
					result = x[1]
					return result
		else:
			result = "INVALID_VAL"
			return result

	# function to parse config files contents
	# config_files_memory = an object that stores required file objects
	def parse_server_conf(self,types,directive_name):
		# error: self.server_conf become log_file
		if types == "server":
			try:
				output_list = self.parser(self.server_conf)
				result = self.check_directives(directive_name,output_list)
				return result
			except FileNotFoundError:
				result = "ERR"
				return result
		elif types == "mysql_admin":
			try:
				output_list = self.parser(self.mysql_admin)
				result = self.check_directives(directive_name,output_list)
				return result
			except FileNotFoundError:
				result = "ERR"
				return result
		else:
			result = "ERR_INVALID_FILE_TYPE"
			return result