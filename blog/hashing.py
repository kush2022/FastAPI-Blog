from passlib.context import CryptContext



pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)
    
    def verify(plain_txt, hashed_password):
        return pwd_context.verify(plain_txt, hashed_password)