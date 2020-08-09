import mysql.connector as mc
import hashlib, binascii, getpass

db = mc.connect(host='localhost', user='root', passwd='anas', database='login_system')
dbCursor = db.cursor()
dbExec = dbCursor.execute

def insertIntoUd(fname, lname, username, email_id, password): 
	# This function is to insert fname, lname, username, email_id and password to the table user_details in the database login_system. Ud stands for User Details
	dbExec(f"insert into user_details (fname, lname, username, email_id, password) values('{fname}', '{lname}', '{username}', '{email_id}', '{password}')")
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
	pass

def checkItemInTable(item, itemType): 
	# item is the data for the itemType for eg; if itemType is email_id then item will be the email_id like this item=='example@example.com' and itemType=='email_id'
	dbExec(f'select {itemType} from user_details')
	items = [i[0] for i in dbCursor.fetchall()]
	if item in items:
		return True
	else:
		return False

def checkUser(username, email_id, password):
	dbExec(f"select password from user_details where username='{username}' and email_id='{email_id}'")

	fetchedPassword = dbCursor.fetchone()[0]
	if fetchedPassword == password:
		return True
	else: 
		return False

def getUsername(task):
	return getItem('Username', checkUsername, task)

def getEmailId(task):
	return getItem('Email ID', checkEmailId, task)

def getPassword():
	password = getpass.getpass()
	return hashIt(password)

def getItem(itemName, checkItemFunc, task): 
	# mainly for username and email_id, itemName refers to what item we are getting for eg; username or email_id. checkItemFunc refers to the function used to check whether the particular item value is already used
	if task.lower() == 'signup':
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

	elif task.lower() == 'login':
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
	while True:
		password = getPassword()
		if checkUser(username, email_id, password):
			return True
			break
		else:
			print("Incorrect Password! Try again:-")
			continue

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
		if login():
			print("Logged In!")
			main()
	elif choice.lower() in ['s']:
		if signup():
			print("Account created!")
			main()
	else:
		print("Please Input valid option!")
		main()

main()
