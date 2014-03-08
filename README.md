jing.fm
=======

Jing.FM powered by python, mplayer, mplayer.py

去除掉pyqt的GUI界面, 直接用命令行更Geek. 其实是我实在做不好界面.

# 1. 安装 #

## 1.1. 安装MPLAYER ##

如果你已经安装了mplayer那么可以跳过这个步骤, 如果没有请按照下述方法安装

1. 下载源码: [网页](http://www.mplayerhq.hu/design7/dload.html), [1.1.1release](http://www.mplayerhq.hu/MPlayer/releases/MPlayer-1.1.1.tar.xz)
2. 解压压缩包: `tar -xvf MPlayer-1.1.1.tar.xz`
3. 安装alsa依赖库: `sudo apt-get install libasound2-dev`
4. 编译安装: `./configure --enable-alsa --disable-ossaudio --yasm=''`
5. 安装好后会在MPlayer的源文件目录下生成一个mplayer的二进制文件, 可以直接使用
6. 将mplayer文件放到指定位置(例如: /bin/), 如果你想放在自己习惯的位置请并修改环境变量

> wget http://www.mplayerhq.hu/MPlayer/releases/MPlayer-1.1.1.tar.xz
> tar -xvf MPlayer-1.1.1.tar.xz
> ./configure --enable-alsa --disable-ossaudio --yasm=''
> sudo cp mplayer ~/bin/

保证安装完成后能够使用mplayer播放m4a的音乐就OK了!

## 2.2. 安装mplayer.py ##

mplayer.py是一款mplayer的python封装.

1. 下载源码: [网页](https://github.com/baudm/mplayer.py), [Git](git@github.com:baudm/mplayer.py.git)
2. 安装: `sudo python setup.py install`

> git clone git@github.com:baudm/mplayer.py.git
> cd mplayer.py
> sudo python setup.py install

# 2. 使用 #

## 2.1. 使用方法 ##

使用方法很简单, 应该都能无障碍地使用:
1. 运行jingFM.py. `python jingFM.py`或`./jingFM.py`都可以.
2. 输入邮箱, 密码 (输错了就帮不了你了), 没有的可以去官网申请[Jing.FM](http://jing.fm).
3. 显示登录成功后输入`help`, 里面就有使用帮助. 如果有各种情况导致不能正确显示请看下面的命令列表 (其实就是抄了一份).

## 2.2. 命令列表 ##

由于是使用命令行来操作, 所以必须提供一些操作命令:

1. info: 显示当前播放歌曲的信息
2. cmbt: 关键词. 更换关键词, 例如: cmbt 刘德华
3. next: 下一曲
4. love: 桃心标记当前曲目
5. hate: 当前歌曲扔垃圾桶
6. help: 显示帮助内容
7. exit: 退出, 因为程序包含多个线程, 所以CTRL+C效果不会好哦!


# N. 帮助 #

如果还是有问题, 请联系我:

1. 邮箱: xiaorx@live.com
2. 也可以wiki留言.

# N+1. 最后 #

由于我实在是不会做GUI, 有个gui的分支, 有兴趣的可以接着开发, 我用pyqt开发了一个界面了, 但是在展示关键词那块做得怎么都很丑, 直接怒删了. 如果你开发出了美观大方的界面请务必告诉我. 谢谢 :-)
