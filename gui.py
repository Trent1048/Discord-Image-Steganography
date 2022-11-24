import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog

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
        key_menu.add_command(label="Generate Pair", command=self.placeholder)
        key_menu.add_command(label="Load Pair", command=self.placeholder)
        menu_bar.add_cascade(label="Keys", menu=key_menu)
        self.config(menu=menu_bar)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # setup text box
        text_box = tk.Text(self, width=25, height=15)
        text_box.grid(row=0, column=1)

        # setup image display
        self.image_holder = tk.Label(self, text="No File Loaded", foreground="red")
        self.image_holder.grid(row=0, column=0)

        # setup load and export and read buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0)
        self.load_image_button = tk.Button(self.button_frame, 
            text="Load Image", command=self.set_image)
        self.load_image_button.grid(row=0, column=0)
        self.export_message_button = tk.Button(self.button_frame, 
            text="Export Message", command=self.placeholder)
        self.export_message_button.grid(row=0, column=1)
        self.read_message_button = tk.Button(self.button_frame, 
            text="Read Message", command=self.placeholder)
        self.read_message_button.grid(row=0, column=2)

    def placeholder(self):
        pass

    def set_image(self):
        """Sets the image for the selected image display box."""
        image_path = filedialog.askopenfilename()
        if image_path.lower().endswith(".png"):
            image_source = Image.open(image_path)
            image_source.thumbnail((200, 200))
            self.image = ImageTk.PhotoImage(image_source)
            self.image_holder.configure(image=self.image)
            self.selected_image_path = image_path
        else:
            self.image_holder.configure(image="", text="Must select a .png image")

if __name__ == "__main__":
    app = SteganographyUI()
    app.mainloop()