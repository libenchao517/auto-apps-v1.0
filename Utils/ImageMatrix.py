################################################################################
# 本文件用于生成一个m行n列的图像矩阵
################################################################################
# 导入模块
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
################################################################################
# 定义图像矩阵APP
class Image_Matrix_App:
    def __init__(self, root, m, n):
        self.root = root
        self.m = m
        self.n = n
        self.left = None
        self.right = None
        self.buttons = []
        default_score = min(0.72/m, 1.08/n)
        str_score = "{:.2f}".format(default_score)
        self.images = [[None for _ in range(n)] for _ in range(m)]
        self.scale_factor = tk.StringVar(value=str_score)
        self.setup_ui()

    def setup_ui(self):
        for i in range(self.m):
            row = []
            for j in range(self.n):
                button = tk.Button(self.root, text="Add Image", command=lambda i=i, j=j: self.add_image(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        scale_label = tk.Label(self.root, text="Scale Factor:")
        scale_label.grid(row=self.m, column=0, columnspan=self.n // 2)
        scale_entry = tk.Entry(self.root, textvariable=self.scale_factor)
        scale_entry.grid(row=self.m, column=self.n // 2, columnspan=self.n // 2)
        show_button = tk.Button(self.root, text="Show All Images", command=self.show_images)
        show_button.grid(row=self.m + 1, column=0, columnspan=self.n)

    def add_image(self, i, j):
        file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif")])
        if file_path:
            self.images[i][j] = Image.open(file_path)
            if self.left is None or self.right is None:
                self.left = self.images[i][j].size[0]
                self.right = self.images[i][j].size[1]
            self.buttons[i][j].config(text="Inserted", bg="lightgreen")

    def show_images(self):
        show_window = tk.Toplevel(self.root)
        show_window.title("All Images")
        scale_factor = float(self.scale_factor.get())
        for i in range(self.m):
            for j in range(self.n):
                if self.images[i][j]:
                    image = self.images[i][j]
                    image.thumbnail((self.left * scale_factor, self.right * scale_factor))  # 按比例缩放
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(show_window, image=photo)
                    label.image = photo
                else:
                    label = tk.Label(show_window, bg="white", width=self.left * scale_factor, height=self.right * scale_factor)
                label.grid(row=i, column=j)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        show_window.geometry(f"{screen_width}x{screen_height}")
################################################################################
# 调用图像矩阵APP
class Image_Matrix:
    def __init__(self, m=3, n=3):
        """
        调用图像矩阵APP
        :param m: 图像矩阵的行数
        :param n: 图像矩阵的列数
        # >>> Image_Matrix(2, 4)
        """
        root = tk.Tk()
        root.title("Image Matrix")
        app = Image_Matrix_App(root, m, n)
        root.mainloop()
