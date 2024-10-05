# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from stitcher import ImageStitcher

class ImageStitchingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Stitching GUI")
        self.stitcher = ImageStitcher()

        self.image_frames = []
        self.image_paths = []
        self.stitched_image = None

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.add_button = tk.Button(self.frame, text="Add Image", command=self.add_image)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.stitch_button = tk.Button(self.frame, text="Stitch Images", command=self.stitch_images)
        self.stitch_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            try:
                image = Image.open(file_path)
                image.thumbnail((150, 150))
                img = ImageTk.PhotoImage(image)

                frame = tk.Label(self.root, image=img)
                frame.image = img
                frame.pack(side=tk.LEFT, padx=5, pady=5)
                self.image_frames.append(frame)
                self.image_paths.append(file_path)
            except IOError as e:
                messagebox.showerror("Error", "Failed to open image: {}".format(e))

    def stitch_images(self):
        if len(self.image_paths) < 2:
            messagebox.showerror("Error", "Please add at least two images to stitch.")
            return

        images = [cv2.imread(path) for path in self.image_paths]
        try:
            result = self.stitcher.stitch(images)
            self.stitched_image = result
            result_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            result_image = Image.fromarray(result_image)
            result_image_tk = ImageTk.PhotoImage(result_image)

            # Create a new label to display the stitched image
            label = tk.Label(self.root, image=result_image_tk)
            label.image = result_image_tk
            label.pack(padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_image(self):
        if self.stitched_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.stitched_image)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No stitched image to save.")

def main():
    root = tk.Tk()
    app = ImageStitchingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
