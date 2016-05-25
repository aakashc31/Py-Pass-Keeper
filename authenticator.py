# bcrypt is used to check if the password matches

import bcrypt

# Takes a string pwd and returns the bcrypt hash
def computeHash(pwd):
	pwd = bytes(pwd, 'utf-8')
	return bcrypt.hashpw(pwd, bcrypt.gensalt());

# takes string pwd and a hashed byte like form, and tells whether they match
def checkAuth(pwd, hashed):
	pwd = bytes(pwd, 'utf-8')
	if bcrypt.hashpw(pwd, hashed) == hashed:
		return True
	return False

