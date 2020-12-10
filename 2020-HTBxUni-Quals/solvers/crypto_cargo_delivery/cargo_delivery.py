
import pwn

conn=pwn.remote("docker.hackthebox.eu",30353)
conn.recvuntil(b'your encrypted message.\n')
conn.send("1\n")
line = conn.recvline()
print(line)
iv = bytes.fromhex(line[:32].decode('utf-8'))
ct = line[32:]
ct = ct[:-1]
ct = bytes.fromhex(ct.decode('utf-8'))
print(conn.recvuntil(b'your encrypted message.\n'))



def sendtext(text):
	conn.send("2\n")
	conn.recvline()
	conn.send(text.hex()+"\n")
	line = conn.recvline()
	conn.recvuntil('your encrypted message.\n')
	if(b'This is a valid ciphertext' in line):
		return True
	return False

from Crypto.Util.number import *

INTER = [bytes([0x00])]*16
L = [bytes([0x00])]*16

for i in range(1,17):
	print("i: "+str(i))
	found = 0
	for j in range(1,i):
		L[16-j] = bytes([bytes_to_long(INTER[16-j]) ^ i])
	for j in range(256):
		L[16-i] = bytes([j])
		if sendtext(b''.join(L)+ct):
			found = 1
			print(j)
			break
	if found == 0:
		print("ERROR")
	INTER[16-i] = bytes([bytes_to_long(L[16-i]) ^ i])

print(iv.hex())
print(b''.join(INTER).hex())

print(bytes.fromhex(hex(bytes_to_long(iv) ^ bytes_to_long(b''.join(INTER)))[2:]))


