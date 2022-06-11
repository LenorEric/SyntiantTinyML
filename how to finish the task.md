# Syntiant TinyML crash tutorial

Lenor

## 基本教程

主要教程参见官方教程。本文只做标注，以及解释各类资源如何使用。

## Clone 完项目后

依照官方教程第 10 页 clone 完项目后，无需按照官方教程新建一个自己的项目，可以直接在 clone 的项目基础上修改。

第一步是在左侧的 data acquisition 中删除所有已经有的数据。

第二步是用手机录制自己的训练集。包括四个文件：

* awake.wav
* light.wav
* shut.wav
* blink.wav

分别包含“唤醒词”、“开灯词”、“关灯词”、“闪烁词”各 50 遍。注意，每个词之间需要包含至少 500 ms 的停顿，每个词的声音大小应当类似，在录制的时候每个词尽可能可以采用不同的语音语调。

如果手机提供的格式不是 wav，需要手动转换为wav格式。

确保自己有 python 环境，目标程序在 python 3.9 中测试通过。

将四个文件放入 ".\\SoundProcess\\source\\" 中，在 ".\\SoundProcess\\" 目录下打开终端，输入

```shell
pip install -r requirements.txt
python .\sound_split.py
```

之后打开 ".\\SoundProcess\\result\\"，试听其中的所有音频，对一个音频中包含多个目标词语或者不包含目标词语的音频进行一个的删。如果生成的音频过少或过多，更改 ".\\SoundProcess\\sound_split.py" 中的 line [8] 的 silence_thresh 为一个更合适的值。这个值代表了语音内容对应的 dBFS 期望平均值。

```python
threshold = -18
```

在保留了全部合适的样本后，将其分别上传到项目中的 Data 里。（使用 upload data）

第一次选择所有 awake 开头的样本，设置：

Automatically split between training and testing 

Enter label: awake

同理，上传余下三种数据。

之后，跳转到官方教程第 17 页。

