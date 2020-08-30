#!/usr/bin/python3
#-*- encoding=UTF8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes
from binascii import hexlify, unhexlify
import random

key = "very_awes0m3_k3y"
flag = "FwordCTF{W!Pr35gp_ZKrJt[NcV_Kd-/NmJ-8ep(*A48t9jBLNrdFDqSBGTAt}" # Cadena aleatoria de prueba
assert len(flag) == 62
assert len(key) == 16

def to_blocks(text):
	return [text[i*2:(i+1)*2].encode() for i in range(len(text)//2)]

def random_bytes(seed):
	random.seed(seed)
	return long_to_bytes(random.getrandbits(8*16))

def encrypt_block(block,key):
	cipher = AES.new(key.encode(), AES.MODE_ECB)
	plain_pad = pad(block, 16)
	return hexlify(cipher.encrypt(plain_pad)).decode()

def encrypt(txt, key):
	res = ""
	blocks = to_blocks(txt)
	for block in blocks:
		res += encrypt_block(block, key)
	return res

def translate(txt,l,r):
	return txt[:l]+txt[r:]+txt[l:r]

def shuffle(txt):
	seed=random.choice(txt)
	random.seed(seed)
	nums = []
	for _ in range(45):
		l = random.randint(0, 15)
		r = random.randint(l+1, 33)
		txt = translate(txt, l, r)
		nums = [[l,r]] + nums
	return txt, nums

def slice(txt, n):
	return [txt[index : index + n] for index in range(0, len(txt), n)]

def decrypt_block(block,key):
	cipher = AES.new(key.encode(), AES.MODE_ECB)
	return unpad(cipher.decrypt(unhexlify(block.encode())), 16).decode()

def shuffle2(txt, seed):
	random.seed(seed)
	nums = []
	for i in range(45):
		l = random.randint(0, 15)
		r = random.randint(l+1, 33)
		txt = translate(txt, l, r)
		nums = [[l,r]] + nums
	return txt, nums

def reverse_translate(txt, l, r):
	n = len(txt) - r + l
	res = txt[:l] + txt[n:] + txt[l:n]
	assert len(res) == len(txt)
	return res

def crack(encrypted):
	# Descifra los bloques
	blocks = slice(encrypted, 32)
	decrypted = "".join(decrypt_block(block, key) for block in blocks)
	print("[*] Descifrado: " + decrypted)
	# Ahora la flag está shuffleada, por lo que se obtienen los indices
	# de los caracteres unicos en la parte que se conoce de la flag
	known = "FwordCTF{}"
	uniqueKnown = ""
	for c in known:
		if decrypted.count(c) == 1:
			uniqueKnown += c
	print("[*] Caracteres únicos de la parte conocida de la flag: " + uniqueKnown)
	indexes = [decrypted.index(c) for c in uniqueKnown]
	print("[*] Indices aleatorizados de los caracteres: " + str(indexes))
	# Se itera el charset de la flag descifrada, ya que la semilla es un caracter de esta,
	# y se busca con cuales de ellas se obtienen los mismos indices
	charset = []
	for char in decrypted:
		if char not in charset:
			charset.append(char)
	dummy = "FwordCTF{BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB}"
	assert len(dummy) == 62

	seeds = []
	for char in charset:
		res, _ = shuffle2(dummy, char)
		i = [res.index(c) for c in uniqueKnown]
		if indexes == i:
			seeds.append(char)
	print("[*] Possible seeds: " + str(seeds))
	# Se obtiene la secuencia de numeros aleatorios generados en la funcion shuffle
	for seed in seeds:
		_, nums = shuffle2(dummy, seed)
		# Aplica las operaciones inversas
		solution = decrypted
		for lr in nums:
			solution = reverse_translate(solution, lr[0], lr[1])
		print("[*] Possible solution with seed {}: {}".format(seed, solution))


def shuffleEncrypt(txt, key):
	shuffled, nums = shuffle(txt)
	print("[*] Shuffled: " + shuffled)
	print("[*] Nums: " + str(nums))
	return encrypt(shuffled, key)


#encrypted = shuffleEncrypt(flag, key)
encrypted = "3ce29d5f8d646d853b5f6677a564aec6bd1c9f0cbfac0af73fb5cfb446e08cfec5a261ec050f6f30d9f1dfd85a9df875168851e1a111a9d9bfdbab238ce4a4eb3b4f8e0db42e0a5af305105834605f90621940e3f801e0e4e0ca401ff451f1983701831243df999cfaf40b4ac50599de5c87cd68857980a037682b4dbfa1d26c949e743f8d77549c5991c8e1f21d891a1ac87166d3074e4859a26954d725ed4f2332a8b326f4634810a24f1908945052bfd0181ff801b1d3a0bc535df622a299a9666de40dfba06a684a4db213f28f3471ba7059bcbdc042fd45c58ae4970f53fb808143eaa9ec6cf35339c58fa12efa18728eb426a2fcb0234d8539c0628c49b416c0963a33e6a0b91e7733b42f29900921626bba03e76b1911d20728254b84f38a2ce12ec5d98a2fa3201522aa17d6972fe7c04f1f64c9fd4623583cc5a91cc471a13d6ab9b0903704727d1eb987fd5d59b5757babb92758e06d2f12fd7e32d66fe9e3b9d11cd93b11beb70c66b57af71787457c78ff152ff4bd63a83ef894c1f01ae476253cbef154701f07cc7e0e16f7eede0c8fa2d5a5dd5624caa5408ca74b4b8c8f847ba570023b481c6ec642dac634c112ae9fec3cbd59e1d2f84f56282cb74a3ac6152c32c671190e2f4c14704ed9bbe74eaafc3ce27849533141e9642c91a7bf846848d7fbfcd839c2ca3b"
print("[*] Cifrado: " + encrypted)

crack(encrypted)