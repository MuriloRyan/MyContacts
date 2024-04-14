import bcrypt

class HashUtils:
    def __init__(self):
        pass

    def encrypt(self,password,salt):

        return bcrypt.hashpw(str(password).encode('utf-8'),salt)

    def generate_n_hash(self,password):
        password = str(password)
        salt = bcrypt.gensalt(rounds=8)

        return {
            "password": bcrypt.hashpw(password.encode('utf-8'), salt),
            "salt":salt
        }

if __name__=='__main__':
    h = HashUtils()