# Jing.FM #

Jing.FM是一款很好的网络音乐产品. 官方网站为[Jing.FM](http://jing.fm),
有很多别家 "电台产品" 没有的特性, 我不善总结, 有兴趣的可以去官网试试.

本项目是一款Jing.FM的本地播放软件. 没什么特别的, 主要是能够不用开着个浏览器.
而且官方的内容还有个总是缓冲的问题, 貌似我的代码没这个问题.

正所谓站在巨人的肩膀上~~让巨人肩周炎~~, 本代码使用了如下大型工程, 在此鸣谢:

1. mplayer. 因为我写了好久都没写出一个可以播放m4a格式的播放器,
   所以我只好直接拿了mplayer.
2. mplayer.py. 一款mplayer的python封装. 因为我只会用python.
~~3. pyqt. 都说了只会python.~~

另外, 不是我不会做GUI, 其实我是美国苹果公司的一线设计师,
只是我觉得用命令行更加geek罢了.

# 1. 安装 #

## 1.1. 安装MPLAYER ##

如果你已经安装了mplayer那么可以跳过这个步骤, 如果没有请按照下述方法安装

1. 下载源码: [网页](http://www.mplayerhq.hu/design7/dload.html),
   [1.1.1release](http://www.mplayerhq.hu/MPlayer/releases/MPlayer-1.1.1.tar.xz)
2. 解压压缩包: `tar -xvf MPlayer-1.1.1.tar.xz`
3. 安装alsa依赖库: `sudo apt-get install libasound2-dev`
4. 编译安装: `./configure --enable-alsa --disable-ossaudio --yasm=''`
5. 安装好后会在MPlayer的源文件目录下生成一个mplayer的二进制文件, 可以直接使用
6. 将mplayer文件放到指定位置(例如: /bin/), 如果你想放在自己习惯的位置请并修改环境变量

```shell
wget http://www.mplayerhq.hu/MPlayer/releases/MPlayer-1.1.1.tar.xz
tar -xvf MPlayer-1.1.1.tar.xz
./configure --enable-alsa --disable-ossaudio --yasm=''
sudo cp mplayer ~/bin/
```

保证安装完成后能够使用mplayer播放m4a的音乐就OK了!

## 2.2. 安装mplayer.py ##

mplayer.py是一款mplayer的python封装.

1. 下载源码: [网页](https://github.com/baudm/mplayer.py),
   [Git](git@github.com:baudm/mplayer.py.git)
2. 安装: `sudo python setup.py install`

```shell
git clone git@github.com:baudm/mplayer.py.git
cd mplayer.py
sudo python setup.py install
```

# 2. 使用 #

## 2.1. 使用方法 ##

使用方法很简单, 应该都能无障碍地使用:
1. 运行jingFM.py. `python jingFM.py` 或 `./jingFM.py`都可以.
2. 输入邮箱, 密码 (输错了就帮不了你了), 没有的可以去官网申请[Jing.FM](http://jing.fm).
3. 显示登录成功后输入 `help`, 里面就有使用帮助. 如果有各种情况导致不能正确显示请看下面的命令列表
   (其实就是抄了一份).

## 2.2. 命令列表 ##

由于是使用命令行来操作, 所以必须提供一些操作命令:

0. boot: 用来开启服务程序, 如果已经开启了再输入会报错.\n\
1. help: 显示当前内容.\n\
2. cmbt: 关键词. 更换关键词, 例如: cmbt 刘德华.\n\
3. next: 下一曲.\n\
4. love: 桃心标记当前曲目.\n\
5. hate: 当前歌曲扔垃圾桶.\n\
6. info: 显示当前播放歌曲的信息.\n\
7. exit: 退出, 因为程序包含多个线程, 所以 CTRL+C 效果不会好哦!\n\

例如: jingFM.py login your-email your-password.\

# N. 帮助 #

如果还是有问题, 请联系我:

1. 邮箱: xiaorx@live.com
2. 也可以wiki留言.

# N+1. 最后 #

由于我实在是不会做GUI, 有个gui的分支, 有兴趣的可以接着开发,
我已经用pyqt开发了一个播放界面, 但是在展示 "关键词" 那块怎么做都很丑,
所以我直接怒删了, 如果哪位高手做了一个美观大方的界面请务必告诉我! 谢谢! :-)
