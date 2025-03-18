################################################################################
# 本文件存储一些图片操作函数
################################################################################
# 导入模块
from PIL import Image
################################################################################
# 定义必要函数
def tif_to_pdf(file):
    image = Image.open(file+".tif")
    rgb_image = image.convert('RGB')
    rgb_image.save(file+".pdf")

def tif_to_png(file):
    image = Image.open(file+".tif")
    rgb_image = image.convert('RGB')
    rgb_image.save(file+".png")

def tif_to_eps(file):
    image = Image.open(file+".tif")
    rgb_image = image.convert('RGB')
    rgb_image.save(file+".eps")

def png_to_eps(file):
    image = Image.open(file+".png")
    rgb_image = image.convert('RGB')
    rgb_image.save(file+".eps")

def to_gray(file):
    image = Image.open(file)
    gray_image = image.convert('L')
    file = file.split(".")
    file = file[0] + "_gray." + file[1]
    gray_image.save(file)
