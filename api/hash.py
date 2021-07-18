from cryptography.fernet import Fernet 

#key = Fernet.generate_key()
fernet = Fernet(b'YmLTwla0Ie4UMHDCDHhtPPdrIad9RPe5OS_GjJi3KGc=')

def encode(word):
    word = str(word)
    a = fernet.encrypt(word.encode())
    return a.decode()

def decode(hashed):
    hashed = hashed.encode()
    return fernet.decrypt(hashed).decode()
    


    
