from Crypto.Cipher import AES
import sys
import hashlib

password = 'cristian'
key = hashlib.sha256(password.encode('utf-8')).digest()
target = open('text.txt', 'rb')
IV = 16 * '\x00' # Initialization vector:
mode = AES.MODE_CBC
messaje = target.read()

print(messaje)

decryptor =AES.new(key, mode, IV=IV)
plain = decryptor.decrypt(messaje)

print("\n\n\n\n", plain)
