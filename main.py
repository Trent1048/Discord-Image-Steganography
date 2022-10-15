import encryption
import steganography
import cv2

# 190 character message maximum for rsa 2048 with sha-256

encryption.generate_key_pair()
public_key, private_key = encryption.read_key_pair()
message = "Hello, here is my super secret message!"
cv2.imwrite("./testOutput.png", steganography.encode_to_image(cv2.imread("./test.png"), message, public_key))
print(steganography.decode_from_image(cv2.imread("./testOutput.png"), private_key))