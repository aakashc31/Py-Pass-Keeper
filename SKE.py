# Symmetric Key Encryption - AES 

import base64
from Crypto.Cipher import AES
from Crypto import Random

# takes string text and password to encrypt in base64 format
def encrypt(key, text):
	text = bytes(text, 'utf-8')
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CFB, iv)
	msg = iv + cipher.encrypt(text)
	return base64.b64encode(msg)

# takes a string key and base64 format msg to decrypt
def decrypt(key, msg):
	msg = base64.b64decode(msg)
	iv = msg[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CFB, iv)
	dec = cipher.decrypt(msg[AES.block_size:])
	return dec

