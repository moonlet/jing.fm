# -*- encoding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import time

class CoverLabel(QtGui.QLabel):
  ''' 封面按钮 '''
  def __init__(self, parent):
    super(CoverLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))
    #self.__parent = parent

  def set_img(self, img_path='temp/cover'):
    self.setPixmap(QtGui.QPixmap(img_path))

class LoveBtn(QtGui.QLabel):
  ''' 是否喜爱的按钮 '''
  def __init__(self, parent, love_img, normal_img,
               love_hover_img, normal_hover_img, love):
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
  ''' 自定义图标的按钮 '''
  def __init__(self, parent, size_tuple, normal_img, hover_img):
    super(ImageBtn, self).__init__(parent)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__hover_img = QtGui.QPixmap(hover_img)
    self.setPixmap(self.__normal_img)
    self.setFixedSize(QtCore.QSize(size_tuple[0], size_tuple[1]))

  def mouseReleaseEvent(self, event):
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.setPixmap(self.__hover_img)
    
  def leaveEvent(self, event):
    self.setPixmap(self.__normal_img)

class ToggleBtn(QtGui.QLabel):
  ''' 存在2个状态的按钮 '''
  def __init__(self, parent, size_tuple, enable_img, disable_img, enable=True):
    super(ToggleBtn, self).__init__(parent)
    self.__enable_img = QtGui.QPixmap(enable_img)
    self.__disable_img = QtGui.QPixmap(disable_img)
    self.setFixedSize(QtCore.QSize(size_tuple[0], size_tuple[1]))
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
    if self.__enable:
      self.setPixmap(QtGui.QPixmap(None))


class ProcessBar(QtGui.QWidget):
  ''' 进度条 '''
  def __init__(self, parent):
    super(ProcessBar, self).__init__(parent)
    self.__width = 300
    self.__rate = 0.0
    self.setMinimumSize(300, 2)
    self.connect(self, QtCore.SIGNAL("update_rate(float)"), self.set_rate)
    self.__normal_color = QtGui.QColor(0x33,0x33,0x33)
    self.__played_color = QtGui.QColor(0x99,0x99,0x99)

  def paintEvent(self, e):
    qp = QtGui.QPainter()
    qp.begin(self)
    self.__draw_bg(qp)
    qp.end()

  def __draw_bg(self, qp):
    mid = int(self.__width * self.__rate)
    qp.setPen(self.__played_color)
    qp.drawRect(0, 0, mid, 1)
    qp.setPen(self.__normal_color)
    qp.drawRect(mid, 0, self.__width, 1)

  def set_rate(self, rate):
    self.__rate = rate
    self.repaint()

   
class QTimer(QtCore.QTimer):
  ''' 增加了暂停功能的定时器，单位ms '''
  def __init__(self, interval):
    super(QTimer, self).__init__()
    self.__interval = interval
    self.__timer = QtCore.QTimer()
    QtCore.QObject.connect(
      self.__timer,
      QtCore.SIGNAL("timeout()"),
      self.__on_timer
    )
    self.init()
  
  def init(self):
    self.__start_time = time.time() # ms
    self.__remnant_time = 0 # ms

  # 用来处理不足1秒的暂停
  def __on_timer(self):
    self.__timer.stop()
    self.emit(QtCore.SIGNAL("timeout()"))
    self.start(self.__interval)

  def pause(self):
    if self.isActive():
      self.stop()
      self.__remnant_time = 1000 - (( time.time() - self.__start_time ) % 1000)
    else:
      if self.__remnant_time:
        self.__timer.start(self.__remnant_time)
      else:
        self.start(self.__interval)

class NameLabel(QtGui.QLabel):
  def __init__(self, parent):
    super(NameLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(200, 30))
    #self.setAlignment(QtCore.Qt.AlignCenter)
    #self.setStyleSheet('QLabel{border-width:1px;border-style:solid;}')
    #self.setPixmap(QtGui.QPixmap('data/love_love.png'))

class NameLabel(QtGui.QLabel):
  def __init__(self, parent):
    super(NameLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))
    self.setPixmap(QtGui.QPixmap('temp/cover.png'))

class LoveBtn(QtGui.QLabel):
  ''' 是否喜爱的按钮 '''
  def __init__(self, parent, love_img, normal_img,
               love_hover_img, normal_hover_img, love):
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
  ''' 自定义图标的按钮 '''
  def __init__(self, parent, size_tuple, normal_img, hover_img):
    super(ImageBtn, self).__init__(parent)
    self.__normal_img = QtGui.QPixmap(normal_img)
    self.__hover_img = QtGui.QPixmap(hover_img)
    self.setPixmap(self.__normal_img)
    self.setFixedSize(QtCore.QSize(size_tuple[0], size_tuple[1]))

  def mouseReleaseEvent(self, event):
    self.emit(QtCore.SIGNAL("released()"))

  def enterEvent(self, event):
    self.setPixmap(self.__hover_img)
    
  def leaveEvent(self, event):
    self.setPixmap(self.__normal_img)

class ToggleBtn(QtGui.QLabel):
  ''' 存在2个状态的按钮 '''
  def __init__(self, parent, size_tuple, enable_img, disable_img, enable=True):
    super(ToggleBtn, self).__init__(parent)
    self.__enable_img = QtGui.QPixmap(enable_img)
    self.__disable_img = QtGui.QPixmap(disable_img)
    self.setFixedSize(QtCore.QSize(size_tuple[0], size_tuple[1]))
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
    if self.__enable:
      self.setPixmap(QtGui.QPixmap(None))


class ProcessBar(QtGui.QWidget):
  ''' 进度条 '''
  def __init__(self, parent):
    super(ProcessBar, self).__init__(parent)
    self.__width = 300
    self.__rate = 0.0
    self.setMinimumSize(300, 2)
    self.connect(self, QtCore.SIGNAL("update_rate(float)"), self.set_rate)
    self.__normal_color = QtGui.QColor(0x33,0x33,0x33)
    self.__played_color = QtGui.QColor(0x99,0x99,0x99)

  def paintEvent(self, e):
    qp = QtGui.QPainter()
    qp.begin(self)
    self.__draw_bg(qp)
    qp.end()

  def __draw_bg(self, qp):
    mid = int(self.__width * self.__rate)
    qp.setPen(self.__played_color)
    qp.drawRect(0, 0, mid, 1)
    qp.setPen(self.__normal_color)
    qp.drawRect(mid, 0, self.__width, 1)

  def set_rate(self, rate):
    self.__rate = rate
    self.repaint()

   
class QTimer(QtCore.QTimer):
  ''' 增加了暂停功能的定时器，单位ms '''
  def __init__(self, interval):
    super(QTimer, self).__init__()
    self.__interval = interval
    self.__timer = QtCore.QTimer()
    QtCore.QObject.connect(
      self.__timer,
      QtCore.SIGNAL("timeout()"),
      self.__on_timer
    )
    self.init()
  
  def init(self):
    self.__start_time = time.time() # ms
    self.__remnant_time = 0 # ms

  # 用来处理不足1秒的暂停
  def __on_timer(self):
    self.__timer.stop()
    self.emit(QtCore.SIGNAL("timeout()"))
    self.start(self.__interval)

  def pause(self):
    if self.isActive():
      self.stop()
      self.__remnant_time = 1000 - (( time.time() - self.__start_time ) % 1000)
    else:
      if self.__remnant_time:
        self.__timer.start(self.__remnant_time)
      else:
        self.start(self.__interval)

class NameLabel(QtGui.QWidget):
  def __init__(self, parent):
    super(NameLabel, self).__init__(parent)
    self.setFixedSize(QtCore.QSize(300, 300))
    self.__bg_label = QtGui.QLabel(self)
    self.__text_label = QtGui.QLabel(self)
    self.__text_label.setAlignment(QtCore.Qt.AlignTop)
    pa = QtGui.QPalette()
    pa.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0xFFFFFF))
    self.__text_label.setPalette(pa)
    self.__text_label.setGeometry(100, 100, 200, 100)
    self.__text_label.setWordWrap(True)
    self.__text_label.adjustSize()

  def set_bg(self, img):
    self.__bg_label.setPixmap(QtGui.QPixmap(img))

  def set_text(self, text):
    self.__text_label.setText(text)

  

class EditLine(QtGui.QLineEdit):
  def __init__(self, parent, size):
    super(EditLine, self).__init__(parent)
    self.setAlignment(QtCore.Qt.AlignCenter)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.__normal_style = '''QLineEdit{
      width: %dpx;
      height: %dpx;
      border-width: 1px;
      border-style: solid;
      border-color: #FF0000;
    }''' % (size[0], size[1])
    self.setStyleSheet(self.__normal_style)
    '''
      background-image: url(%s);
      background-repeat: no-repeat;
      background-position: center left;
    '''
 
if __name__ == '__main__':
  import sys
  class QClient(QtGui.QWidget):
    def __init__(self):
      super(QClient, self).__init__()
      self.setFixedSize(QtCore.QSize(300, 300))
      m = CoverLabel(self)
      m.set_img()
      k = NameLabel(self)
      k.set_bg('data/pause.png')
      k.set_text('wocao0000000000000000000000000000000000000000000000000000000000000000000000000000000')

  app = QtGui.QApplication(sys.argv)
  q = QClient()
  q.show()
  app.exec_()
