from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_key_pair(public_key_file="public_key.pem", private_key_file="private_key.pem"):
    """Generates and stores a public and private key pair 
    in the files `public_key_file` and `private_key_file`.
    """

    # generate keys
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, # reccomended default settings
        backend=default_backend())
    public_key = private_key.public_key()

    # store private key
    private_key_serialized = private_key.private_bytes(encoding=serialization.Encoding.PEM, 
        format=serialization.PrivateFormat.PKCS8, 
        encryption_algorithm=serialization.NoEncryption())
    with open(private_key_file, "wb") as key_file:
        key_file.write(private_key_serialized)

    # store public key
    public_key_serialized = public_key.public_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(public_key_file, "wb") as key_file:
        key_file.write(public_key_serialized)

def read_key_pair(public_key_file="public_key.pem", private_key_file="private_key.pem"):
    """Reads a pair of public and private keys from the files 
    `public_key_file` and `private_key_file` and returns the 
    `rsa` objects for those keys, `(public_key, private_key)`.
    """
    
    # read private key
    with open(private_key_file, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    # read public key
    with open(public_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    return (public_key, private_key)

def encrypt(key, message: str) -> bytes:
    """Returns an encrypted value of the given `message`."""
    cipher_text = key.encrypt(message.encode("utf-8"), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))
    return cipher_text

def decrypt(key, cipher_text: bytes):
    """Returns the decrypted value of the `cipher_text`."""
    message = key.decrypt(cipher_text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
        algorithm=hashes.SHA256(), label=None))
    return message.decode("utf-8")