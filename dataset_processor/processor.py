from random import randint as random
from .data import Data
from .tools.tagger import Tagger
from .tools.upscale import UpscaleModel
from .tools.smartcrop import SmartCrop
from PIL import Image
from PIL import ImageEnhance
import numpy as np


class Processor:
    """
    这是一个处理器类，包含所有有关数据处理的函数
    编写规范如下:
    def 处理名(data:Data,args)->Data:
        #代码块
        return data
    """

    def random_crop(data: Data, size) -> Data:
        if not (data.size[0] <= size or data.size[1] <= size):
            x = random(1, data.size[0] - size)
            y = random(1, data.size[1] - size)
            box = (x, y, x + size, y + size)
            data.img = data.img.crop(box)
            data.conduct += f"_rc{data.repeat}"
            data.size = data.img.size
        else:
            raise ImageTooSmallError(data.name + data.ext)
        return data

    def flip(data: Data) -> Data:
        data.img = data.img.transpose(Image.FLIP_LEFT_RIGHT)
        data.conduct += f"_f{data.repeat}"
        return data

    def resize(data: Data, proportion: float) -> Data:
        size = (int(data.size[0] * proportion), int(data.size[1] * proportion))
        data.img = data.img.resize(size)
        data.conduct += f"_r{data.repeat}"
        data.size = data.img.size
        return data

    def force_resize(data: Data, size: list) -> Data:
        """
        size: [x,y]
        """
        data.img = data.img.resize(size)
        data.conduct += f"_fr{data.repeat}"
        data.size = data.img.size
        return data

    def offset(data: Data, offset: int) -> Data:
        data.img = data.img.offset(offset, 0)
        data.conduct += f"_off{data.repeat}"
        return data

    def rotation(data: Data, rot: int) -> Data:
        data.img = data.img.rotate(rot)
        data.conduct += f"_rot{data.repeat}"
        return data

    def contrast_enhancement(data: Data) -> Data:  # 对比度增强
        image = data.img
        enh_con = ImageEnhance.Contrast(image)
        contrast = 1.5
        data.img = enh_con.enhance(contrast)
        data.conduct += f"_con_e{data.repeat}"
        return data

    def brightness_enhancement(data: Data) -> Data:  # 亮度增强
        image = data.img
        enh_bri = ImageEnhance.Brightness(image)
        brightness = 1.5
        data.img = enh_bri.enhance(brightness)
        data.conduct += f"_bri_e{data.repeat}"
        return data

    def color_enhancement(data: Data) -> Data:  # 颜色增强
        image = data.img
        enh_col = ImageEnhance.Color(image)
        color = 1.5
        data.img = enh_col.enhance(color)
        data.conduct += "_col_e"
        return data

    def random_enhancement(data: Data) -> Data:  # 随机抖动
        image = data.img
        random_factor = np.random.randint(8, 31) / 10.  # 随机因子
        color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
        random_factor = np.random.randint(8, 10) / 10.  # 随机因子
        brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
        random_factor = np.random.randint(8, 10) / 10.  # 随机因子
        contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
        random_factor = np.random.randint(8, 20) / 10.  # 随机因子
        data.img = ImageEnhance.Sharpness(contrast_image).enhance(random_factor)  # 调整图像锐度
        data.conduct += f"_ran_e{data.repeat}"
        return data

    def none(data: Data) -> Data:
        """
        无操作，主要用于一些特殊场景
        """
        return data

    def append_tag(data: Data, tag: str) -> Data:
        data.token.append(tag)
        return data

    def remove_tag(data: Data, tag: str) -> Data:
        if tag in data.token:
            data.token.remove(tag)
        else:
            raise TagNotExistError(tag, data.name + data.ext)
        return data

    def insert_tag(data: Data, tag: str) -> Data:
        data.token.insert(0, tag)
        return data

    def tag_move_forward(data: Data, tag: str) -> Data:
        """
        将匹配项放到开头
        """
        if tag in data.token:
            data.token.remove(tag)
        else:
            raise TagNotExistError(tag, data.name + data.ext)
        data.token.insert(0, tag)
        return data

    def rename_tag(data: Data, tags: list[str]) -> Data:
        """
        将Atag改名为Btag
        """
        tag_a = tags[0]
        tag_b = tags[1]
        if tag_a in data.token:
            index = data.token.index(tag_a)
            data.token.insert(index, tag_b)
            data.token.remove(tag_a)
        else:
            raise TagNotExistError(tag_a, data.name + data.ext)
        return data

    def tag_image(data: Data, tagger: Tagger)->Data:
        return tagger.tag_data(data)

    def upscale_image(data: Data, upscale: UpscaleModel)->Data:
        data.img = upscale.upscale_data(data)
        data.size = data.img.size
        return data
    
    def convert_to_white_background(data:Data)->Data:
        if data.img.mode=="RGBA":
            new_img = Image.new("RGB",data.size,(255,255,255))
            new_img.paste(data.img,(0,0),mask=data.img)
            data.img = new_img
            data.img.convert("RGB")
            data.ext=".jpg"
            data.conduct+="_cwb"
        return data

    def smart_crop(data:Data,size:list)->Data:
        """
        size: [x,y]
        """
        size = tuple(size)
        smart_crop = SmartCrop()
        data = Processor.convert_to_white_background(data)
        top_crop = smart_crop.crop(data.img,100,100)['top_crop']
        #下面这大堆东西都是限位用的
        long_side = max(top_crop['width'],top_crop['height'])
        long_side_limit = min(data.size[0],data.size[1])
        if long_side > long_side_limit:
            long_side = long_side_limit
        limit = (data.size[0]-long_side,data.size[1]-long_side)
        if top_crop['x'] <= limit[0]:
            x=top_crop['x'] 
        else:
            x= limit[0]
        if top_crop['y'] <= limit[1]:
            y=top_crop['y'] 
        else:
            y= limit[1]
        box = (x,y,x+long_side,y+long_side)
        data.img = data.img.crop(box).resize(size)
        data.size = data.img.size
        data.conduct += "_sc"
        return data


# 自定义异常
class ProcessorError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ImageTooSmallError(ProcessorError):
    def __init__(self, name: str):
        print("image " + name + " is too small!")


class TagNotExistError(ProcessorError):
    def __init__(self, tag, name: str):
        print("Tag" + tag + "not exist in" + name + "!")
