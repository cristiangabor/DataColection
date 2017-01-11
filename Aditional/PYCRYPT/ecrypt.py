import sys
import hashlib
from Crypto.Cipher import AES

password = 'cristian'
my_key= hashlib.sha256(password.encode('utf-8')).digest()
key=my_key
IV = 16 * '\x00' # Initialization vector:
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)

text ="Ce faci"
ciphertext =encryptor.encrypt(text)

target = open("text.txt", 'wb')

target.write(ciphertext)
target.close()
print(ciphertext)
