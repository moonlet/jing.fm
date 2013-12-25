# -*- encoding: utf-8 -*-
import sys
import os
from client import Client
from PyQt4 import QtGui, QtCore

class CoverLabel(QtGui.QLabel):
  def __init__(self, parent):
    super(CoverLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))
    self.__parent = parent

  def set_img(self, img_path='temp/cover'):
    self.setPixmap(QtGui.QPixmap(img_path))

class LoveBtn(QtGui.QLabel):
  def __init__(self, parent, love_img, normal_img, love_hover_img, normal_hover_img, love):
    super(LoveBtn, self).__init__(parent)
    self.__love_img = QtGui.QPixmap(love_img)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__love_hover_img = QtGui.QPixmap(love_hover_img)
    self.__normal_hover_img = QtGui.QPixmap(normal_hover_img)
    self.setFixedSize(QtCore.QSize(40, 40))
    self.set_img(love)

  def mouseReleaseEvent(self, event):
    if self.__love:
      self.setPixmap(self.__normal_hover_img)
    else:
      self.setPixmap(self.__love_hover_img)
    self.__love = False if self.__love else True
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    if self.__love:
      self.setPixmap(self.__love_hover_img)
    else:
      self.setPixmap(self.__normal_hover_img)

  def leaveEvent(self, event):
    if self.__love:
      self.setPixmap(self.__love_img)
    else:
      self.setPixmap(self.__normal_img)

  def set_img(self, love):
    self.__love = True if love == 'l' else False
    if self.__love:
      self.setPixmap(self.__love_img)
    else:
      self.setPixmap(self.__normal_img)

class ImageBtn(QtGui.QLabel):
  def __init__(self, parent, normal_img, hover_img):
    super(ImageBtn, self).__init__(parent)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__hover_img = QtGui.QPixmap(hover_img)
    self.setPixmap(self.__normal_img)
    self.setFixedSize(QtCore.QSize(40, 40))

  def mouseReleaseEvent(self, event):
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.setPixmap(self.__hover_img)
    
  def leaveEvent(self, event):
    self.setPixmap(self.__normal_img)

class ToggleBtn(QtGui.QLabel):
  def __init__(self, parent, enable_img, disable_img, enable=True):
    super(ToggleBtn, self).__init__(parent)
    self.__enable_img = QtGui.QPixmap(enable_img)
    self.__disable_img = QtGui.QPixmap(disable_img)
    self.setFixedSize(QtCore.QSize(120, 120))
    self.__enable = enable
    
  def __set_img(self):
    if self.__enable:
      self.setPixmap(self.__enable_img)
    else:
      self.setPixmap(self.__disable_img)

  def mouseReleaseEvent(self, event):
    self.__enable = False if self.__enable else True
    self.__set_img() 
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.__set_img()

  def leaveEvent(self, event):
    self.setPixmap(QtGui.QPixmap(None))
    
class QClient(QtGui.QWidget):
  def __init__(self):
    super(QClient, self).__init__()
    self.__init_player('resonx@gmail.com', '411100')
    self.__init_UI()

  def __del__(self):
    self.__player.exit()
    QtGui.qApp.quit()

  def __init_player(self, username, password):
    self.__player = Client()
    self.__player.init(username, password)
    self.__player.play()

  def next(self):
    self.__player.next_btn()
    self.__set_cover()
    self.__love_btn.set_img(self.__player.status('love'))

  def love(self):
    self.__player.love_btn()

  def pause(self):
    self.__player.pause()

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
    self.__cover_bg = CoverLabel(self)
    # 
    self.__love_btn = LoveBtn(
      self,
      'data/love_love.png',
      'data/love_normal.png',
      'data/love_love_hover.png',
      'data/love_normal_hover.png',
      self.__player.status('love')
    )
    self.__trash_btn = ImageBtn(
      self,
      'data/trash_normal.png',
      'data/trash_hover.png',
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
    self.__name_label = QtGui.QLabel(self)

    self.__love_btn.move(10, 350)
    self.__trash_btn.move(60, 350)
    self.__next_btn.move(110, 350)
    self.__pause_btn.move(90, 90)
    self.__name_label.move(0, 315)
    self.__cover_bg.move(0, 0)

    self.connect(self.__love_btn, QtCore.SIGNAL('released()'), self.love)
    self.connect(self.__next_btn, QtCore.SIGNAL('released()'), self.next)
    self.connect(self.__pause_btn, QtCore.SIGNAL('released()'), self.pause)

    self.__set_cover()


def main():
  app = QtGui.QApplication(sys.argv)
  qclient = QClient()
  qclient.show()
  app.exec_()

if __name__ == "__main__":
  main()
