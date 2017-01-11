from simplecrypt import encrypt
import sys

text = "CE mai faci domnule, Cristian? "
password ="eu"

cipher = encrypt(password, text)

target = open('text.txt', 'wb')
target.write(cipher)
target.close()
