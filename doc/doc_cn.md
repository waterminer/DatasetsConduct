# 说明文档

## 安装

需要安装依赖

```txt
python -m venv ./venv
./venv/Scripts/activate
pip install -r ./requirements.txt
```

注意：该版本会安装torch相关的一大堆依赖，如果不想要，可以选择激活别的地方的venv后再来运行  
*如果你不懂我说的是什么意思那你就照着上面指令用就行了*

## 使用方式

参考conf文件进行编写

```yaml
path:
  input: "" #输入路径
  output: "" #输出路径

tagger: #自动打标相关设置
  active: True #启用自动打标
  batch_size: 4 #批次大小
  max_data_loader_n_workers: 1 #越大越占内存

conduct:
  - #处理组1 此处示意为将所有大于512的图片进行翻转
    filters: #用于定义过滤器
    - #过滤器1
      filter: img_filter
      arg: [512,-1]
    processor: #用于定义处理器
    - #处理器1
      method: flip
      arg: 512

#以下为进阶示范
  - #处理组2 此处示意为将1024~2048区间大小的图片进行缩放然后进行随机裁切
    repeat: 3 #用于循环执行(可选)
    filters: #用于定义过滤器
    - #过滤器1
      filter: img_filter
      arg: [1024,2048]
    processor: #用于定义处理器
    - #处理器1
      method: resize
      arg: 0.5
    - #处理器2
      method: random_crop
      arg: 512
```

在默认情况下，文件保存名称为:`id_处理id_重复次数.格式`  
比如:`000001_f_0.jpg`

## 可选项

在yaml中加入option来自定义以下选项

|名称|说明|
|save_sorce_name|保存原文件名称|
|save_conduct_id|保存处理id|
|save_repeat|保存重复次数|
|save_sub|保存子处理|

以下是示例：

```yaml
option:
  save_sorce_name:True
  save_sub:True
```

## 处理器说明

### 图片处理

|名称|处理id|说明|参数|
| -- | -- | -- | -- |
|random_crop|_rc|随机裁切矩形图片|图片分辨率（整数）|
|flip|_f|水平翻转图片| - |
|resize|_r|按比例重新调整大小|比例（浮点数）|
|force_resize|_fr|将图片缩放至特定大小|数组，输入格式为[x,y]|
|offset|_off|将图片偏移n个像素|偏移量（整数）|
|rotation|_rot|将图片选择n个角度|角度(整数)|
|contrast_enhancement|_con_e|对比度增强|-|
|brightness_enhancement|_bri_e|亮度增强|-|
|color_enhancement|_col_e|饱和度增强|-|
|random_enhancement|_ran_e|随机增强|-|
|none|-|不做操作（用于特定场合）|-|

### 标签处理

|名称|说明|参数|
| -- | -- | -- |
|append_tag|在标签组末尾加上标签|标签（文本）|
|remove_tag|删除标签组中符合条件的标签|标签（文本）|
|insert_tag|在标签组开头插入标签|标签（文本）|
|move_forward|将选定标签移到开头|标签（文本）|
|rename_tag|重命名标签，将`A标签`重命名为`B标签`|['A标签','B标签']|

## 过滤器说明

负责过滤符合特定条件的数据

|名称|说明|参数|
| -- | -- | -- |
|img_size|过虑特定尺寸的图片|数组，输入格式为[max,min]，缺省填-1 |
|tag_filter|过滤掉特定标签|标签（文本）|
|tag_selecter|须要包含特定标签|标签（文本）|
|tag_is_not_none|只含有带标签的图片|-|
|tag_is_none|只含有不带标签的图片|-|

## 子处理说明

在配置文件`conduct`项中可以添加`sub_conduct`子处理，在运行中会将子处理的结果作为输入返回主处理

子处理的编写方式与主处理的编写方式相同。

以下是一种子处理的使用示例：

```yaml
conduct:
  - sub_conduct: #将图片进行随机裁切
      -
        filters:
        - filter: img_size
          arg: [1024,1536]
        processor:
        - method: random_crop
          arg: 1024
      -
        filters:
        - filter: img_size
          arg: [1536,2048]
        processor:
        - method: resize
          arg: 0.75
        - method: random_crop
          arg: 1024
    processor: 
      - method: flip #将所有子处理进行翻转
```

当然，如果你想要的话，你可以在子处理中嵌套子处理，这是完全合法的

## 自动打标设置说明

在Tagger后添加`active: True`可以启用自动打标

如果你已经全部完成打标了，依旧打开此项会大大拖慢速度（花时间读取模型）,所以请自行选择是否打开

目前只支持对未打标文件进行打标

以下这下配置是可选的，如果你不清楚是什么，请保持默认

|名称|说明|参数|
|--|--|--|
|active|启用自动打标|布尔值(True/False)|
|model_path|模型路径，下载的模型都会放在此文件夹内|路径|
|model_type|模型种类，具体看下一章|模型种类|
|force_download|强制下载模型|布尔值|
|undesired_tags|排除标签|标签，以英文半角逗号","分隔|
|remove_underscore|以空格替代下划线"_"|布尔值|
|batch_size|每批大小|整数|
|max_data_loader_n_workers|数据读取大小，越大越占内存|整数|
|thresh|置信度，会排除掉比这个值低的标签，默认是0.35|0~1浮点数|
|character_threshold|角色置信度，如果启用，会以这个值单独设置角色标签的推断|0~1浮点数|
|general_threshold|普通标签置信度，如果启用，会以这个值单独设置普通标签置的推断|0~1浮点数|

### 自动打标模型种类

默认参数为`WD14_CONVNEXT`可以按照喜好自行选择
|值|链接|P=R: threshold|F1|
|--|--|--|--|
|WD14_MOAT|[链接](https://huggingface.co/SmilingWolf/wd-v1-4-moat-tagger-v2)|0.3771|0.6911|
|WD14_VIT|[链接](https://huggingface.co/SmilingWolf/wd-v1-4-vit-tagger-v2)|0.3537|0.6770|
|WD14_SWINV2|[链接](https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2)|0.3771|0.6854|
|WD14_CONVNEXT|[链接](https://huggingface.co/SmilingWolf/wd-v1-4-convnext-tagger-v2)|0.3685|0.6810|
|WD14_CONVNEXT2|[链接](https://huggingface.co/SmilingWolf/wd-v1-4-convnextv2-tagger-v2)|0.3710|0.6862|
