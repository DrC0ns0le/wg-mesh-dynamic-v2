import os
import base64
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization

# generate private key

def generate():
    private_key = X25519PrivateKey.generate()

    privkey = private_key.private_bytes(  
        encoding=serialization.Encoding.Raw,  
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    priv64=base64.b64encode(privkey).decode('utf8').strip()

    # public key
    pubkey = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, 
        format=serialization.PublicFormat.Raw)

    pub64=base64.b64encode(pubkey).decode('utf8').strip()
    
    return {"private_key": priv64, "public_key": pub64}

def preshared():
    
    # Generate a 32-byte random key
    psk_bytes = os.urandom(32)

    # Encode the key in base64
    psk_base64 = base64.b64encode(psk_bytes).decode('utf-8')

    return psk_base64
    
