# 说明文档

## 处理方式

用以下方式编写：

``` python
[[{'method':"处理A",'args':512},{'method':"处理B"}],[{'method':"处理B"}]]
```

其中，最内层括号为串联处理，次一层为并联处理

`'method'`参数应该填处理器名称

`args`参数应该填处理器参数

## 处理器说明

|名称|说明|参数1|参数2|
| -- | -- | -- | -- |
|randomcrop|随机裁切矩形图片|图片分辨率（整数）| - |
|flip|水平翻转图片| - | - |
