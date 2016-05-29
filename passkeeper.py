import SKE
import time
import authenticator
from filehandler import *
import getpass

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(65 + BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

# This function is supposed to some prechecks
# For now only checks if the data file exists or not. If not, then creates one. 
# Later, may be consistency/integrity of the file will be checked.
def preCheck():
	checkDataIntegrity()
	return

# To view the description of all the passwords that have been saved
def viewAllDesc():
	r = getAllDesc()
	r.sort()
	for i in r:
		print(i)
	return

# To save a new password
def addNewEntry():
	desc = input("Enter description: "); 
	
	r = fetchDescEntry(desc);
	if len(r) != 0:
		print("A password with same description already exists!")
		return

	text = input("Enter password to be saved: ");
	pwd = getpass.getpass("Enter password for current entry: "); #Will need this to be invisible, also ask to re-enter
	if(len(pwd) < 8 or len(pwd) > 16):
		print('Password must be 8 - 16 characters long!')
		return
	pwd2 = getpass.getpass('Re-enter password: ');
	if(pwd != pwd2):
		print("Passwords don't match!\nEntry adding failed!");
		return

	bc = authenticator.computeHash(pwd); #To be used as authentication 
	pwd = pad(pwd)
	cipher = SKE.encrypt(pwd, text); #Encrypt 
	flushEntry(desc, bc, cipher);
	print('Entry added successfully!');

# To view a password you have saved earlier
def viewSavedEntry():
	desc = input('Enter description: ');
	
	r = fetchDescEntry(desc);
	if len(r) == 0:
		print(desc + ' does not exist');
		return

	bc = bytes(r[0], 'utf-8')
	cipher = bytes(r[1], 'utf-8')
	
	key = getpass.getpass('Enter password: ');
	if authenticator.checkAuth(key, bc):
		print('Authentication Successfull!');
		input('Press enter to view the saved password')
		key = pad(key)
		ret = SKE.decrypt(key, cipher);
		print(ret.decode('utf-8'))
	else:
		time.sleep(2)
		print('Authentication Unsuccessful!')
	return

# To delete a saved entry
def deleteSavedEntry():
	desc = input('Enter description: ');
	
	r = fetchDescEntry(desc);
	if len(r) == 0:
		print(desc + ' does not exist');
		return

	bc = bytes(r[0], 'utf-8')
	cipher = bytes(r[1], 'utf-8')
	
	key = getpass.getpass('Enter password: ');
	if authenticator.checkAuth(key, bc):
		print('Authentication Successfull!');
		ch = input('Are you sure you want to delete this entry? (y/n)')
		if ch == 'y' or ch == 'Y':
			if deleteDescEntry(desc):
				print('Delete Successful!')
			else:
				print('Delete Unsuccessful!')
		else:
			print('Delete unsuccessful')
			pass
	else:
		time.sleep(2)
		print('Authentication Unsuccessful!')
	return

def menu():
	print('\n*****************')
	print('1: View description of all saved passwords')
	print('2: Add a new entry')
	print('3: View a saved entry')
	print('4: Delete a saved entry')
	print('5: Exit')
	print('*****************\n')

def main():
	preCheck();
	menu()
	while 1:
		ch = input('\nEnter your choice: ')
		ch = ch.strip();
		if ch == '1':
			viewAllDesc()
		elif ch == '2':
			addNewEntry()
		elif ch == '3':
			viewSavedEntry()
		elif ch == '4':
			deleteSavedEntry()
		elif ch == '5':
			print('Exiting...')
			return
		else:
			print('Enter choice number from 1 to 5')
		# input('Press enter to continue...')

main()
