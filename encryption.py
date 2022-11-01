from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

MAX_MESSAGE_LENGTH = 190

def generate_key_pair(public_key_file="public_key.pem", private_key_file="private_key.pem"):
    """Generates and stores a public and private key pair 
    in the files `public_key_file` and `private_key_file`.
    """
    
    # use default key name for empty string as well as None values
    if public_key_file == "":
        public_key_file = "public_key.pem"
    if private_key_file == "":
        private_key_file = "private_key.pem"

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

def encrypt_blocks(key, message: str) -> bytes:
    """Returns an encrypted value of the given `message`, which can be of any length."""
    encrypted_sections = []
    message_section_start_index = 0
    # go through sections of a size equal to the max message length
    while True:
        # stop looping when the message has no more sections
        if message_section_start_index >= len(message):
            break
        # encrypt each section
        encrypted_sections.append(encrypt(key, message[
            message_section_start_index:message_section_start_index + MAX_MESSAGE_LENGTH]))
        # update the index of the section
        message_section_start_index += MAX_MESSAGE_LENGTH
    return b"".join(encrypted_sections)

def encrypt(key, message: str) -> bytes:
    """Returns an encrypted value of the given `message`."""
    if len(message) > MAX_MESSAGE_LENGTH:
        raise Exception("Message too long")
    cipher_text = key.encrypt(message.encode("utf-8"), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))
    return cipher_text

def decrypt_blocks(key, cipher_text: bytes):
    """Returns the decrypted value of the `cipher_text`, which can be of any length."""
    block_size = (key.key_size + 7) // 8
    decrypted_sections = []
    cipher_text_section_start_index = 0
    # go through the sections of size equal to the block size
    while True:
        # stop looping when the message has no more sections
        if cipher_text_section_start_index >= len(cipher_text):
            break
        # decrypt each section
        decrypted_sections.append(decrypt(key, cipher_text[
            cipher_text_section_start_index:cipher_text_section_start_index + block_size]))
        # update the index of the section
        cipher_text_section_start_index += block_size
    return "".join(decrypted_sections)

def decrypt(key, cipher_text: bytes):
    """Returns the decrypted value of the `cipher_text`."""
    message = key.decrypt(cipher_text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
        algorithm=hashes.SHA256(), label=None))
    return message.decode("utf-8")