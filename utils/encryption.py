from cryptography.fernet import Fernet

def load_key():
    with open('utils/encryptionKey.key', 'r') as f:
        key = f.read().encode()
    return key

fernet = Fernet(load_key())

def encrypt(text):
    encrypted = fernet.encrypt(text.encode())
    return encrypted.decode('utf-8')

def decrypt(encrypted_text):
    print(type(encrypted_text))
    decrypted = fernet.decrypt(encrypted_text.encode())
    return decrypted.decode('utf-8')

