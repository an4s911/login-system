import mysql.connector as mc
import hashlib, binascii, getpass
import re, datetime

databaseName = 'login_system'
tableName = 'user_details'

db = mc.connect(host='localhost', user='root', passwd='anas') # connecting to the mysql server [, database='login_system']
dbCursor = db.cursor() # cursor for database
dbExec = dbCursor.execute # just a smaller execute statement so its not too long because 'dbCursor.execute' is soo boring to type over and over
dbFetchall = dbCursor.fetchall
dbFetchone = dbCursor.fetchone

dbExec(f'create database if not exists {databaseName}')
dbExec(f'use {databaseName}')
dbExec(f'create table if not exists {tableName}(id int not null auto_increment primary key, fname char(30), lname char(30), username varchar(50) not null unique, email_id varchar(50) not null unique, password varchar(128) not null)')

userDetails = {'loggedIn':False}

try:
	f = open('log.txt', 'r')
except FileNotFoundError:
	f = open('log.txt', 'a')
	f.write("------- Logs every SignUp and Login -------")

def checkQ(inputValue): # when the user enters the letter 'q' anywhere the user is asked to input, the programs exits(or breaks, quits). inputValue is whatever the user inputs or enters
	if inputValue.lower() == 'q':
		print("Do you really want to quit?")
		choice = input("If you want to start over type 's' else press Enter\n:")
		main() if choice.lower() in ['s'] else quit()

def insertIntoUd(fname, lname, username, email_id, password): 
	# This function is to insert fname, lname, username, email_id and password to the table user_details in the database login_system. Ud stands for User Details
	dbExec(f"insert into {tableName} (fname, lname, username, email_id, password) values('{fname}', '{lname}', '{username}', '{email_id}', '{password}')")
	db.commit()

def update(item, itemType): 
	# read the comment for the function checkItemInTable(item, itemType)
	pass

def hashIt(password):
	password = password.encode('utf-8')
	dk = hashlib.pbkdf2_hmac('sha256', password, b'anas', 100000)
	return binascii.hexlify(dk).decode('utf-8')

def checkEmailId(email_id): # checks if the email id is there in the table user_details in the database and returns a boolean
	return checkItemInTable(email_id, 'email_id')

def checkUsername(username): # same as checkEmailId but this checks for the username
	return checkItemInTable(username, 'username')

def checkPassword(password):
	pass

def checkItemInTable(item, itemType): # checks for item in the table user_details in the database. item is the data for the itemType for eg; if itemType is email_id then item will be the email id like this item=='example@example.com' and itemType=='email_id'
	dbExec(f'select {itemType} from {tableName}')
	items = [i[0] for i in dbCursor.fetchall()]
	if item in items:
		return True
	else:
		return False

def checkUser(username, email_id, password): # checks if the password for the username and email_id is correct and returns boolean
	dbExec(f"select password from {tableName} where username='{username}' and email_id='{email_id}'")

	try:
		fetchedPassword = dbCursor.fetchone()[0]
	except TypeError:
		print("Username and Email ID does not match!")
		login()
	else:
		if fetchedPassword == password:
			return True
		else: 
			return False

def getUsername(task): # takes user input for username
	return getItem('Username', checkUsername, task)

def getEmailId(task): # takes user input for email id
	return getItem('Email ID', checkEmailId, task)

def getPassword(): # takes user input for password
	password = getpass.getpass()
	checkQ(password)
	return hashIt(password)

def getItem(itemName, checkItemFunc, task): # mainly for username and email_id, itemName refers to what item we are getting for eg; username or email_id. checkItemFunc refers to the function used to check whether the particular item value is already used. task is either login task or signup task, this is to make different functions for both seperately.
	if task.lower() == 'signup':
		while True:
			item = input(f"{itemName}: ")
			checkQ(item)
			if not checkItemFunc(item):
				return item
				break
			else:
				print(f"{itemName} already exists!")
				if ifYes('Login'):
					login()
					break
				else:
					continue

	elif task.lower() == 'login':
		while True:
			item = input(f"{itemName}: ")
			checkQ(item)
			if checkItemFunc(item):
				return item
				break
			else:
				print(f"{itemName} not found!")
				if ifYes('SignUp'):
					signup()
					break
				else:
					continue

def ifYes(task): # here also mostly the task if either login or signup but can be used for other things too. This function is to ask the user if the user would like to change their task to something recommended
	choice = input(f"Would you like to {task}?\n(y/n):")
	checkQ(choice)
	if choice in ['y']:
		return True
	else:
		return False

def log(action, username, email_id):
	with open('log.txt', 'a') as logFile:
		logFile.write(f"\n{datetime.datetime.today().strftime('%d %b %Y %I:%M %p GMT+3')} | action:{action} | user:{username} | email_id:{email_id}")

def login(usernameEmailId, password): # The login function  returns
	if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", usernameEmailId):
		if checkEmailId(usernameEmailId):
			dbExec(f"select username from {tableName} where email_id='{usernameEmailId}'")
			username = dbFetchone()[0]
			if checkUser(username, usernameEmailId, password):
				log('login', username, usernameEmailId)
				return (username, True)
			else:
				return (username, False)
		else:
			return (usernameEmailId, False)
	else:
		if checkUsername(usernameEmailId):
			dbExec(f"select email_id from {tableName} where username='{usernameEmailId}'")
			email_id = dbFetchone()[0]
			if checkUser(usernameEmailId, email_id, password):
				log('login', usernameEmailId, email_id)
				return (usernameEmailId, True)
			else:
				return (usernameEmailId, False)
		else:
			return (usernameEmailId, False)


def signup(fname, lname, username, email_id, password): # The signup function. returns True after signing up and recording all user data
	if checkUsername(username):
		return ("Username", False)
	elif checkEmailId(email_id):
		return ("Email ID", False)
	else:
		insertIntoUd(fname, lname, username, email_id, password)
		log('signup', username, email_id)
		with open('log.txt', 'a') as logFile:
			logFile.write(f" | name:{fname} {lname}")
		return (None, True)

def main(): # The Main function. This is the function that is executed first when running this program.
	if userDetails['loggedIn'] == True:
		dbExec(f"select fname, lname, username, email_id from {tableName} where username='{userDetails['username']}'")
		fname, lname, username, email_id = dbFetchone()
		name = fname + '' + lname
		print("Name\tUsername\tEmail ID")
		print(f"{name}\t{username}\t{email_id}")

	else:
		print("Choose from the following by entering the character in the corresponding brackets. Type 'q' anywhere in the program to exit.")
		choice = input("Login(l)\nSignUp(s)\n:") 
		checkQ(choice)
		if choice.lower() in ['l']:
			login()
		
		elif choice.lower() in ['s']:
			signup()		
				
		else:
			print("Please Input valid option!")
			main()

def returnUserDetails(username):
	dbExec(f"select fname, lname, username, email_id from user_details where username='{username}'")
	return dbFetchone()



if __name__=='__main__':
	usernameEmailId = input("username/email: ")
	password = input("Password: ")
	print(login(usernameEmailId, hashIt(password)))
# 	main()

# ~sr