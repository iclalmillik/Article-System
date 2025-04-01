import base64
import os
from Crypto.Cipher import AES

def generate_aes_key():  #256 bit AES anahtarı

    return os.urandom(32)

def encrypt_data_aes(plain_text, key):
  
    if isinstance(plain_text, str):
        plain_text = plain_text.encode('utf-8')
    
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plain_text)
    
    encrypted = cipher.nonce + tag + ciphertext
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data_aes(encoded_data, key):

    encrypted = base64.b64decode(encoded_data)
    nonce = encrypted[:16]
    tag = encrypted[16:32]
    ciphertext = encrypted[32:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
