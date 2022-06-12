# Syntiant TinyML crash tutorial

Lenor

## 符号简介

:floppy_disk:: 这个符号代表对应的内容是个文件，且可以在 ".\\resource" 中找到

:arrow_left:: 这个符号代表当你阅读本文到这个位置时，需要中断并跳转到官方教程的特定位置继续阅读。

:arrow_right:: 这个符号代表当你阅读官方教程到特定位置时，需要中断并跳转到本文继续阅读。

:arrow_right_hook:: 这个符号代表当你阅读官方教程到特定位置时，需要注意这里的内容并继续阅读。

## 基本教程

主要教程参见官方教程 :floppy_disk: Syntiant_TinyML Tutorial (Windows).pdf 。本文只做标注，以及解释各类资源如何使用。官方教程正式从第 9 页开始。

:arrow_right:依照官方教程第 10 页 clone 完项目后，无需按照官方教程新建一个自己的项目，可以直接在 clone 的项目基础上修改。

第一步是在左侧的 data acquisition 中删除所有已经有的数据。在顶部栏中有训练集和测试集，两者都需要删光。

第二步是用手机录制自己的训练集。包括五个文件：

* awake.wav
* light.wav
* shut.wav
* blink.wav
* noise.wav

分别包含“唤醒词”、“开灯词”、“关灯词”、“闪烁词”各 40 遍，每个词长度约为 1 秒，以及测试环境下的噪声（应当约为 40 秒）。注意，每个词之间需要包含至少 500 ms 的停顿，每个词的声音大小应当类似，在录制的时候每个词尽可能可以采用不同的语音语调，且录制环境应当尽可能安静。

*Tips: 四个词之间的差别越大越好，这样可以在较少训练集的情况下提供更高的识别精度。例如 ”开灯“ 、”关灯“ 不是一对好的识别词，而 ”开灯“ 、”熄灭“ 则是一对好的识别词。*

如果手机提供的格式不是 wav，需要手动转换为wav格式。

确保自己有 python 环境，目标程序在 python 3.9 中测试通过。

将四个文件放入 ".\\SoundProcess\\source\\" 中，在 ".\\SoundProcess\\" 目录下打开终端，输入

```shell
pip install -r requirements.txt
python .\sound_split.py
```

之后打开 ".\\SoundProcess\\result\\"，试听其中的所有音频，对一个音频中包含多个目标词语或者不包含目标词语的音频进行一个的删。如果生成的音频过少或过多，更改 ".\\SoundProcess\\sound_split.py" 中的 line [9] 的 silence_thresh 为一个更合适的值。这个值代表了语音内容对应的 dBFS 期望平均值。

```python
threshold = -18
```

在保留了全部合适的样本后，将其分别上传到项目中的 Data 里。（使用 upload data）

第一次选择所有 awake 开头的样本，设置：

Automatically split between training and testing 

Enter label: awake

同理，上传余下三种数据。

:arrow_left:之后，跳转到官方教程第 13 页。

:arrow_right_hook: @Page18 这里生成的 Feature 图像可能不一定是三维的，原因未知

:arrow_right_hook: @Page20 模型正确率不应当低于 90%，否则检查以上步骤是否出错。

:arrow_right_hook: @Page21 需要勾选 awake 等全部五个选项。

:arrow_right: @Page22 解压 :floppy_disk: arduino-cli_0.23.0_Windows_64bit.zip 到一个新建的特定的英文路径目录，并将这个目录添加到系统路径（Path）。

**重启电脑**。使用 micro usb 数据线将 Syntiant TinyML 开发板连接至电脑。检查其连接状况：

<img src="how to finish the task.assets/image-20220612060450512-16549877297541.png" alt="image-20220612060450512" style="zoom:80%;" />

返回浏览器，检查是否下载了类似 :floppy_disk: syntiant-rc-go-stop-syntiant-ndp101-v46.zip 的文件并解压至一个  :floppy_disk: 新建的独立目录。运行其中的 flash_windows.bat。初次运行可能需要下载部分文件。如果程序卡在 Flashing Arduino firmware... 则按下（或尝试双击）开发板上的 reset 按键并重启 flash_windows.bat，如果出现其他错误，参见官方教程 :arrow_left: @Page34 到 :arrow_right: @Page36。否则按照提示操作。

程序正常烧录后，关闭官方教程，并确保你的电脑上有 Arduino IDE。

用 Arduino IDE 打开 :floppy_disk: firmware-syntiant-tinyml-model 中的 firmware-syntiant-tinyml-model.ino。对其进行必要的修改以实现 “开灯”、“关灯” 等功能，实现思路可以参照 :floppy_disk: firmware-syntiant-tinyml。

大致要做的事情包括：

* 使用在 Edge Impluse 中，Deployment 中选择 Syntiant NDP101 library 下载到的类似 :floppy_disk: syntiant-rc-go-stop-syntiant-ndp101-lib-v48.zip 的文件中的内容替换 src 目录中的内容。
* 修改 firmware-syntiant-tinyml-model.ino 是其能够识别自定义指令，并修改状态位。
* 在 ".\\src\\syntiant.cpp" 的 syntiant_loop() 中加入相关函数以处理指令。

**代码一定不要照抄哦，里面包含用户信息的	**

目前已知的坑：

* \firmware-syntiant-tinyml\src\model-parameters-backup\model_variables.h 中，引用了 #include "../edge-impulse-sdk/classifier/ei_model_types.h"，可能因为生成的代码没有使用相对路径而报错
* 记得运行 update_libraries_windows.bat 哦
* syntiant_loop() 函数中不能加入任何的中断操作（例如 delay ）
* 笔者环境下，syntiant_loop() 的死循环单轮执行时间约为 1ms 数量级。

*假设你已经熟悉 Arduino IDE 的相关操作：* 选择开发板对应的串口，且开发板为 Arduino SAMD - Arduino MKRZERO。编译这个项目并烧录即可实现所需的功能。*加入上传成功，那么你就假装自己没有看到任何红色的 Warning*

## 附录

### 查询#wink#状态

[官网教程](https://docs.edgeimpulse.com/docs/edge-impulse-cli/cli-installation)

如果希望查询当前 Predictions 的状态，可以使用 edge-impulse-cli 提供的工具。

首先安装 :floppy_disk: node-v16.15.1-x64.msi，注意勾选 附加工具(**Additional Node.js tools** (called **Tools for Native Modules** on newer versions))。

安装完成后重启电脑，在终端中输入 {0} 安装 edge-impulse-cli，并使用其提供的工具查询串口。

```Shell
npm install -g edge-impulse-cli --force
edge-impulse-run-impulse
```

根据提示操作即可。
