import hashlib
import random
import string
from datetime import datetime 
from time import sleep
SALT = 'Twmj7fEIyGS0o8MB'

hashed_pass = '4e1b7b60f66a918dd7190eb7e21e82f51fcc18c20060bd1bdd2e48007316e5a3'
def hash_password(password):
    return hashlib.sha256((SALT + password).encode()).hexdigest()
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    print("Random alphanumeric String is:", result_str)

#print(hash_password(input('Enter Pass: ')))

current_time = float(datetime.now().strftime("%H.%M"))
if current_time < 1.55 or current_time > 6.30:
    print(datetime.now().strftime("%B %d %Y %I:%M:%S %p"))
    sleep(300)
else:
    print('sleeping')
    sleep(60*60)

print(datetime.now().strftime("%B %d %Y %H.%M "))