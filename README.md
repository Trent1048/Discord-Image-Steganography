# Image Steganography
## Motivation and Problem
This project seeks to provide a way for users to send encrypted messages concealed as harmless images. This would be useful in situations where users don’t want to alert outside parties that there are secret messages being sent even if their private communication channel is compromised.
## Description of the Contribution
The project will result in an application where users link their discord account and input the private key of their message recipient. Then they will input their message in the application, which will be encrypted using the public key, hidden into an image using steganography, which is exported so they can send it to their message recipient, and then decrypted using the user’s private key after importing it on the other end. The image data is hidden into will be either manually selected by the user or pulled from a google images search of a specified topic such as “programmer memes.”
