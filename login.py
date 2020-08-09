import mysql.connector as mc
import hashlib, binascii

db = mc.connect(host='localhost', user='root', passwd='anas', database='login_system')
dbCursor = db.cursor()

def insertIntoUd(fname, lname, username, email_id, password): # This function is to insert fname, lname, username, email_id and password to the table user_details in the database login_system. Ud stands for User Details
	dbCursor.execute(f"insert into user_details (fname, lname, username, email_id, password) values('{fname}', '{lname}', '{username}', '{email_id}', '{password}')")
	db.commit()

def update():
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

def checkItemInTable(item, itemType): # item is the data for the itemType for eg; if itemType is email_id then item will be the email_id like this item=='example@example.com' and itemType=='email_id'
	dbCursor.execute(f'select {itemType} from user_details')
	items = [i[0] for i in curs.fetchall()]
	if item in items:
		return False
	else:
		return True

def checkUser(username, email_id, password):
	pass

def login():
	pass

def signup():
	fname = input("First Name: ")
	lname = input("Last Name: ")

	while True:
		username = input("Username: ")
		if checkUsername(username):
			break

	while True:
		email_id = input("Email ID: ")
		if checkEmailId(email_id):
			break

	password = input("Password: ")
	password = hashIt(password)

	if not checkUser(username, email_id, password):
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
