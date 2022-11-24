import cv2
import encryption
import steganography
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox

class SteganographyUI(tk.Tk):
    """The GUI for the image steganography program."""

    def __init__(self):
        """Initializes the user interface for the steganography program."""
        super().__init__()

        # configure window
        self.title("Image Steganography")
        self.geometry("500x300")
        self.resizable(0, 0)

        # setup menu bar
        menu_bar = tk.Menu(self)
        key_menu = tk.Menu(menu_bar, tearoff=0)
        key_menu.add_command(label="Generate Pair", command=self.generate_key_pair)
        key_menu.add_command(label="Load Public Key", command=self.load_public_key)
        key_menu.add_command(label="Load Private Key", command=self.load_private_key)
        key_menu.add_separator()
        key_menu.add_command(label="Set Pair", command=self.set_key_pair)
        menu_bar.add_cascade(label="Keys", menu=key_menu)
        self.config(menu=menu_bar)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # setup text box
        self.text_box = tk.Text(self, width=25, height=15)
        self.text_box.grid(row=0, column=1)

        # setup image display
        self.image_holder = tk.Label(self, text="No File Loaded", foreground="red")
        self.image_holder.grid(row=0, column=0)
        self.selected_image_path = None

        # setup load and export and read buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0)
        self.load_image_button = tk.Button(self.button_frame, 
            text="Load Image", command=self.set_image)
        self.load_image_button.grid(row=0, column=0)
        self.export_message_button = tk.Button(self.button_frame, 
            text="Export Message", command=self.export_message)
        self.export_message_button.grid(row=0, column=1)
        self.read_message_button = tk.Button(self.button_frame, 
            text="Read Message", command=self.read_message)
        self.read_message_button.grid(row=0, column=2)

        # initialize the keys and file paths
        self.public_key_file = None
        self.private_key_file = None
        self.public_key = None
        self.private_key = None

    def generate_key_pair(self):
        """Generates a key pair for encryption/decryption."""
        public_key_file = filedialog.asksaveasfilename(
            initialfile="publicKey.pem", filetypes=[("PEM File", ".pem")])
        private_key_file = filedialog.asksaveasfilename(
            initialfile="privateKey.pem", filetypes=[("PEM File", ".pem")])
        encryption.generate_key_pair(public_key_file, private_key_file)

    def load_public_key(self):
        """Loads the public key for encryption."""
        self.public_key_file = filedialog.askopenfilename(filetypes=[("PEM File", ".pem")])

    def load_private_key(self):
        """Loads the private key for decryption."""
        self.private_key_file = filedialog.askopenfilename(filetypes=[("PEM File", ".pem")])

    def set_key_pair(self):
        """Sets the key pair to be used for encryption/decryption."""
        if self.public_key_file is None or self.private_key_file is None:
            messagebox.showwarning(title="Warning", message="Must load public and private key first")
        else:
            self.public_key, self.private_key = encryption.read_key_pair(self.public_key_file, self.private_key_file)

    def set_image(self):
        """Sets the image for the selected image display box."""
        image_path = filedialog.askopenfilename(filetypes=[("PNG File", ".png")])
        image_source = Image.open(image_path)
        image_source.thumbnail((200, 200))
        self.image = ImageTk.PhotoImage(image_source)
        self.image_holder.configure(image=self.image)
        self.selected_image_path = image_path

    def export_message(self):
        """Encrypts and hides a message into an image."""
        if self.selected_image_path is None:
            messagebox.showwarning(title="Warning", message="Must select an image first")
        elif self.public_key is None:
            messagebox.showwarning(title="Warning", message="Must set a key pair first")
        else:
            message = self.text_box.get("1.0", "end")
            output_image_path = filedialog.asksaveasfilename(filetypes=[("PNG File", ".png")])
            cv2.imwrite(output_image_path, steganography.encode_to_image(
                cv2.imread(self.selected_image_path), message, self.public_key))

    def read_message(self):
        """Reads the encrypted message from the selected file."""
        if self.selected_image_path is None:
            messagebox.showwarning(title="Warning", message="Must select an image first")
        elif self.private_key is None:
            messagebox.showwarning(title="Warning", message="Must set a key pair first")
        else:
            self.text_box.delete("1.0", "end")
            try:
                self.text_box.insert("1.0", steganography.decode_from_image(
                    cv2.imread(self.selected_image_path), self.private_key))
            except Exception as e:
                self.text_box.insert("1.0", str(e))
                self.text_box.tag_config("red", foreground="red")
                self.text_box.tag_add("red", "1.0", "end")

if __name__ == "__main__":
    app = SteganographyUI()
    app.mainloop()