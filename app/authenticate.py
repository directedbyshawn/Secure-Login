'''

    Authentication methods for cs166 final project.

'''

import random, hashlib
from .db import retrieve_accounts

lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
special = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '?', '[', ']', '{', '}', ':', ';', '"', '/', '.', ',', '<', '>']

def authenticate(username, password):
    
    ''' Authenticates user upon login '''
    
    # retrieves users from database
    users = retrieve_accounts()

    stored_username = ''
    stored_password = ''

    # finds user in records
    for user in users:
        if user[0] == username:
            stored_username = user[0]
            stored_password = user[1]

    # if user is not found, false
    if (stored_username == '' or stored_password == ''):
        return False
    
    # retrieves salt and stored password from pw string
    salt_length = 40
    salt = stored_password[:salt_length]
    stored_hash = stored_password[salt_length:]

    # compares inputted password with hash and returns result
    hashable = salt + password
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()
    return this_hash == stored_hash

def verify_new_account(username, password):
    
    '''

        Method used to determine if new account credentials are valid

        Parameters:
            username (str) : username entered by user
            password (str) : password entered by user

        Returns:
            status (bool) : status of if the new credentials are good or not
    
    '''

    global lower_case, upper_case, nums, special

    # retrieves all users from db and makes a list of all usernames
    users = retrieve_accounts()
    taken_usernames = []
    for accounts in users:
        taken_usernames.append(accounts[0])

    # status of whether or not password contains the requirements
    requirement_one = len(password) >= 8
    requirement_two = len(password) <= 25
    requirement_three = username not in taken_usernames

    requirement_lower = False
    requierment_upper = False
    requirement_nums = False
    requirement_special = False

    for char in password:
        if char in lower_case:
            requirement_lower = True
        if char in upper_case:
            requierment_upper = True
        if char in nums:
            requirement_nums = True
        if char in special:
            requirement_special = True

    # SQL injection prevention
    for char in username:
        if char in special:
            return False


    status = False
    if (requirement_one and requirement_two and requirement_three and requirement_lower and requierment_upper and requirement_nums and requirement_special):
        status = True

    return status

def random_password():
    
    '''

        Function to return randomly generated password

        Returns:
            password (str) : randomly generated password
    
    '''

    global lower_case, upper_case, nums, special
    
    chars = [lower_case, upper_case, nums, special]

    password_length = random.randint(12, 16)

    password = ''
    for i in range(password_length):
        lib = chars[random.randint(0, 3)]
        char = lib[random.randint(0, len(lib) - 1)]
        password += char 

    return password