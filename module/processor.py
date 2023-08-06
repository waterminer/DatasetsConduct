from random import randint as random
from .data import Data
from PIL import Image
from PIL import ImageEnhance
import numpy as np

class Processor:
    # 在这里定义处理方法
    """
    编写规范如下:
    def 处理名(data:Data,args):
        #代码块
        return data
    """

    def random_crop(data, size):
        if not (data.size[0] <= size or data.size[1] <= size):
            x = random(1, data.size[0] - size)
            y = random(1, data.size[1] - size)
            box = (x, y, x + size, y + size)
            data.img = data.img.crop(box)
            data.conduct += "_rc"
            data.size = data.img.size
        else:
            raise ImageTooSmallError(data.name + data.ext)
        return data

    def flip(data):
        data.img = data.img.transpose(Image.FLIP_LEFT_RIGHT)
        data.conduct += "_f"
        return data

    def resize(data: Data, proportion: float):
        data.size = (int(data.size[0] * proportion), int(data.size[1] * proportion))
        data.img = data.img.resize(data.size)
        data.conduct += "_r"
        return data

    def force_resize(data: Data, size: list):
        data.size = (size[0], size[1])
        data.img = data.img.resize(data.size)
        data.conduct += "_fr"
        return data
    
    def offset(data: Data,offset:int):
        data.img = data.img.offset(offset,0)
        data.conduct += "_off"
        return data
    
    def rotation(data: Data, rot:int):
        data.img = data.img.rotate(rot)
        data.conduct += "_rot"
        return data
    
    def contrast_enhancement(data: Data): #对比度增强
        image = data.img
        enh_con = ImageEnhance.Contrast(image)
        contrast = 1.5
        data.img = enh_con.enhance(contrast)
        data.conduct += "_con_e"
        return data
    
    def brightness_enhancement(data: Data):#亮度增强
        image = data.img
        enh_bri = ImageEnhance.Brightness(image)
        brightness = 1.5
        data.img = enh_bri.enhance(brightness)
        data.conduct += "_bri_e"
        return data

    def color_enhancement(data: Data):#颜色增强
        image = data.img
        enh_col = ImageEnhance.Color(image)
        color = 1.5
        data.img = enh_col.enhance(color)
        data.conduct += "_col_e"
        return data
    
    def random_enhancement(data: Data): #随机抖动
        """
        对图像进行颜色抖动
        :param image: PIL的图像image
        :return: 有颜色色差的图像image
        """
        image = data.img
        random_factor = np.random.randint(8, 31) / 10.  # 随机因子
        color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
        random_factor = np.random.randint(8, 10) / 10.  # 随机因子
        brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
        random_factor = np.random.randint(8, 10) / 10.  # 随机因子
        contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
        random_factor = np.random.randint(8, 20) / 10.  # 随机因子
        data.img = ImageEnhance.Sharpness(contrast_image).enhance(random_factor)  # 调整图像锐度
        data.conduct += "_ran_e"
        return data

    def none(data: Data):
        """
        无操作，主要用于一些特殊场景
        """
        return data

    def append_tag(data: Data, tag: str):
        data.token.append(tag)
        return data

    def remove_tag(data: Data, tag: str):
        if tag in data.token:
            data.token.remove(tag)
        else:
            raise TagNotExistError(tag,data.name + data.ext)
        return data

    def insert_tag(data: Data, tag: str):
        data.token.insert(0, tag)
        return data

    def tag_move_forward(data: Data,tag:str):
        """
        将匹配项放到开头
        """
        if tag in data.token:
            data.token.remove(tag)
        else:
            raise TagNotExistError(tag,data.name + data.ext)
        data.token.insert(0, tag)
        return data
    
    def rename_tag(data:Data,tags:list[str]):
        """
        将Atag改名为Btag
        """
        tag_a = tags[0]
        tag_b = tags[1]
        if tag_a in data.token:
            index = data.token.index(tag_a)
            data.token.insert(index,tag_b)
            data.token.remove(tag_a)
        else:
            raise TagNotExistError(tag_a,data.name + data.ext)
        return data

# 自定义异常
class ProcessorError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ImageTooSmallError(ProcessorError):
    def __init__(self, name: str):
        print("image " + name + " is too small!")

class TagNotExistError(ProcessorError):
    def __init__(self,tag,name: str):
        print("Tag"+ tag + "not exist in"+name+"!")
