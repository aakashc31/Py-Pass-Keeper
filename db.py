import sqlite3

import os, sys, stat
import base64, uuid, hashlib

dbname = 'data.db'

def checkFolder():
	conn = sqlite3.connect(dbname)
	x = conn.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='auth_data';''')
	if x.fetchone():
		return
	conn.execute('''CREATE TABLE auth_data
		(NAME 	TEXT PRIMARY KEY NOT NULL,
		HASH 	TEXT NOT NULL,
		CONTENT TEXT NOT NULL)''');
	#check if the table exists

# returns a list of all the password descriptions in the file
def getAllDesc():
	conn = sqlite3.connect(dbname)
	cursor = conn.execute("SELECT NAME from auth_data")
	ret = []
	for row in cursor:
		ret.append(row[0])
	conn.close()
	return ret;

# adds a new entry. Create a new file and add its entry to the dict file
def flushEntry(desc, bc, cipher):
	bc = bc.decode('utf-8')
	cipher = cipher.decode('utf-8')
	conn = sqlite3.connect(dbname)
	cursor = conn.execute("INSERT INTO auth_data VALUES(?,?,?)", (desc, bc, cipher))
	conn.commit();
	conn.close()

# fetch the entry from the file corresponding to the given description 'desc'
# it is returned in string format so convert it to bytes later
# if not available then returns an empty list
def fetchDescEntry(desc):
	conn = sqlite3.connect(dbname)
	cursor = conn.execute("SELECT * from auth_data where NAME=:name", {"name":desc})
	ret = []
	for row in cursor:
		ret.append(row[1])
		ret.append(row[2])
	return ret

def deleteDescEntry(desc):
	conn = sqlite3.connect(dbname)
	cursor = conn.execute("DELETE from auth_data where NAME=:name", {"name":desc})
	conn.commit()
	conn.close()
	return True
