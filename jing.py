# -*- encoding: utf-8 -*-
import sys
from client import Client
from PyQt4 import QtGui, QtCore, Qt
from widget import *


class QClient(QtGui.QWidget):
  def __init__(self):
    super(QClient, self).__init__()
    self.__timer = QTimer(1000)
    QtCore.QObject.connect(self.__timer, QtCore.SIGNAL("timeout()"), self.__on_timer)
    self.__init_player('resonx@gmail.com', '411100')
    self.__init_UI()

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

  def __init_player(self, username, password):
    self.__player = Client()
    self.__player.init(username, password)
    self.__play()
  
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

  def __init_UI(self):
    self.setWindowTitle('Jing.FM')
    self.setFixedSize(QtCore.QSize(300, 400))
    # 无边框
    self.setWindowFlags(Qt.Qt.FramelessWindowHint)
    # 窗口可移动
    self.setMouseTracking(True)

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
      'data/hate_normal.png',
      'data/hate_hover.png',
    )
    self.__next_btn = ImageBtn(
      self,
      'data/next_normal.png',
      'data/next_hover.png'
    )
    self.__pause_btn = ToggleBtn(
      self,
      'data/play.png',
      'data/pause.png',
    )
    self.__exit_btn = QtGui.PushButton(self)
    self.__name_label = QtGui.QLabel(self)
    self.__process_bar = ProcessBar(self)

    self.__love_btn.move(10, 350)
    self.__hate_btn.move(60, 350)
    self.__next_btn.move(110, 350)
    self.__pause_btn.move(90, 90)
    self.__name_label.move(0, 315)
    self.__process_bar.setGeometry(0, 300, 300, 2)
    self.__cover_bg.move(0, 0)

    self.connect(self.__love_btn, QtCore.SIGNAL('released()'), self.love)
    self.connect(self.__hate_btn, QtCore.SIGNAL('released()'), self.hate)
    self.connect(self.__next_btn, QtCore.SIGNAL('released()'), self.next)
    self.connect(self.__pause_btn, QtCore.SIGNAL('released()'), self.pause)
    self.connect(self.__exit_btn, QtCOre.SIGNAL('clicked()'), self.exit)
  
    self.__set_cover()

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


def main():
  app = QtGui.QApplication(sys.argv)
  qclient = QClient()
  qclient.show()
  app.exec_()

if __name__ == "__main__":
  main()
