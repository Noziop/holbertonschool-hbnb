# Script pour générer le hash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
password = 'admin1234'
hashed = bcrypt.generate_password_hash(password, rounds=12).decode('utf-8')
print(hashed)