# -*- encoding: utf-8 -*-
import sys
from client import Client
from PyQt4 import QtGui, QtCore, Qt
from widget import *

class QLoginWidget(QtGui.QWidget):
  def __init__(self):
    super(QLoginWidget, self).__init__()
    self.__init_UI()
    
  def __init_UI(self):
    self.setFixedSize(QtCore.QSize(300, 200))
    self.__exit_btn = ImageBtn(
      self,
      (32, 32),
      'data/exit.png',
      'data/exit.png',
    )
    self.__exit_btn.move(263, 5)
    self.connect(self.__exit_btn, QtCore.SIGNAL('released()'), QtCore.QCoreApplication.instance().quit)


    self.__username_qle = QtGui.QLineEdit(self)
    self.__password_qle = QtGui.QLineEdit(self)
    self.__password_qle.setEchoMode(QtGui.QLineEdit.Password)
    self.__username_img = QtGui.QLabel(self)
    self.__username_img.setPixmap(QtGui.QPixmap('data/user.png'))
    self.__password_img = QtGui.QLabel(self)
    self.__password_img.setPixmap(QtGui.QPixmap('data/password.png'))
    '''
    self.__submit_btn = ImageBtn(
      self,
      (32, 32),
      'data/enter.png',
      None,
    )
    self.__submit_btn.setFocusPolicy(QtCore.Qt.StrongFocus)
    '''
    self.tips = QtGui.QLabel(self)
    
    self.__username_qle.setGeometry(90, 60, 160, 30)
    self.__password_qle.setGeometry(90, 100, 160, 30)
    self.__username_img.move(50, 60)
    self.__password_img.move(50, 100)
    #self.__submit_btn.move(218, 190)
    self.tips.setGeometry(50, 10, 200, 30)
    self.tips.setAlignment(QtCore.Qt.AlignCenter)
    self.connect(self.__password_qle, QtCore.SIGNAL('returnPressed()'), self.__submit)
    self.connect(self.__username_qle, QtCore.SIGNAL('returnPressed()'), self.__submit)

  
  def __submit(self):
    self.__username = self.__username_qle.text()
    self.__password = self.__password_qle.text()
    if self.__username == '':
      self.tips.setText(u'用户名不能为空')
    elif self.__password == '':
      self.tips.setText(u'密码不能为空')
    else:
      self.emit(QtCore.SIGNAL("login(PyQt_PyObject, PyQt_PyObject)"), self.__username, self.__password)
    
    

class QClient(QtGui.QWidget):
  def __init__(self):
    super(QClient, self).__init__()
    self.__player = Client()
    self.__play_widget = QPlayWidget(self.__player)
    self.__login_widget = QLoginWidget()
    self.__main_layout = QtGui.QHBoxLayout(self)
    self.__main_layout.setContentsMargins(0,0,0,0)
    self.setLayout(self.__main_layout)
    self.__init_UI()
    self.__login_show()

  def __init_UI(self):
    self.setWindowTitle('Jing.FM')
    self.setFixedSize(QtCore.QSize(300, 200))
    # 无边框
    self.setWindowFlags(Qt.Qt.FramelessWindowHint)
    # 窗口可移动
    self.setMouseTracking(True)

  def __login_show(self):
    self.__main_layout.addWidget(self.__login_widget)
    self.connect(self.__login_widget, QtCore.SIGNAL('login(PyQt_PyObject, PyQt_PyObject)'), self.__init_player)

  def __play_show(self):
    self.__main_layout.removeWidget(self.__login_widget)
    self.__main_layout.addWidget(self.__play_widget)

  def __init_player(self, username, password):
    if self.__player.init(username, password):
      self.setFixedSize(QtCore.QSize(300, 400))
      self.__play_show()
      self.__play_widget.init()
    else:
      self.__login_widget.tips.setText(u'帐号密码不正确')
    
  def mousePressEvent(self,event):
    #鼠标点击事件
    if event.button() == QtCore.Qt.LeftButton:
      self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
      event.accept()
  
  def mouseMoveEvent(self,event):
    #鼠标移动事件
    if event.buttons() ==QtCore.Qt.LeftButton:
      self.move(event.globalPos() - self.dragPosition)
      event.accept() 
  


class QPlayWidget(QtGui.QWidget):
  def __init__(self, player):
    super(QPlayWidget, self).__init__()
    self.__timer = QTimer(1000)
    self.__player = player
    QtCore.QObject.connect(self.__timer, QtCore.SIGNAL("timeout()"), self.__on_timer)

  def init(self):
    self.__play()
    self.init_UI()

  def __del__(self):
    self.__player.exit()
    self.__timer.stop()
    QtGui.qApp.quit()

  def __auto_next(self):
    self.__timer.stop()
    self.__player.end_next()
    self.__cur_time = 0
    self.__timer.start(1000)
    self.__set_cover()
    self.__love_btn.set_img(self.__player.status('love'))

  def __on_timer(self):
    total_time = int(self.__player.status('d'))
    self.__cur_time += 1
    mid_time = total_time / 2
    if self.__cur_time >= total_time:
      self.__auto_next()
    elif 0 <= self.__cur_time == mid_time:
      self.__player.heard_song()
    if self.__cur_time % 30 == 0:
      self.__player.post_time(self.__cur_time)
    rate = float(self.__cur_time) / float(total_time)
    self.__process_bar.emit(QtCore.SIGNAL("update_rate(float)"), rate)

  
  def __play(self):
    self.__timer.stop()
    self.__player.play()
    self.__cur_time = 0
    self.__timer.start(1000)

  def next(self):
    self.__timer.stop()
    self.__player.next_btn()
    self.__cur_time = 0
    self.__timer.start(1000)
    self.__set_cover()
    self.__love_btn.set_img(self.__player.status('love'))

  def hate(self):
    self.__timer.stop()
    self.__player.hate_btn()
    self.__cur_time = 0
    self.__timer.start(1000)
    self.__set_cover()
    self.__love_btn.set_img(self.__player.status('love'))

  def love(self):
    self.__player.love_btn()

  def pause(self):
    self.__player.pause()
    self.__timer.pause()

  def __set_cover(self):
    cover_url = self.__player.status('cover_url')
    self.__player.download(cover_url, "temp/cover")
    self.__cover_bg.set_img("temp/cover")
    self.__name_label.setText(self.__player.status('n'))
    self.__name_label.setAlignment(QtCore.Qt.AlignCenter)
    self.__name_label.resize(300, 20)

  def init_UI(self):
    self.setFixedSize(QtCore.QSize(300, 400))

    self.__cover_bg = CoverLabel(self)
    self.__love_btn = LoveBtn(
      self,
      'data/love_love.png',
      'data/love_normal.png',
      'data/love_love_hover.png',
      'data/love_normal_hover.png',
      self.__player.status('love')
    )
    self.__hate_btn = ImageBtn(
      self,
      (40, 40),
      'data/hate_normal.png',
      'data/hate_hover.png',
    )
    self.__next_btn = ImageBtn(
      self,
      (40, 40),
      'data/next_normal.png',
      'data/next_hover.png'
    )
    self.__pause_btn = ToggleBtn(
      self,
      'data/play.png',
      'data/pause.png',
    )
    self.__exit_btn = ImageBtn(
      self,
      (32, 32),
      'data/exit.png',
      'data/exit.png',
    )
    self.__name_label = QtGui.QLabel(self)
    self.__process_bar = ProcessBar(self)

    self.__love_btn.move(10, 350)
    self.__hate_btn.move(60, 350)
    self.__next_btn.move(110, 350)
    self.__pause_btn.move(90, 90)
    self.__exit_btn.move(263, 5)
    self.__name_label.move(0, 315)
    self.__process_bar.setGeometry(0, 300, 300, 2)
    self.__cover_bg.move(0, 0)

    self.connect(self.__love_btn, QtCore.SIGNAL('released()'), self.love)
    self.connect(self.__hate_btn, QtCore.SIGNAL('released()'), self.hate)
    self.connect(self.__next_btn, QtCore.SIGNAL('released()'), self.next)
    self.connect(self.__pause_btn, QtCore.SIGNAL('released()'), self.pause)
    self.connect(self.__exit_btn, QtCore.SIGNAL('released()'), QtCore.QCoreApplication.instance().quit)
  
    self.__set_cover()


def main():
  app = QtGui.QApplication(sys.argv)
  q = QClient()
  q.show()
  '''
  qclient = QPlayWidget()
  qclient.init('resonx@gmail.com', '411100')
  qclient.show()
  '''
  app.exec_()

if __name__ == "__main__":
  main()
