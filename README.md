# Secure Login

<img alt="login screen" src="https://srodgers.w3.uvm.edu/cs166/login.png" style="width: 500px; margin: 30px;">

## Description
This is a secure login system I created for a class project. Users are able to create an account, login, and then access a few menu options based on their authentication level. 
- `Level 1` is the highest, and users with level 1
authentication can access any option from the directory.  
- `Level 2` users can access a few special options, but not all of them.  
- `Level 3` users can only access the most basic options.  

I have created three accounts and added them to the database, the logins can be found in test_credentials.txt. I created a level 1, 2, 
and 3 accounts so that you can see that the authentication level does affect user access. All users created from the create page are given level 3 accces which 
is the lowest. 

## Security
Users are permanentely locked out after three incorrect login attempts. If they try to access any page on the server, they are redirected to a page indicating that they are locked out. User account information is stored in an sqlite database, where the passwords are salted and encrypted using the sha1 hash function.

## Purpose
The purpose of this project is not to actually create a purposeful service, but to demonstrate an understanding of proper technique for creating secure web services. The class I created this for is a cybersecurity class, so the site is meant to be resistant to SQL injection attacks, as well as any sort of attack on the integrity of the database.

## Instructions
To test my work, install from `requirements.txt`. Only flask will be installed, every other module is included with python. You will need to run the setup.py script first to create the
database. After that, you can run the app using start.py. To login, check `app/test_credentials.csv` for some pre created credentials. I have not currently added a feature to log out as this project
was created solely for security demonstration purposes. If you would like to test the different pre created credentials, you must restart the dev server.
