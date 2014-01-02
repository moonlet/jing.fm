# -*- encoding: utf-8 -*-
from client import Client
from PyQt4 import QtGui, QtCore, Qt
from widget import *

class QBaseWidget(QtGui.QWidget):
  ''' 添加了关闭窗口按钮的基类 '''
  def __init__(self):
    super(QBaseWidget, self).__init__()
    self.__init_UI()

  def __init_UI(self):
    self.setFixedSize(QtCore.QSize(300, 400))
    self.__exit_btn = ImageBtn(
      self,
      (30, 30),
      None,
      'data/exit.png',
    )
    self.__exit_btn.move(263, 5)
    self.connect(
      self.__exit_btn,
      QtCore.SIGNAL('released()'),
      QtCore.QCoreApplication.instance().quit
    )

  def raise_exit(self):
    self.__exit_btn.raise_()

class QLoginWidget(QBaseWidget):
  ''' 登录窗口 '''
  def __init__(self):
    super(QLoginWidget, self).__init__()
    self.__init_UI()
    
  def __init_UI(self):
    # username edit line
    self.__username_qle = QtGui.QLineEdit(self)
    self.__username_qle.setGeometry(90, 60, 160, 30)
    self.connect(
      self.__username_qle,
      QtCore.SIGNAL('returnPressed()'),
      self.__submit
    )
    self.__username_qle.setFocus()
    # username img
    self.__username_img = QtGui.QLabel(self)
    self.__username_img.setPixmap(QtGui.QPixmap('data/user.png'))
    self.__username_img.move(50, 60)
    # password edit line
    self.__password_qle = QtGui.QLineEdit(self)
    self.__password_qle.setEchoMode(QtGui.QLineEdit.Password)
    self.__password_qle.setGeometry(90, 100, 160, 30)
    self.connect(
      self.__password_qle,
      QtCore.SIGNAL('returnPressed()'),
      self.__submit
    )
    # password img
    self.__password_img = QtGui.QLabel(self)
    self.__password_img.setPixmap(QtGui.QPixmap('data/password.png'))
    self.__password_img.move(50, 100)
    # tips
    self.tips = QtGui.QLabel(self)
    self.tips.setGeometry(50, 10, 200, 30)
    self.tips.setAlignment(QtCore.Qt.AlignCenter)
    # 命令

  
  def __submit(self):
    self.__username = self.__username_qle.text()
    self.__password = self.__password_qle.text()
    if self.__username == '':
      self.tips.setText(u'用户名不能为空')
    elif self.__password == '':
      self.tips.setText(u'密码不能为空')
    else:
      self.emit(
        QtCore.SIGNAL("login(PyQt_PyObject, PyQt_PyObject)"),
        self.__username,
        self.__password
      )
    

class QPlayerWidget(QBaseWidget):
  ''' 播放器 '''
  def __init__(self, player):
    super(QPlayerWidget, self).__init__()
    self.__cover_path = 'temp/cover'
    # 用于进度条的定时器
    self.__timer = QTimer(1000)
    QtCore.QObject.connect(
      self.__timer,
      QtCore.SIGNAL("timeout()"),
      self.__on_timer
    )
    # 从QClient中传入的player
    self.__player = player

  def __del__(self):
    self.__timer.stop()
    QtGui.qApp.quit()

  # 初始化函数
  def init(self):
    self.__play()
    self.__init_UI()

  # 下一曲的基础操作
  def __base_next(self):
    self.__total_time = self.__player.status('d')
    self.__mid_time = self.__total_time / 2
    self.__timer.start(1000)
    # 设置封面
    self.__set_cover()
    # 设置桃心按钮的图标
    self.__love_btn.set_img(self.__player.status('love'))
    
  # 歌曲播放结束，跳转下一曲
  def __end_next(self):
    self.__timer.stop()
    self.__player.end_next()
    self.__base_next()

  # 定时器任务函数
  def __on_timer(self):
    cur_time = self.__player.status('ct')
    if cur_time >= self.__total_time:
      # 当前歌曲播放完毕下一曲
      self.__end_next()
    elif 0 <= cur_time == self.__mid_time:
      # 超过一半的时间，发送"heard_song"信息
      self.__player.heard_song()
    if cur_time % 30 == 0:
      # 定时发送, 时间间隔为30秒
      self.__player.post_time(cur_time)
    # 播放比例，用于进度条
    rate = float(cur_time) / float(self.__total_time)
    self.__process_bar.emit(QtCore.SIGNAL("update_rate(float)"), rate)

  def __play(self):
    self.__timer.stop()
    self.__total_time = self.__player.status('d')
    self.__mid_time = self.__total_time / 2
    self.__player.play()
    self.__timer.start(1000)

  def __next(self):
    self.__timer.stop()
    self.__player.next_btn()
    self.__base_next()

  def __hate(self):
    self.__timer.stop()
    self.__player.hate_btn()
    self.__base_next()

  def __love(self):
    self.__player.love_btn()

  def __pause(self):
    self.__player.pause()
    self.__timer.pause()

  def __set_cover(self):
    cover_url = self.__player.status('cover_url')
    self.__player.download(cover_url, self.__cover_path)
    self.__cover_bg.set_img(self.__cover_path)
    self.__name_label.setText(self.__player.status('n'))
    self.__name_label.setAlignment(QtCore.Qt.AlignCenter)
    self.__name_label.resize(300, 20)

  def __init_UI(self):
    self.setFixedSize(QtCore.QSize(300, 400))
    # 歌名标签
    self.__name_label = QtGui.QLabel(self)
    #self.__name_label.move(0, 320)
    self.__name_label.setGeometry(0, 320, 300, 20)
    # 进度条
    self.__process_bar = ProcessBar(self)
    self.__process_bar.setGeometry(0, 300, 300, 2)
    # 封面
    self.__cover_bg = CoverLabel(self)
    self.__cover_bg.move(0, 0)
    self.__set_cover()
    # 桃心按钮
    self.__love_btn = LoveBtn(
      self,
      'data/love_love.png',
      'data/love_normal.png',
      'data/love_love_hover.png',
      'data/love_normal_hover.png',
      self.__player.status('love')
    )
    self.__love_btn.move(10, 350)
    self.connect(self.__love_btn, QtCore.SIGNAL('released()'), self.__love)
    # 垃圾桶按钮
    self.__hate_btn = ImageBtn(
      self,
      (40, 40),
      'data/hate_normal.png',
      'data/hate_hover.png',
    )
    self.__hate_btn.move(60, 350)
    self.connect(self.__hate_btn, QtCore.SIGNAL('released()'), self.__hate)
    # 下一曲按钮
    self.__next_btn = ImageBtn(
      self,
      (40, 40),
      'data/next_normal.png',
      'data/next_hover.png'
    )
    self.__next_btn.move(110, 350)
    self.connect(self.__next_btn, QtCore.SIGNAL('released()'), self.__next)
    # 暂停按钮
    self.__pause_btn = ToggleBtn(
      self,
      (120, 120),
      'data/play.png',
      'data/pause.png',
    )
    self.__pause_btn.move(90, 90)
    self.connect(self.__pause_btn, QtCore.SIGNAL('released()'), self.__pause)
    # 将父类中的exit按钮提到最高层显示
    super(QPlayerWidget, self).raise_exit()


class QClient(QtGui.QWidget):
  ''' 整体的一个客户端
  调用QLoginWidget作为登录时用
  调用QPlayWidget作为播放时用 '''
  def __init__(self):
    super(QClient, self).__init__()
    # 播放器
    self.__player = Client()
    self.__player_widget = QPlayerWidget(self.__player)
    self.__login_widget = QLoginWidget()
    self.__main_layout = QtGui.QHBoxLayout(self)
    # layout的边界设为0
    self.__main_layout.setContentsMargins(0,0,0,0)
    self.setLayout(self.__main_layout)
    self.__init_UI()
    self.__login_show()

  def __init_UI(self):
    self.setWindowTitle('Jing.FM')
    #self.setWindowFlags(Qt.Qt.FramelessWindowHint) # 无边框
    self.setWindowFlags(Qt.Qt.SplashScreen) # 无边框,比FramelessWindowHint好
    self.setMouseTracking(True) # 窗口可移动
    self.setFixedSize(QtCore.QSize(300, 400))
    screen = QtGui.QDesktopWidget().screenGeometry()
    size = self.geometry()
    self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

  # 展示login widget
  def __login_show(self):
    self.__main_layout.addWidget(self.__login_widget)
    self.connect(
      self.__login_widget,
      QtCore.SIGNAL('login(PyQt_PyObject, PyQt_PyObject)'),
      self.__init_player
    )

  # 展示player widget
  def __player_show(self):
    self.__main_layout.removeWidget(self.__login_widget)
    self.__main_layout.addWidget(self.__player_widget)

  # 判断登录成功与否
  def __init_player(self, username, password):
    success, ret_text = self.__player.init(username, password)
    if success:
      # 成功
      self.__player_show()
      self.__player_widget.init()
    else:
      # 失败
      self.__login_widget.tips.setText(ret_text)
    
  #鼠标点击事件
  def mousePressEvent(self,event):
    if event.button() == QtCore.Qt.LeftButton:
      self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
      event.accept()
  
  #鼠标移动事件
  def mouseMoveEvent(self,event):
    if event.buttons() ==QtCore.Qt.LeftButton:
      self.move(event.globalPos() - self.dragPosition)
      event.accept() 
  


def main():
  import sys
  app = QtGui.QApplication(sys.argv)
  q = QClient()
  q.show()
  app.exec_()

if __name__ == "__main__":
  main()
