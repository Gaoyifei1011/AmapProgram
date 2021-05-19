<div align=center><img alt="AmapProgram Logo" src="https://github.com/Gaoyifei1011/AmapProgram/blob/main/Resources/Icon/RoutePlanningLogo.png"/></div>

# <p align="center">AmapProgram</p>
<p align="center">使用高德地图Web API制作的小程序</p>

## 关于（About）

**AmapProgram**项目是一个基于高德地图Web API实现的一个可视化的小程序。前端使用Python PyQt5框架实现，后台基于高德地图的Web API。已经在Windows 10平台上良好运行。<br>

这个项目是为了完成我的毕业设计所用的。且由于我是一个初学者，Python学习的深度并没有那么深厚，所以代码中可能存在一些混乱，命名规则没有遵守工程化，请大家多多包涵。

## 介绍（Introduce）

### 程序使用（Program USES）

#### 程序打开方式（Program Opening Ways）
目前提供了已经编译好的预览版的直接运行文件，当然你也可以自己克隆代码使用Python运行<br>
1.下载并运行[Release](https://github.com/Gaoyifei1011/AmapProgram/releases)目录里面已经打包好的的AmapProgram.exe。<br>
2.使用python运行源代码里面的main.py，需要自己在[高德开放平台](https://lbs.amap.com/)和[百度地图开放平台](https://lbsyun.baidu.com/)申请自己所需要的Key,找到代码中的APIKey属性和sk属性对应的值进行替换，具体申请步骤请自行查询。<br>
在AmapProgram目录下打开cmd或powershell，输入以下内容（确保电脑已经安装Python3和必备的第三方库）：
```bash
python main.py
```

#### 程序主界面（Program Main Interface）
运行这个主程序后需要进行登录（未来设计是会进行链接数据库的，但是由于时间的问题，没有进行数据库的开发），以及构建的时候没有添加注册用户的模块，所以复制完文件后默认使用root用户进行登录，进入到主界面。<br>
<div align=center><img alt="LoginMainWindow" src="https://github.com/Gaoyifei1011/AmapProgram/blob/main/ScreenShots/LoginMainWindow.png"/></div>
<p align="center">登录界面窗口显示</p><br>

<div align=center><img alt="MainWindow" src="https://github.com/Gaoyifei1011/AmapProgram/blob/main/ScreenShots/MainWindow.png"/></div>
<p align="center">主界面窗口显示</p>

### 程序开发运行环境（Program Development and Runtime Environment）

#### 开发环境（Development Environment）
Windows 10 Build 21382(Dev Channel)<br>
Jetbarins Pycharm 2021.1 + Python3.9

#### 第三方库（Third-party Libraries）
源代码运行程序前必须要安装Python的第三方库依赖(安装第三方库建议使用国内的镜像源，用以加快速度)<br>
```bash
pip install apscheduler
pip install inspect
pip install loguru
pip install matplotlib
pip install numpy
pip install pandas
pip install pathlib
pip install pillow
pip install PyQt5
pip install pyqtchart
pip install requests
pip install urllib.request
pip install xlrd
pip install xlutils
pip install xlwt
```
这些第三方库是我目前已经了解到的必须会使用到的第三方库，可能有一部分库没有使用到，建议根据运行程序出现错误的原因网上搜索对应的第三方库的安装，就可以顺利运行了。

#### 其他说明（Other Instructions）

1.应用所有数据来源均来自高德地图。<br>
2.原来的开发进度是使用高德地图的API来实现所有功能的，但是由于高德地图关于实时路况的API没有开放。所以暂时使用百度地图的实时路况的API数据来实现这一功能。

## 参考及引用（Reference & Quotation）
1.开发参考：[高德地图Web API文档](https://lbs.amap.com/api/webservice/summary/)，[百度地图Web API文档](https://lbsyun.baidu.com/index.php?title=webapi)。<br>
2.图片库参考：Windows Fluent UI Photo Library、小爱同学、高德地图。

## 注意（Attention）

1.由于在构建应用之初没有对应用的登录进行一个良好的设计，需要将Release中的AmapAccount压缩包里面的Account文件夹复制到%localAppdata%目录下。<br>
2.导入后用户名和密码都是root就可以进入主界面了。<br>
3.由于在构建项目中仅仅对一部分内容进行了日志记录和异常处理，所以可能在运行过程中会发生闪退现象。<br>
4.我本人要进行考研的复习，这个问题有时间以后在进行处理吧，如果发现任何Bug，请在Github仓库中创建一个新的[Issue](https://github.com/Gaoyifei1011/AmapProgram/issues)，我会尽可能使用我的闲余时间进行回答的。<br>
5.未来有时间会再制作一个英文的Readme.md的。<br>
6.本项目目前仅用于学习和交流使用，如果涉及到商业用途发生一切问题，本人不承担任何责任，如果涉及到侵权的内容，请尽快联系我本人，我会尽快删除。<br>
7.有喜欢这个项目的其他童鞋欢迎点击一下star，感谢你们的支持与认可。<br>
