from PIL import Image 
import os

class Data:
    conduct = ""
    repeat = 1
    id = 0
    # 图片读取并初始化
    def __init__(self,path:str,name:str,ext:str):
        self.name = name
        self.ext = ext
        self.path = path
        #读取图片
        self.img = Image.open(os.path.join(path,name+ext))
        self.size = self.img.size

    # 载入标签
    def inputToken(self,file_name:str):
        file = open(os.path.join(self.path,file_name),"r")
        self.token = file.read(-1)
        file.close
    
    #保存的方法
    def save(self,output_dir):
        savename=self.name+"_"+str(self.id)+self.conduct
        self.img.save(os.path.join(output_dir,savename+self.ext))
        file = open(os.path.join(output_dir,savename+".txt"),mode="x")
        print(savename)
        file.write(self.token)
        file.close
        self.img.close
