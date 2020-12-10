#!/usr/bin/python3

cipheredFlag = [0x9, 0x7, 0x11, 0x48, 0x20, 0x73, 0x2, 0x68, 0x2C, 0x67, 0x62, 0x2, 0x3E, 0x36, 0x7D, 0x1A, 0x1E, 0x35, 0x1F, 0x7, 0x2A, 0x1D, 0x3C, 0x0B, 0x71, 0x25, 0x62, 0x57, 0x7E, 0x30, 0x13, 0x3B, 0x71, 0x7, 0x2E]

def decryptPassword(password):
	res = ""
	for c in password:
		x = ord(c)
		if x >= ord('A') and x <= ord('Z'):
			x -= 17
			if x < ord('A'):
				x += ord('Z')
				x -= ord('@')
		res += chr(x)
	return res

def decryptFlag(ciphered, password):
	res = ""
	l = len(password)
	for i in range(len(ciphered)):
		res += chr( ord(password[i % l]) ^ ciphered[i] )

	return res

password = decryptPassword("RJJ3DSCP")
print("[*] Decrypted password: {}".format(password))
print("[*] Flag: {}".format(decryptFlag(cipheredFlag, password)))