import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import webptools
import os

def convert_image(input_path, output_format):
    img = Image.open(input_path)
    output_path = os.path.splitext(input_path)[0] + f'.{output_format}'
    
    if output_format == 'png':
        img.save(output_path, 'PNG')
    elif output_format == 'webp':
        webptools.dwebp(input_path, '-o', output_path)
    return output_path

def open_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.webp")])
    if file_paths:
        for file_path in file_paths:
            add_image_to_list(file_path)

def add_image_to_list(file_path):
    img_listbox.insert(tk.END, file_path)

def convert_selected_images(output_format):
    selected_items = img_listbox.curselection()
    for index in selected_items:
        input_path = img_listbox.get(index)
        output_path = convert_image(input_path, output_format)
        result_text.insert(tk.END, f"Converted {input_path} to {output_format}: {output_path}\n")

app = tk.Tk()
app.title("Image Format Converter")

open_button = tk.Button(app, text="Open Images", command=open_files)
open_button.pack(pady=10)

img_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE)
img_listbox.pack()

convert_png_button = tk.Button(app, text="Convert to PNG", command=lambda: convert_selected_images('png'))
convert_png_button.pack()

convert_webp_button = tk.Button(app, text="Convert to WebP", command=lambda: convert_selected_images('webp'))
convert_webp_button.pack()

result_text = tk.Text(app, height=10, width=50)
result_text.pack(pady=10)

app.mainloop()
