# -*- encoding: utf-8 -*-
import sys
import os
from client import Client
from PyQt4 import QtGui, QtCore

class CoverLabel(QtGui.QLabel):
  def __init__(self, parent):
    super(CoverLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))

  def set_img(self, img_path='temp/cover'):
    self.setPixmap(QtGui.QPixmap(img_path))

  #def mouseReleaseEvent(self, event):
  #  self.emit(QtCore.SIGNAL("released()"))

class LoveBtn(QtGui.QLabel):
  def __init__(self, parent, love_img, unlove_img, love):
    super(LoveBtn, self).__init__(parent)
    self.__love_img = QtGui.QPixmap(love_img)
    self.__unlove_img = QtGui.QPixmap(unlove_img)
    self.setFixedSize(QtCore.QSize(40, 40))
    self.set_img(love)

  def mouseReleaseEvent(self, event):
    if self.__love:
      self.setPixmap(self.__unlove_img)
    else:
      self.setPixmap(self.__love_img)
    self.__love = False if self.__love else True
    self.emit(QtCore.SIGNAL("released()"))

  def set_img(self, love):
    self.__love = True if love == 'l' else False
    if self.__love:
      self.setPixmap(self.__love_img)
    else:
      self.setPixmap(self.__unlove_img)

class ImageBtn(QtGui.QLabel):
  def __init__(self, parent, img):
    super(ImageBtn, self).__init__(parent)
    self.__img = QtGui.QPixmap(img)
    self.setPixmap(self.__img)
    self.setFixedSize(QtCore.QSize(40, 40))

  def mouseReleaseEvent(self, event):
    self.emit(QtCore.SIGNAL("released()"))
    
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
    print "pause"
    self.__player.pause()

  def __set_cover(self):
    cover_url = self.__player.status('cover_url')
    self.__player.download(cover_url, "temp/cover")
    self.__cover_bg.set_img("temp/cover")

  def __init_UI(self):
    self.setWindowTitle('Jing.FM')
    self.setFixedSize(QtCore.QSize(300, 300))
    self.__cover_bg = CoverLabel(self)
    self.__set_cover()
    self.__cover_bg.move(0, 0)

    self.__love_btn = LoveBtn(self, 'data/love.png', 'data/unlove.png', self.__player.status('love'))
    self.__next_btn = ImageBtn(self, 'data/next.png')
    self.__love_btn.move(100, 240)
    self.__next_btn.move(160, 240)

    '''
    self.__set_cover()
    self.__pause_btn = CoverBtn(self)

    btn_layout_top = QtGui.QHBoxLayout()
    btn_layout_top.addWidget(self.__love_btn)
    btn_layout_top.addWidget(self.__next_btn)

    whole_layout = QtGui.QVBoxLayout(self)
    whole_layout.addWidget(self.__pause_btn)
    whole_layout.addLayout(btn_layout_top)

    self.setLayout(whole_layout)

    self.connect(self.__love_btn, QtCore.SIGNAL('released()'), self.love)
    self.connect(self.__next_btn, QtCore.SIGNAL('released()'), self.next)
    self.connect(self.__pause_btn, QtCore.SIGNAL('released()'), self.pause)
    '''


def main():
  app = QtGui.QApplication(sys.argv)
  qclient = QClient()
  qclient.show()
  app.exec_()

if __name__ == "__main__":
  main()
