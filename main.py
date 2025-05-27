import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
from typing import Union
import os
import sys


def app():
    # PARAMETERS
    image_dict: dict[str, Union[ImageTk.PhotoImage, Image, None]] =\
        {"image": None, # Type: PhotoImage
        "outer_image_canvas": None, # Type: PhotoImage
        "final_image": None, # Type: PhotoImage
        "final_image_canvas": None# Type: PhotoImage
         }

    # BUTTON FUNCTIONS
    def load_button():
        filepath = filedialog.askopenfile(mode="r", filetypes=[("Images", ["*.png", "*.jpg", "*.jpeg"])])
        if filepath is None:
            return
        with Image.open(fp=filepath.name) as loaded_image:
            display_image = ImageOps.fit(image=loaded_image,
                                         size=(800, 450),
                                         method=Image.Resampling.LANCZOS,
                                         bleed=0,
                                         centering=(0.5, 0.5)
                                         )
            image_dict["outer_image_canvas"] = ImageTk.PhotoImage(image=display_image)
        canvas.create_image(0, 0, image=image_dict["outer_image_canvas"], anchor="nw")
        image_dict["image"] = loaded_image


    def set_watermark():
        if hasattr(sys, '_MEIPASS'):
            # Use the temporary extraction directory for the executable
            base_path = sys._MEIPASS
        else:
            # Use the current directory when running as a Python script
            base_path = os.path.dirname(__file__)

        # Loads the watermark image
        image_path = os.path.join(base_path, "assets/watermark.png")
        watermark_img = Image.open(fp=image_path)
        if image_dict["image"] is None:
            return

        # Get dimensions of each image
        width1, height1 = image_dict["image"].size
        width2, height2 = watermark_img.size

        # Find center pixel of outer image
        center_x, center_y = (width1 / 2), (height1 / 2)

        # Offset inner image to align its center
        im2_x = center_x - (width2 / 2)
        im2_y = center_y - (height2 / 2)

        # Paste inner image over outer image
        back_im = image_dict["image"].copy()
        back_im.paste(watermark_img, (int(im2_x), int(im2_y)), watermark_img)
        image_dict["final_image"] = back_im

        # Change canvas image to watermarked image
        display_image = ImageOps.fit(image=back_im,
                                     size=(800, 450),
                                     method=Image.Resampling.LANCZOS,
                                     bleed=0,
                                     centering=(0.5, 0.5)
                                     )
        image_dict["final_image_canvas"] = ImageTk.PhotoImage(display_image)
        canvas.create_image(0, 0, image=image_dict["final_image_canvas"], anchor="nw")
        messagebox.showinfo(title="Success", message="Image watermarked correctly")


    def save_image():
        filepath = filedialog.asksaveasfilename(filetypes=[("Images", ["*.png", "*.jpg", "*.jpeg"])])
        if filepath is None:
            return
        filepath = filepath + ".png"
        image_to_save = image_dict["final_image"]
        if image_to_save is None:
            return
        image_to_save.save(fp=filepath)

    # GUI STARTS HERE
    root = tk.Tk()
    root.geometry("900x562")
    root.resizable(False, False)
    root.grid_columnconfigure((1,2,3), weight=1)
    root.title("Automatic Watermarker for NogaDevs")

    load_img_btn = ttk.Button(root, command=load_button, text="UPLOAD IMAGE", width=30)
    load_img_btn.grid(row=0, column=0, sticky="ew", pady=15, padx=50)

    set_watermark_btn = ttk.Button(root, command=set_watermark, text="SET WATERMARK", width=30)
    set_watermark_btn.grid(row=0, column=1, sticky="ew", pady=15, padx=50)

    save_btn = ttk.Button(root, command=save_image, text="SAVE", width=30)
    save_btn.grid(row=0, column=2, sticky="ew", pady=15, padx=50)

    canvas = tk.Canvas(root, width=800, height=450)
    canvas.grid(row=1, column=0,rowspan=2, columnspan=3, pady=15, padx=30)


    # GUI FINISHES HERE

    root.mainloop()

if __name__ == "__main__":
    app()
