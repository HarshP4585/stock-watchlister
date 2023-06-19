from passlib.context import CryptContext
context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(data):
    return context.hash(data)

def verify(plain_password, hashed_password):
    # fixed pattern verify(plain, hashed)
    return context.verify(plain_password, hashed_password)
