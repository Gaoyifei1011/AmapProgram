
# <p align="center">AmapProgram</p>
<p align="center">使用高德地图Web API制作的小程序</p>


# 关于（About）

**AmapProgram**项目是一个基于高德地图Web API实现的一个可视化的小程序。前端使用Python PyQt5框架实现，后台基于高德地图的Web API。已经在Windows 10平台上良好运行。<br>

这个项目是为了完成我的毕业设计所用的。且由于我是一个初学者，Python学习的深度并没有那么深厚，所以代码中可能存在一些混乱，命名规则没有遵守工程化，请大家多多包涵。<br>

# 介绍（Introduce）

## 程序使用

### 程序打开方式
目前提供了已经编译好的预览版的直接运行文件，当然你也可以自己克隆代码使用Python运行
1.使用release里面已经打包好的的AmapProgram.exe点击打开
2.使用python运行源代码里面的main.py

### 程序主界面 
运行这个主程序后需要进行登录（未来设计是会进行链接数据库的，但是由于时间的问题，没有进行数据库的开发），以及构建的时候没有添加注册用户的模块，所以复制完文件后默认使用root用户进行登录，进入到主界面。<br>
<div align=center><img src="https://github.com/Gaoyifei1011/AmapProgram/blob/main/ScreenShots/LoginMainWindow.png"/></div>
<p align="center">登录界面窗口显示</p><br>

<div align=center><img src="https://github.com/Gaoyifei1011/AmapProgram/blob/main/ScreenShots/MainWindow.png"/></div>
<p align="center">主界面窗口显示</p>

### 程序开发运行环境

开发环境
Windows 10 Build 21382(Dev Channel)
Jetbarins Pycharm 2021.1 + Python3.9

第三方库
源代码运行程序前必须要安装Python的第三方库依赖(安装第三方库建议使用国内的镜像源，用以加快速度)<br>
pip install apscheduler<br>
pip install inspect<br>
pip install requests<br>
pip install urllib.request<br>
pip install pillow<br>
pip install PyQt5<br>
pip install numpy<br>
pip install pandas<br> 
pip install matplotlib<br>
pip install xlrd<br>
pip install xlwt<br>
pip install xlutils<br>
pip install loguru<br>
pip install pathlib<br>
pip install pyqtchart<br>
这些第三方库是我目前已经了解到的必须会使用到的第三方库，可能有一部分库没有使用到，建议根据运行程序出现错误的原因网上搜索对应的第三方库的安装，就可以顺利运行了。<br>

# 注意（Attention）

1.由于在构建应用之初没有对应用的登录进行一个良好的设计，需要将Release中的AmapAccount压缩包里面的Account文件夹复制到%localAppdata%目录下。<br>
2.导入后用户名和密码都是root就可以进入主界面了。<br>
3.由于在构建项目中仅仅对一部分内容进行了日志记录和异常处理，所以可能在运行过程中会发生闪退现象。我本人要进行考研的复习，这个问题有时间以后在进行处理吧。<br>
