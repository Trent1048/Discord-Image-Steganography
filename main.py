import os
import cv2
import encryption
import steganography

public_key = private_key = None

# define functions for each menu option

def generate_key_pair():
    """Generates a pair of public and private keys."""
    # loop until valid key names are given
    while True:
        public_key_file = input("Public key file name: ")
        private_key_file = input("Private key file name: ")
        if public_key_file != private_key_file:
            break
    encryption.generate_key_pair(public_key_file, private_key_file)

def load_key_pair():
    """Sets the active key pair."""
    # loop until valid key names are acquired
    while True:
        # loop until a valid key name is given
        while True:
            public_key_file = input("Public key file name: ")
            if os.path.exists("./" + public_key_file):
                break
            print("Please enter a valid key file")
        # loop until a valid key name is given
        while True:
            private_key_file = input("Private key file name: ")
            if os.path.exists("./" + private_key_file):
                break
            print("Please enter a valid key file")
        # ensure the keys aren't the same
        if public_key_file != private_key_file:
            break
        else:
            print("Please ensure public and private key are different")
    # update the key values
    global public_key, private_key
    public_key, private_key = encryption.read_key_pair("public_key.pem", "private_key.pem")

def encrypt_message_to_image():
    """Encrypts a message and hides it into an image."""
    if public_key is None:
        print("Please load a key pair before encrypting a message")
        return
    message = input("Please input a message: ")
    # get the input image file
    while True:
        picture_file_name = input("Please enter a png file name for the image to encrypt into: ")
        if os.path.exists("./" + picture_file_name) and picture_file_name.endswith(".png"):
            break
        else:
            print("Please input a valid file name")
    # get the output image file name
    while True:
        picture_out_file_name = input("Please enter a png file name for the output image: ")
        if picture_out_file_name.strip() == "":
            print("Please input an actual name for a file")
        elif not picture_out_file_name.endswith(".png"):
            print("Please enter a png file name")
        else:
            break
    cv2.imwrite("./" + picture_out_file_name, steganography.encode_to_image(
        cv2.imread("./" + picture_file_name), message, public_key))

def decrypt_message_from_image():
    """Decrypts a message from an image."""
    if private_key is None:
        print("Please load a key pair before decrypting a message")
        return
    # get the input image file
    while True:
        picture_file_name = input("Please enter a png file name for the image to decrypt from: ")
        if os.path.exists("./" + picture_file_name) and picture_file_name.endswith(".png"):
            break
        else:
            print("Please input a valid file name")
    print(steganography.decode_from_image(cv2.imread("./" + picture_file_name), private_key))

# run a simple menu in a loop
print("Welcome to my image steganography program")
while True:
    print("\nPlease enter an option:" +
        "\n\t1 Generate new key pair" +
        "\n\t2 Load key pair" +
        "\n\t3 Encrypt message to image" +
        "\n\t4 Decrypt message from image" +
        "\n\t5 Quit")
    option = input()
    # check the input
    if option == "1":
        generate_key_pair()
    elif option == "2":
        load_key_pair()
    elif option == "3":
        encrypt_message_to_image()
    elif option == "4":
        decrypt_message_from_image()
    elif option == "5":
        break
    else:
        print("Please enter a valid option")

print("Goodbye")