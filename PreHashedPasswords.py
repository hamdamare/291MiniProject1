from hashlib import pbkdf2_hmac

def hashpass():
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000
	entered_pwd = raw_input('Enter a password: ')
	dk = pbkdf2_hmac(hash_name, bytearray(entered_pwd, 'ascii'), bytearray(salt, 'ascii'), iterations)
	print(dk)
hashpass()
