import email, base64
from asn1crypto import cms
from Crypto.Util.number import *
from OpenSSL.crypto import load_certificate
from OpenSSL.crypto import FILETYPE_PEM
# Opening message
eml_file = 'challenge'
message = email.message_from_file(open(eml_file))

# Printing content types
for part in message.walk():
	print(part.get_content_type())
	content_info = cms.ContentInfo.load(part.get_payload(decode=True))
	ct = content_info['content']['encrypted_content_info']['encrypted_content'].native
	print("here we see the algorithm and the iv, since its cbc", content_info['content']['encrypted_content_info']['content_encryption_algorithm'].native)
	print("recipients infos (we can copy from here their encrypted keys (encrypted_key for each recipient), which are the same but each encrypted with their private key)", str(content_info['content']['recipient_infos'].native))
	#https://github.com/wbond/asn1crypto/blob/master/asn1crypto/algos.py
	#https://github.com/wbond/asn1crypto/blob/master/asn1crypto/cms.py
	#We discover how this protocol works by printing some information

print("ciphertext", ct)


def keyfrom(file):
	with open(file, 'rb') as fp:
		cert = load_certificate(FILETYPE_PEM, fp.read())

	# This gives you the modulus in integer form
	modn = cert.get_pubkey().to_cryptography_key().public_numbers().n
	e = cert.get_pubkey().to_cryptography_key().public_numbers().e

	return modn, e

N = []


n,e = keyfrom("mechi.crt")
N.append(n)
n,e = keyfrom("corius.crt")
N.append(n)
n,e = keyfrom("andromeda.crt")
N.append(n)

print("RSA modules, in the same order as the recipients above", N)
print("e, it's three for all the recipients", e)
print("i copied this info to sage (i like it better than a script, although many people will disagree)")
# e is 3 for the 3 of them

#https://www.johndcook.com/blog/2019/03/06/rsa-exponent-3/

from sage.all import *

