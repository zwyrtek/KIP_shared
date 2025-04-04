import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Canvas
from PIL import Image, ImageTk


class InpaintingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inpaint Yellow-Masked Image")

        self.canvas = Canvas(master, width=600, height=400)
        self.canvas.pack()

        self.label = Label(master, text="Upload an image with yellow mask (e.g., yellow rectangle)")
        self.label.pack()

        self.upload_btn = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()

        self.inpaint_btn = Button(master, text="Inpaint Image", command=self.inpaint_image, state='disabled')
        self.inpaint_btn.pack()

        self.image = None
        self.mask = None
        self.tk_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if not file_path:
            return

        self.image = cv2.imread(file_path)

        # Detect yellow mask
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        self.mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        self.show_image(self.image)
        self.inpaint_btn.config(state='normal')
        self.label.config(text="Yellow mask detected. Click 'Inpaint Image'.")

    def inpaint_image(self):
        if self.image is None or self.mask is None:
            return

        inpainted = cv2.inpaint(self.image, self.mask, 3, cv2.INPAINT_TELEA)
        self.show_image(inpainted)
        self.label.config(text="Inpainting completed!")

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil = image_pil.resize((600, 400), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)


if __name__ == "__main__":
    root = Tk()
    app = InpaintingApp(root)
    root.mainloop()
