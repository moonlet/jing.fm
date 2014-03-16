# -*- encoding: utf-8 -*-
'''
服务端.
通过Listener获取客户端传来的命令, 并对应操作与反馈操作结果.
'''

from multiprocessing.connection import Listener
from exception import JingCritical as JC
from exception import JingError as JE
from exception import JingWarning as JW
from exception import JingInfo as JI
import player
import config
import urllib2
import os, fcntl, errno


class Server():
  def __init__(self):
    '''
    初始化. 需判断是否当前已经启动了一个进程.
    '''
    # 进程锁文件
    self.__f_lock = os.open(
        config.lockfile,
        os.O_CREAT|os.O_RDWR,
        0660
    )
    has_instance = self.lock()
    if has_instance:
      raise JC(u"已经有一个实例了")

    # 封装好的播放器
    self.__player = player.Player()
    # 监听
    self.__listener = Listener(
        (config.hostname, config.port),
        authkey=config.authkey
    )

    # 根据命令来确定操作
    self.__C2O_dict = {
      'login': self.cmd_login, # 登录
      'info': self.cmd_info, # 歌曲信息
      'next': self.cmd_next, # 下一曲
      'love': self.cmd_love, # 喜欢, 点红心
      'hate': self.cmd_hate, # 不喜欢, 点垃圾桶
      'cmbt': self.cmd_cmbt, # 关键词切换
      'exit': self.cmd_exit, # 退出
    }
    JI(u"开启成功")


  def __del__(self):
    try:
      if self.__player:
        self.__player.__del__()
    except AttributeError: # 存在变量不存在的情况
      pass

    try:
      if self.__listener:
        self.__listener.close()
    except AttributeError: # 存在变量不存在的情况
      pass

    try:
      if self.__f_lock:
        os.close(self.__f_lock)
    except AttributeError: # 存在变量不存在的情况
      pass


  def lock(self):
    '''
    通过fcntl判断文件是否保护中, 借此判断进程是否已经开启了一个.
    '''
    try:
      fcntl.lockf(self.__f_lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
    except IOError as e:
      if e.errno in (errno.EACCES, errno.EAGAIN):
        # 已经有一个进程了
        return True
      else:
        raise e
    # 没有进程
    return False


  def cmd_unknown(self, params):
    '''
    所有的未知命令都进入这个函数
    '''
    raise JI(u"未知命令")


  def cmd_login(self, params):
    email = params[0]
    password = params[1]
    self.__player.login(email, password)
    self.__player.fetch_all()
    self.__player.play()
    raise JI(u"登录成功")


  def cmd_info(self, params):
    self.__player.print_info()


  def cmd_next(self, params):
    self.__player.next()


  def cmd_love(self, params):
    self.__player.love()


  def cmd_hate(self, params):
    self.__player.hate()


  def cmd_cmbt(self, params):
    if len(params) < 1:
      raise JW(u"关键词格式不对: cmbt 关键词")
    self.__player.update_cmbt(params[0])


  def cmd_help(self, params):
    self.__player.help()


  def cmd_exit(self, params):
    raise JC("EXIT")


  def anay_cmd(self, raw_cmd):
    '''
    分析传来的命令.
    因为传递来的数据是文本信息, 所以需要在此处重新分析一次.
    @ raw_cmd: 传递来的原始命令文本.
    '''
    cmd_list = raw_cmd.split('\t')
    cmd = cmd_list[0] # 第一个字段
    param_list = []
    if len(cmd_list) > 1: # 其余字段
      param_list = cmd_list[1:]
    return cmd, param_list


  def make_msg(self, msg, token):
    '''
    用来将Exception中的信息作为反馈传递给用户
    @ msg: 文本信息.
    @ token: 用来区分不同类型的反馈的token.
    '''
    msg_list = msg.split("\n")
    msg_list = [ "%s %s" % (token, x) for x in msg_list ]
    msg_ret = "\n".join(msg_list)
    return msg_ret


  def listen(self):
    '''
    监听与操作.
    '''
    # 建立一个连接
    conn = self.__listener.accept()
    # 等待信息
    recv_cmd = conn.recv()
    # 分析命令
    cmd, params = self.anay_cmd(recv_cmd)
    # 命令->操作
    operation = self.__C2O_dict.get(cmd, self.cmd_unknown)
    # 传递给客户端的反馈信息
    send_info = None
    # 是否继续
    is_continue = True
    try:
      operation(params)
    except JI as e:
      send_info = self.make_msg(e.msg, ">")
    except JW as e:
      send_info = self.make_msg(e.msg, "#")
    except JE as e:
      send_info = self.make_msg(e.msg, "!")
    except JC as e:
      # 出现critical错误, 不再继续
      send_info = self.make_msg(e.msg, "!!")
      is_continue = False
    except KeyError as e:
      # 对应内部的dict中找不到信息
      msg = u'KEY_ERROR'
      JE(msg, e)
      send_info = self.make_msg(msg, '!')
    except ValueError as e:
      # 对应内部的类型转换错误, 如果出现一般为脏数据
      msg = u'VALUE_ERROR'
      JE(msg, e)
      send_info = self.make_msg(msg, '!')
    except urllib2.HTTPError as e:
      # 对应net封装里面的HTTP错误
      msg = u'HTTP_ERROR'
      JE(msg, e)
      send_info = self.make_msg(msg, '!')
    except urllib2.URLError as e:
      # 对应net封装里面的URL错误
      msg = u'URL_ERROR'
      JE(msg, e)
      send_info = self.make_msg(msg, '!')


    if send_info:
      # 传递的是\u1234这样的编码值
      send_info = repr(send_info)
      conn.send_bytes(send_info)
    conn.close()
    return is_continue


  def run(self):
    '''
    主循环
    '''
    while 1:
      is_continue = self.listen()
      if not is_continue:
        break

    self.__del__()


if __name__ == "__main__":
  import sys
  try:
    pid = os.fork()
    if pid > 0: # father
      sys.exit(0)
  except OSError:
    sys.exit(1)

  try:
    server = Server()
  except JC:
    sys.exit(0)
  else:
    server.run()
