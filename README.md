# 代码使用说明

 1. 基本功能
 2. 运行方法
 3. 代码目录结构说明
 4. 常见问题说明

## 一、基本功能
项目基本分为游戏界面前端、手势识别后端两个部分。
### 手势识别后端
功能是通过Mediapipe库对摄像头画面中的手部及姿态进行捕捉，返回33个坐标点的数据，对数据处理后通过训练SVM分类实现手部姿态的识别，并实时通过键盘事件发送到前端界面中，实现对游戏的实时控制。
### 游戏界面前端
音乐节奏小游戏，用户需在音符落下时尽快作出响应的手部动作才可被判定正确。提供了自定义音乐、背景图像、难度、音符速度等功能扩展性较强。另附一个写谱代码，用户可以选择自己喜欢的音乐，自行编写谱面实现最大的自定义程度；且在编写谱面时可以使用键盘操作，最大程度减少延迟，提高谱面和音乐的匹配性。

## 二、运行方法
### 需要安装的库（Python版本3.9.0）
```
absl-py==2.1.0
attrs==24.2.0
cffi==1.17.1
contourpy==1.3.0
cycler==0.12.1
flatbuffers==24.3.25
fonttools==4.54.1
importlib_metadata==8.5.0
importlib_resources==6.4.5
jax==0.4.30
jaxlib==0.4.30
joblib==1.4.2
kiwisolver==1.4.7
matplotlib==3.9.2
mediapipe==0.10.18
ml_dtypes==0.5.0
MouseInfo==0.1.3
numpy==2.0.2
opencv-contrib-python==4.10.0.84
opt_einsum==3.4.0
packaging==24.2
pandas==2.2.3
pillow==11.0.0
protobuf==4.25.5
PyAutoGUI==0.9.54
pycparser==2.22
pygame==2.6.1
PyGetWindow==0.0.9
PyMsgBox==1.0.9
pynput==1.7.7
pyparsing==3.2.0
pyperclip==1.9.0
PyRect==0.2.0
PyScreeze==1.0.1
python-dateutil==2.9.0.post0
pytweening==1.2.0
pytz==2024.2
scikit-learn==1.5.2
scipy==1.13.1
sentencepiece==0.2.0
six==1.16.0
sounddevice==0.5.1
threadpoolctl==3.5.0
tzdata==2024.2
zipp==3.20.2
```
requirments.txt已放在项目目录中，直接运行

```
pip install -r requirements.txt
```
即可完成依赖库的安装。
### 直接运行

项目中预先提供了训练图像数据、处理后数据、模型文件、音乐、前端需要的图片、谱面数据，可以直接游玩。

方法：

 1.  准备：默认的训练图像是用一个摄像头在桌面上方拍摄的，所以需要准备一个摄像头并置于桌面上方50cm左右处，以完成手势的采集。例如：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ddd8c14181db4349b65077f9abab3dcb.jpeg)
将摄像头摆放至合适的位置，将`Gesture_recognition`文件中第54行和`Capture_image`文件中第59行`cam = cv2.VideoCapture(0)`中的参数修改为摄像头对应的序号（如果电脑有多个摄像头），否则保持默认0即可。
（我用的是Iriun Webcam方案，将手机与电脑连在同一局域网下，手机可以当作电脑摄像头使用，图像更清晰，位置也更灵活。）

 2. 运行代码
PyCharm右上角运行配置选到“run”后，点击运行即可。
![](https://i-blog.csdnimg.cn/direct/a2564d8d93fb4b98ae098f25f5a89cf4.png)
### 自定义运行
如果不满足复现训练环境时的条件，可以从零开始，采集训练图像、处理数据、训练自己的模型。
先将项目目录中，`Gesture_train`,`DataFrames`,`model`三个文件夹内容清空。

将运行配置切换为当前文件。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f5bc548ec9c44f94a3fa81b94dde5b22.png)
#### 手势识别后端
运行`Gesture_recognition.py`进行图像采集，用于机器学习模型训练。
根据代码输出的文字提示，按键盘操作，完成`剪刀、石头、布`三种手势的录制（也可以自定义其他手势，代码中作相应修改即可）。采集过程中尽量多活动、翻转一下手腕，保证采集到全方位、多角度的姿态图像。

运行`Process_image.py`：处理图像，利用mediapipe获取手势21个关键点数据。

运行`Process_points.py`：处理21个关键点数据，包括转化为dataframe、none值处理、数据归一化（标准化）、手势翻转。

运行`Train_model.py`：训练模型。

运行`Gesture_recognition`：检验手势识别效果。

#### 游戏前端
##### （可选）自己写谱
可以将`/gamedata`中的音乐换成自己喜欢的音乐，同时修改`Write.py`与`Play.py`中对应行的文件名称。运行`Write.py`，在音乐合适的时机按下键盘上的DFJK四个键之一，对应实际游玩中的手势操作（DK对应“布”，FJ对应“剪刀”）。不要出现同一时刻按下三个及以上按键的操作。**写谱完成直接点击窗口右上角关闭，不要点击Pycharm中的停止运行**。生成的谱面文件存储在项目目录中的`data3.cir`中，将此文件剪切到`/gamedata`中即完成写谱操作。

##### 运行游戏
将运行配置切换到“run”后直接运行。

默认模式下的音符流速可以在`Play.py`中第48行`fixspeed=`处修改。等号后面的数越大，音符流速越慢。

## 三、代码目录结构说明
`/Gesture_train`:存储采集的图像
`/DataFrames`:存储图像处理中及完成后形成的训练数据
`/model`:存储模型文件
`/font`:存储中文字体
`/gamedata`:存储音乐文件和谱面数据文件
`/image`:存储游戏绘制中需要的图片
自定义的背景图像可以放在`/image/bg`中。
其余`.py`文件功能已在运行说明中给出。

## 四、常见问题说明
### 录制手势/进行游戏时按键盘无反应：
需将输入法改至**英语（美国）**。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e7a32cd0b53043598aa665512eced108.png)
### 无法打开摄像头/摄像头画面无图像：
检查`cam = cv2.VideoCapture(0)`中的参数是否与要使用的摄像头编号一致。



