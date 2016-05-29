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

# checks if everything's ok with the data folder
def checkDataIntegrity():
	checkFolder() #this will ensure that data folder and dict file exist
	os.chdir(separator)

	# if any entry is invalid (file not exists, or checkSum does not match), remove it
	entries = []
	guidList = []
	with open(dictFilename) as data:
		for line in data:
			[desc, guid, checkSum] = line.strip().split('*#*')
			filename = foldername + separator + guid + ".dat"
			if not os.path.isfile(filename):
				continue
			content = ''
			with open(filename) as f:
				for l in f:
					content += l
			currCheckSum =  hashlib.sha224(bytes(content, 'utf-8')).hexdigest()  
			if checkSum == currCheckSum:
				entries.append([desc, guid, checkSum])
				guidList.append(guid)
			else:
				print('Deleting file: ' + filename)
				os.remove(filename)

	# now we have a list of entries which are valid
	allGuid = set(guidList)
	os.chdir(foldername)
	for file in os.listdir(foldername):
		if file == 'dictionary.dat':
			continue
		if not file.endswith(".dat"):
			print('Deleting file: ' + file)
			os.remove(file)
		guid = file.replace('.dat', '') #check if its a valid guid!!!
		if guid not in allGuid:
			#we have a guid which is not in our desc list
			# for now, by default, try to add it
			# print(guid + ' is not in dictionary!')
			content = ''
			with open(file) as f:
				for line in f:
					content += line
			l = content.split('\n')
			if len(l) == 3:
				[desc, bc, cipher] = l
				entries.append([desc, guid, hashlib.sha224(bytes(content, 'utf-8')).hexdigest()])

	#now we re-write the dictionary file
	f = open(dictFilename, "w")
	for l in entries:
		toWrite = l[0] + '*#*' + l[1] + '*#*' + l[2] + '\n'
		f.write(toWrite)
	f.close()


def deleteDescEntry(desc):
	entry = []
	allEntries = []
	with open(dictFilename) as data:
		for line in data:
			l = line.strip().split('*#*')
			if len(l) == 3 and l[0] == desc:
				entry = l
			else:
				allEntries.append(l)
	if len(entry) != 3:
		return False
	guid = entry[1]
	filename = foldername + separator + guid + '.dat'
	if not os.path.isfile(filename):
		return False

	f = open(dictFilename, 'w')
	for l in allEntries:
		f.write(l[0] + '*#*' + l[1] + '*#*' + l[2] + '\n')
	f.close()
	os.chmod(filename, 0o777)
	os.remove(filename) #delete the file if it exists
	return True
