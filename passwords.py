
from hashlib import pbkdf2_hmac
import time
#Encrypts a user enterd password
def Encrypt():
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000

	entered_pwd = raw_input('Enter a password: ')
	while entered_pwd:
		if (len(entered_pwd)<4):
			print('Enter a longer password')
			time.sleep(0.5)
			entered_pwd = raw_input('Enter a password: ')
		
		else:
			password = entered_pwd
			dk = pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)
			dk2 = pbkdf2_hmac(hash_name, bytearray(entered_pwd, 'ascii'), bytearray(salt, 'ascii'), iterations)
			encrypted_pass = dk
			encrypted_pass2 = dk2
			break

	return encrypted_pass
print(Encrypt())
			

	


