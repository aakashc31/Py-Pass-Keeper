import os, sys, stat
import base64, uuid, hashlib

separator = "\\"
foldername = os.getcwd() + separator + "data"
dictFilename = foldername + separator + "dictionary.dat"	
	
def checkFolder():
	if not os.path.exists(foldername):
		os.makedirs(foldername)
	filename = dictFilename
	if(not os.path.isfile(filename)):
		fo = open(filename, "w")
		fo.close()
	return

# returns a list of all the password descriptions in the file
def getAllDesc():
	ret = []
	with open(dictFilename) as data:
		for line in data:
			l = line.strip().split('*#*')
			if len(l) == 3:
				ret.append(l[0])
			else:
				pass #should raise some exception, right?
	return ret;

# adds a new entry. Create a new file and add its entry to the dict file
def flushEntry(desc, bc, cipher):
	# write the content to file
	guid = str(uuid.uuid1())
	filename = foldername + separator + guid + '.dat'
	content = desc + '\n' + bc.decode('utf-8') + '\n' + cipher.decode('utf-8')
	f = open(filename, 'w')
	f.write(content)
	f.close(); 

	os.chmod(filename, stat.S_IRUSR);

	# add entry to the dict file
	checkSum =  hashlib.sha224(bytes(content, 'utf-8')).hexdigest()  
	toWrite = desc + '*#*' + guid + '*#*' + checkSum + '\n'
	f = open(dictFilename, 'a')
	f.write(toWrite)
	f.close()

# fetch the entry from the file corresponding to the given description 'desc'
# it is returned in string format so convert it to bytes later
# if not available then returns an empty list
def fetchDescEntry(desc):
	entry = []
	with open(dictFilename) as data:
		for line in data:
			l = line.strip().split('*#*')
			if len(l) == 3 and l[0] == desc:
				entry = l
				break
	if len(entry) != 3:
		return []
	guid = entry[1]
	filename = foldername + separator + guid + '.dat'
	if not os.path.isfile(filename):
		return []
	ret = []
	with open(filename) as data:
		for line in data:
			ret.append(line.strip())
	return ret[1:] if len(ret) == 3 else []

