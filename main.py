import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from backend import *

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.image = None
        self.original_image = None

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.btn_load = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_load.pack(side=tk.LEFT)

        self.btn_capture = tk.Button(root, text="Capture from Webcam", command=self.capture_image)
        self.btn_capture.pack(side=tk.LEFT)

        self.channel_var = tk.StringVar(value="none")
        self.red_channel = tk.Radiobutton(root, text="Red Channel", variable=self.channel_var, value="red", command=self.update_image)
        self.red_channel.pack(side=tk.LEFT)
        self.green_channel = tk.Radiobutton(root, text="Green Channel", variable=self.channel_var, value="green", command=self.update_image)
        self.green_channel.pack(side=tk.LEFT)
        self.blue_channel = tk.Radiobutton(root, text="Blue Channel", variable=self.channel_var, value="blue", command=self.update_image)
        self.blue_channel.pack(side=tk.LEFT)

        self.blur_label = tk.Label(root, text="Gaussian Blur Kernel Size:")
        self.blur_label.pack(side=tk.LEFT)
        self.blur_entry = tk.Entry(root)
        self.blur_entry.pack(side=tk.LEFT)

        self.btn_blur = tk.Button(root, text="Apply Blur", command=self.apply_blur)
        self.btn_blur.pack(side=tk.LEFT)

        self.btn_gray = tk.Button(root, text="Convert to Gray", command=self.convert_to_gray)
        self.btn_gray.pack(side=tk.LEFT)

        self.line_coords_label = tk.Label(root, text="Line Coords (x1,y1,x2,y2):")
        self.line_coords_label.pack(side=tk.LEFT)
        self.line_coords_entry = tk.Entry(root)
        self.line_coords_entry.pack(side=tk.LEFT)

        self.line_thickness_label = tk.Label(root, text="Line Thickness:")
        self.line_thickness_label.pack(side=tk.LEFT)
        self.line_thickness_entry = tk.Entry(root)
        self.line_thickness_entry.pack(side=tk.LEFT)

        self.btn_draw_line = tk.Button(root, text="Draw Line", command=self.draw_line)
        self.btn_draw_line.pack(side=tk.LEFT)

        self.btn_reset = tk.Button(root, text="Reset Image", command=self.reset_image)
        self.btn_reset.pack(side=tk.LEFT)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = load_image(file_path)
                self.original_image = self.image.copy()
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def capture_image(self):
        try:
            self.image = capture_from_webcam()
            self.original_image = self.image.copy()
            self.display_image(self.image)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_image(self):
        if self.image is not None:
            try:
                channel = self.channel_var.get()
                if channel != "none":
                    img = show_channel(self.image, channel)
                else:
                    img = self.image
                self.display_image(img)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def apply_blur(self):
        if self.image is not None:
            try:
                kernel_size = int(self.blur_entry.get())
                self.image = apply_gaussian_blur(self.image, kernel_size)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def convert_to_gray(self):
        if self.image is not None:
            try:
                self.image = convert_to_gray(self.image)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def draw_line(self):
        if self.image is not None:
            try:
                coords = list(map(int, self.line_coords_entry.get().split(',')))
                thickness = int(self.line_thickness_entry.get())
                self.image = draw_line(self.image, (coords[0], coords[1]), (coords[2], coords[3]), thickness)
                self.display_image(self.image)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def display_image(self, img):
        if len(img.shape) == 2:  # Grayscale image
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
