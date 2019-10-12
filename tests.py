import mysql.connector as sql
from getpass import getpass
from sys import exc_info, exit

def menu():
    print("""
    PyPosts Tests Menu

    1. GetPostInfoByID
    2. GetPostByID
    3. GetAuthorByID
    
    Type 'exit' to exit program
    """)
    if bool()
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


while True:
    exit_code = menu()
    if exit_code == 1:
        break
        exit(1)