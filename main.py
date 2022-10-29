import encryption
import steganography
import cv2

encryption.generate_key_pair()
public_key, private_key = encryption.read_key_pair()
message = ("According to all known laws of aviation, there is no way a bee should " +
    "be able to fly. Its wings are too small to get its fat little body off the " +
    "ground. The bee, of course, flies anyway because bees don't care what humans " +
    "think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, " +
    "black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready!")
cv2.imwrite("./testOutput.png", steganography.encode_to_image(
    cv2.imread("./test.png"), message, public_key))
print(steganography.decode_from_image(cv2.imread("./testOutput.png"), private_key))