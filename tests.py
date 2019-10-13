import mysql.connector as sql
from getpass import getpass
from sys import exc_info, exit
import pyposts as pyp

def menu():
    print("""
    PyPosts Tests Menu

    1. GetPostInfoByID
    2. GetPostByID
    3. GetAuthorByID
    
    Please select by entering number.

    Type 'exit' to exit program
    """)
    test = input("> ")
    if bool(test):
        if test == '1':
            test(1)
        elif test == '2':
        elif test == '3':
        elif test == '4':
        elif test == '5':
        elif test == '6':
        elif test == 'exit':
            return 1
    
    else:
        print("Invalid value! Only 1-6, Please try again!")
    # return 0 to ask for continue not exiting
    return 0

# perform actual test according to type of test required
# MySQL host's information and other required information
# will be prompt before starting test
def test(test_type):
    print("Before test, some MySQL host's info is required.")


while True:
    exit_code = menu()
    if exit_code == 1:
        break
        exit(1)