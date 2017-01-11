from simplecrypt import decrypt
import sys

password ="eu"

target = open("text.txt", 'rb')
plaintext= target.read()
mytext=decrypt(password, plaintext)

print(mytext)
