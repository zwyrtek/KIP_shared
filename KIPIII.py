import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Canvas, StringVar, OptionMenu
from PIL import Image, ImageTk


class ManualInpaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Manual Inpaint - Draw Mask")

        self.canvas = Canvas(master, width=600, height=400, bg='black')
        self.canvas.pack()

        self.label = Label(master, text="Draw mask with mouse (left = draw, right = erase).")
        self.label.pack()

        self.upload_btn = Button(master, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()

        self.clear_btn = Button(master, text="Clear Mask", command=self.clear_mask, state='disabled')
        self.clear_btn.pack()

        self.inpaint_btn = Button(master, text="Inpaint Image", command=self.inpaint_image, state='disabled')
        self.inpaint_btn.pack()

        self.save_btn = Button(master, text="Save Result", command=self.save_image, state='disabled')
        self.save_btn.pack()

        self.alg_var = StringVar(value='TELEA')
        self.alg_menu = OptionMenu(master, self.alg_var, 'TELEA', 'NS')
        self.alg_menu.pack()

        self.image = None
        self.mask = None
        self.result = None
        self.tk_image = None
        self.preview = None

        self.canvas.bind("<B1-Motion>", self.draw_mask)
        self.canvas.bind("<B3-Motion>", self.erase_mask)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if not file_path:
            return

        self.image = cv2.imread(file_path)
        self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        self.preview = self.image.copy()
        self.result = None

        self.show_image(self.preview)
        self.inpaint_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        self.save_btn.config(state='disabled')
        self.label.config(text="Draw or erase mask with mouse.")

    def draw_mask(self, event):
        self._update_mask(event, draw=True)

    def erase_mask(self, event):
        self._update_mask(event, draw=False)

    def _update_mask(self, event, draw=True):
        if self.image is None:
            return
        x = int(event.x * self.image.shape[1] / self.canvas.winfo_width())
        y = int(event.y * self.image.shape[0] / self.canvas.winfo_height())
        color = 255 if draw else 0
        cv2.circle(self.mask, (x, y), 10, color, -1)
        preview = self.image.copy()
        preview[self.mask == 255] = (0, 0, 255)
        self.preview = preview
        self.show_image(preview)

    def clear_mask(self):
        if self.image is None:
            return
        self.mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        self.preview = self.image.copy()
        self.show_image(self.preview)
        self.label.config(text="Mask cleared.")

    def inpaint_image(self):
        if self.image is None or self.mask is None:
            return
        method = cv2.INPAINT_TELEA if self.alg_var.get() == 'TELEA' else cv2.INPAINT_NS
        self.result = cv2.inpaint(self.image, self.mask, 3, method)
        self.preview = self.result
        self.show_image(self.result)
        self.label.config(text=f"Inpainting done using {self.alg_var.get()}.")
        self.save_btn.config(state='normal')

    def save_image(self):
        if self.result is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png"),
                                                            ("JPEG Image", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.result)
            self.label.config(text=f"Result saved to: {file_path}")

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil = image_pil.resize((600, 400), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)


if __name__ == "__main__":
    root = Tk()
    app = ManualInpaintApp(root)
    root.mainloop()
