# -*- encoding: utf-8 -*-
from threading import Timer
import api
import mplayer
import sys
import getpass
import re


def STDERR(line): sys.stderr.write("%s\n" % (line))
def STDOUT(line): sys.stderr.write("%s\n" % (line))

USAGE = '''\
# 使用帮助:
# 命令分为2部分: 命令对象 [命令参数]. 所有的命令包括:
#   1. info: 显示当前播放歌曲的信息.
#   2. cmbt: 关键词. 更换关键词, 例如: cmbt 刘德华.
#   3. next: 下一曲.
#   4. love: 桃心标记当前曲目.
#   5. hate: 当前歌曲扔垃圾桶.
#   6. help: 显示当前内容.
#   7. exit: 退出, 因为程序包含多个线程, 所以CTRL+C效果不会好哦!.\
'''

class Client(object):
  def __init__(self):
    super(Client, self).__init__()
    self.__api = api.API()
    self.__playlist = []
    self.__player = mplayer.Player()
    self.__usr = None
    self.__cmbt = None
    # 定时器, 用来轮询歌曲是否播放完毕
    self.__timer = Timer(1, self.__on_time)


  def __on_time(self):
    '''
    定时器函数. 轮询歌曲是否完毕的函数, 没1s轮询一次
    同时还需要进行POST_TIME, POST_HEARD等操作
    '''
    ct = self.__player.time_pos
    if ct == None:
      self.end()
    else:
      d = self.__playlist[0]['d'] # 总时间
      ct = int(ct) # 当前播放时间

      if ct > d/2: # half_flag的标记条件
        self.__playlist[0]['half_flag'] = True
      elif ct > 10: # next_flag的标记条件
        self.__playlist[0]['next_flag'] = True
      # 每5秒POST_TIME一次
      if ct % 5 == 0:
        uid = self.__usr['id']
        tid = self.__playlist[0]['tid']
        self.__api.post_time(uid, self.__cmbt, tid, ct)

      self.__timer = Timer(1, self.__on_time)
      self.__timer.start()


  def __del__(self):
    # 关闭mplayer
    self.__player.quit()
    # 取消定时器
    self.__timer.cancel()


  def login(self, email, password):
    '''
    登录. 同时将数据保存
    '''
    if not email or not password:
      raise Exception("请输入完整的邮箱和密码")

    login_ret = self.__api.login(email, password)
    if not login_ret:
      raise Exception("登录不成功, 请确认账号密码正确")

    try:
      self.__usr = login_ret['usr']
      self.__playlist.append(login_ret['pld'])
      self.__cmbt = login_ret['pld']['cmbt']
    except KeyError:
      raise Exception("返回数据格式非法")


  def fetch_all(self):
    '''
    一次性获取playlist, track, trackinfo
    '''
    # 获取所有参数信息
    try:
      uid = self.__usr['id']
      mid = self.__playlist[0]['mid']
      tid = self.__playlist[0]['tid']
    except KeyError:
      raise Exception("返回数据格式非法")

    # 更新播放列表
    if len(self.__playlist) <= 1:
      pls_ret = self.__api.fetch_pls(self.__cmbt, uid)
      if not pls_ret:
        raise Exception("获取播放列表失败")
      self.__playlist.extend(pls_ret)

    # 更新歌曲URL
    url = self.__api.fetch_track(mid)
    if not url:
      raise Exception("获取歌曲URL失败")
    self.__playlist[0]['url'] = url
    self.__playlist[0]['d'] = int(self.__playlist[0]['d'])

    # 更新歌曲信息
    info = self.__api.fetch_track_info(uid, tid)
    if not info:
      raise Exception("获取歌曲信息失败")
    self.__playlist[0]['info'] = info


  def love(self):
    try:
      uid = self.__usr['id']
      tid = self.__playlist[0]['tid']
    except KeyError:
      raise Exception("返回数据格式非法")

    love_ret = self.__api.post_love(uid, tid, self.__cmbt)
    self.__playlist[0]['info']['lvd'] = 'l'
    if not love_ret:
      raise Exception("桃心没点亮")


  def hate(self):
    try:
      uid = self.__usr['id']
      tid = self.__playlist[0]['tid']
    except KeyError:
      raise Exception("返回数据格式非法")

    hate_ret = self.__api.post_hate(uid, tid, self.__cmbt)
    if not hate_ret:
      raise Exception("没讨厌成功")
    self.__next()


  def print_info(self):
    '''
    打印当前播放歌曲的信息
    '''
    try:
      singer = self.__playlist[0]['info']['cmps_info']['singer']
      n = self.__playlist[0]['n']
      loved = self.__playlist[0]['info']['lvd']
    except KeyError:
      raise Exception("返回数据格式非法")
    loved = u'真爱' if loved == 'l' else u'母鸡'
    STDOUT(u"# 关键词: %s" % (self.__cmbt))
    STDOUT(u"# 歌  手: %s" % (singer))
    STDOUT(u"# 歌  名: %s" % (n))
    STDOUT(u"# 爱不爱: %s" % (loved))


  def play(self):
    '''
    播放
    '''
    try:
      url = self.__playlist[0]['url']
    except KeyError:
      raise Exception("返回数据格式非法")

    self.__player.loadfile(url)
    # 开启本次的timer
    self.__timer = Timer(5, self.__on_time)
    self.__timer.start()


  def __next(self):
    '''
    封装的一个下一首函数
    自动下一首和主动下一首有区别
    '''
    del self.__playlist[0]
    self.fetch_all()
    # 取消上一次的timer
    self.__timer.cancel()
    self.play()



  def end(self):
    '''
    自动播放完毕后的下一曲
    '''
    try:
      uid = self.__usr['id']
      tid = self.__playlist[0]['tid']
      d = self.__playlist[0]['d']
    except KeyError:
      raise Exception("返回数据格式非法")

    self.__api.post_end(uid, tid, d)
    self.__next()


  def next(self):
    '''
    人肉点击"下一曲"
    '''
    try:
      uid = self.__usr['id']
      tid = self.__playlist[0]['tid']
      # 听歌超过10秒为True
      next_flag = self.__playlist[0].get('next_flag', False)
      # 听歌超过时长一半为True
      half_flag = self.__playlist[0].get('half_flag', False)
    except KeyError:
      raise Exception("返回数据格式非法")

    self.__api.post_next(uid, tid, next_flag, half_flag)
    self.__next()


  def update_cmbt(self, cmbt):
    try:
      uid = self.__usr['id']
      tid = self.__playlist[0]['tid']
    except KeyError:
      raise Exception("返回数据格式非法")
    cmbt = cmbt.decode("utf-8")
    pls = self.__api.fetch_pls(cmbt, uid)
    if not pls:
      STDERR("这个关键词找不到啊")
    else: # 成功则更换
      self.__playlist = [ self.__playlist[0] ]
      self.__playlist.extend(pls)
      self.__cmbt = cmbt
      self.__next()


  def run(self):
    email = raw_input('> 请输入邮箱: ')
    pwd = getpass.getpass('> 请输入密码: ')
    try:
      self.login(email, pwd)
      STDOUT("> 登录成功! 恭候您的指令")
      self.fetch_all()
      self.play()
      # 接收命令
      self.cmd()
    except Exception as e:
      STDERR("! %s" % (str(e)))
      # 出错必须干掉计时器先
      self.__timer.cancel()

  def cmd(self):
    while 1:
      # 所有的命令都分成2部分, [操控对象] [操控值(部分可选)]
      # 中间用分隔符号(空格, tab)分开
      raw_cmd = raw_input(': ')
      raw_cmd = re.split(r"\s+", raw_cmd)
      if len(raw_cmd) < 1:
        STDERR("> 咱能认真输入命令吗? 计算机也辛苦啊!")
        continue

      cmd = raw_cmd[0]
      val = " ".join(raw_cmd[1:]) if len(raw_cmd) > 1 else None
      if   cmd == 'next':
        self.next()
      elif cmd == 'love':
        self.love()
      elif cmd == 'hate':
        self.hate()
      elif cmd == 'info':
        self.print_info()
      elif cmd == 'cmbt':
        if val == None:
          STDERR("> 关键词格式不对: cmbt 关键词...")
          continue
        self.update_cmbt(val)
      elif cmd == 'help':
        print USAGE
      elif cmd == 'exit':
        STDERR("> 您老就不听了啊?")
        self.__timer.cancel()
        break
      else:
        STDERR("> 未知指令")


if __name__ == '__main__':
  c = Client()
  c.run()
