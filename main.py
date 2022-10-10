import encryption

encryption.generate_key_pair()
public_key, private_key = encryption.read_key_pair()
message = "This is my message, can you read it?"
encrypted_message = encryption.encrypt(public_key, message)
print("\n" + str(encrypted_message))
decrypted_message = encryption.decrypt(private_key, encrypted_message)
print("\n" + decrypted_message)