from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash():
    def hash_password(password: str):
        return context.hash(password)
    
    def verify_password(plain_text: str, hash: str):
        return context.verify(plain_text, hash)