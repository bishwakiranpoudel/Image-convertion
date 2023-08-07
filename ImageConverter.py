import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import webptools
import os

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Format Conversion App")

        self.output_directory_var = tk.StringVar()
        self.images_to_convert = []

        self.create_widgets()

    def create_widgets(self):
        open_button = tk.Button(self.root, text="Open Images", command=self.open_files)
        open_button.pack(pady=10)

        self.img_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        self.img_listbox.pack()

        output_dir_frame = tk.Frame(self.root)
        output_dir_frame.pack(pady=5)

        output_dir_label = tk.Label(output_dir_frame, text="Output Directory:")
        output_dir_label.pack(side=tk.LEFT)

        self.output_dir_entry = tk.Entry(output_dir_frame, textvariable=self.output_directory_var)
        self.output_dir_entry.pack(side=tk.LEFT, padx=5)

        output_dir_button = tk.Button(output_dir_frame, text="Browse", command=self.choose_output_directory)
        output_dir_button.pack(side=tk.LEFT)

        convert_frame = tk.Frame(self.root)
        convert_frame.pack(pady=10)

        convert_png_button = tk.Button(convert_frame, text="Convert to PNG", command=lambda: self.convert_selected_images('png'))
        convert_png_button.pack(side=tk.LEFT, padx=5)

        convert_webp_button = tk.Button(convert_frame, text="Convert to WebP", command=lambda: self.convert_selected_images('webp'))
        convert_webp_button.pack(side=tk.LEFT, padx=5)

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(pady=10)

    def open_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.webp")])
        if file_paths:
            for file_path in file_paths:
                self.add_image_to_list(file_path)

    def add_image_to_list(self, file_path):
        self.img_listbox.insert(tk.END, os.path.basename(file_path))
        self.images_to_convert.append(file_path)

    def choose_output_directory(self):
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory_var.set(output_directory)

    def convert_selected_images(self, output_format):
        output_directory = self.output_directory_var.get()
        if not output_directory:
            self.result_text.insert(tk.END, "Please choose an output directory.\n")
            return

        selected_items = self.img_listbox.curselection()
        for index in selected_items:
            input_path = self.images_to_convert[index]
            self.convert_image(input_path, output_format, output_directory)

    def convert_image(self, input_path, output_format, output_directory):
        img = Image.open(input_path)
        output_filename = os.path.basename(input_path).replace(os.path.splitext(input_path)[1], f'.{output_format}')
        output_path = os.path.join(output_directory, output_filename)

        if output_format == 'png':
            img.save(output_path, 'PNG')
        elif output_format == 'webp':
            webptools.dwebp(input_path, '-o', output_path)

        self.result_text.insert(tk.END, f"Converted {os.path.basename(input_path)} to {output_format}: {output_path}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
