import os
import base64

filename = "allData.dat";


def createFileIfNotExists():
	if(not os.path.isfile(filename)):
		fo = open(filename, "w")
		fo.close()

# returns a list of all the password descriptions in the file
def getAllDesc():
	lno = 0
	ret = []
	with open(filename, "r") as data:
		for line in data:
			if lno % 3 == 0:
				ret.append(line.strip())
			else:
				pass
			lno += 1
	return ret

# appends the given entry to the file.
def flushEntry(desc, bc, cipher):
	mode = "a"
	fo = open(filename, mode)
	fo.write(desc+'\n')
	fo.write(bc.decode('utf-8') + '\n')
	fo.write(cipher.decode('utf-8') + '\n')
	fo.close()

# fetch the entry from the file corresponding to the given description 'desc'
# if not available then returns an empty list
def fetchDescEntry(desc):
	ret = []
	lno = 0
	loc = -1
	curr = []
	with open(filename, "r") as data:
		for line in data:
			x = line.strip()
			curr.append(x)
			if x == desc:
				loc = lno//3
			lno += 1
			if(lno % 3 == 0):
				ret.append(curr)
				curr = []
	ret.append(curr)
	ans = []
	if loc == -1:
		return ans
	ans.append(ret[loc][1])
	ans.append(ret[loc][2])
	return ans


