import mysql.connector as mc
import hashlib, binascii, getpass

db = mc.connect(host='localhost', user='root', passwd='anas', database='login_system')
dbCursor = db.cursor()


def insertIntoUd(fname, lname, username, email_id, password): 
	# This function is to insert fname, lname, username, email_id and password to the table user_details in the database login_system. Ud stands for User Details
	dbCursor.execute(f"insert into user_details (fname, lname, username, email_id, password) values('{fname}', '{lname}', '{username}', '{email_id}', '{password}')")
	db.commit()

def update(item, itemType): 
	# read the comment for the function checkItemInTable(item, itemType)
	pass

def hashIt(password):
	password = password.encode('utf-8')
	dk = hashlib.pbkdf2_hmac('sha256', password, b's', 100000)
	return binascii.hexlify(dk).decode('utf-8')

def checkEmailId(email_id):
	return checkItemInTable(email_id, 'email_id')

def checkUsername(username):
	return checkItemInTable(username, 'username')

def checkPassword(password):
	return checkItemInTable(password, 'password')

def checkItemInTable(item, itemType): 
	# item is the data for the itemType for eg; if itemType is email_id then item will be the email_id like this item=='example@example.com' and itemType=='email_id'
	dbCursor.execute(f'select {itemType} from user_details')
	items = [i[0] for i in dbCursor.fetchall()]
	if item in items:
		return True
	else:
		return False

def checkUser(username, email_id, password):
	pass

def getUsername(task):
	return getItem('Username', checkUsername, task)

def getEmailId(task):
	return getItem('Email ID', checkEmailId, task)

def getPassword():
	password = getpass.getpass()
	return hashIt(password)

def getItem(itemName, checkItemFunc, task): 
	# mainly for username and email_id, itemName refers to what item we are getting for eg; username or email_id. checkItemFunc refers to the function used to check whether the particular item value is already used
	if task.lower() == 'login':
		while True:
			item = input(f"{itemName}: ")
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

	elif task.lower() == 'signup':
		while True:
			item = input(f"{itemName}: ")
			if checkItemFunc(item):
				return item
				break
			else:
				if ifYes('SignUp'):
					signup()
					break
				else:
					continue

def ifYes(task):
	choice = input(f"Would you like to {task}?\n(y/n):")
	if choice in ['y']:
		return True
	else:
		return False

def login():
	username = getUsername('login')
	email_id = getEmailId('login')
	password = getPassword()

def signup():
	fname = input("First Name: ")
	lname = input("Last Name: ")

	username = getUsername('signup')
	email_id = getEmailId('signup')

	password = getPassword()

	insertIntoUd(fname, lname, username, email_id, password)

def main():
	choice = input("Login(l)\nSignUp(s)\n:") 
	if choice.lower() in ['l']:
		login()
	elif choice.lower() in ['s']:
		signup()
	else:
		print("Please Input valid option!")
		main()

main()
