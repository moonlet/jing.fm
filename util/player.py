# -*- encoding: utf-8 -*-
'''
封装的jing.fm的播放器.
实现了:
  1. 下一曲
  2. 自动下一曲 (轮询的方法, 使用threading.Timer作为定时器)
  3. 喜欢, 不喜欢
  4. 关键词切换

'''

from exception import JingCritical as JC
from exception import JingError as JE
from exception import JingWarning as JW
from exception import JingInfo as JI
from threading import Timer
import api, mplayer


class Player(object):
  def __init__(self):
    super(Player, self).__init__()
    self.__api = api.API()
    self.__playlist = []
    self.__mplayer = mplayer.Player()
    self.__usr = None
    self.__cmbt = None
    # 定时器, 用来轮询歌曲是否播放完毕
    self.__timer = None


  def __del__(self):
    # 取消定时器
    if self.__timer:
      self.__timer.cancel()
    # 关闭mplayer
    if self.__mplayer:
      self.__mplayer.quit()


  def __on_time(self):
    '''
    定时器函数. 轮询歌曲是否完毕的函数, 没1s轮询一次
    同时还需要进行POST_TIME, POST_HEARD等操作
    '''
    ct = self.__mplayer.time_pos
    if ct == None: # 歌曲结束
      self.end()
    else:
      d = int(self.__playlist[0]['d']) # 总时间
      ct = int(ct) # 当前播放时间

      if ct > d/2: # half_flag的标记条件
        self.__playlist[0]['half_flag'] = True
      elif ct > 10: # next_flag的标记条件
        self.__playlist[0]['next_flag'] = True

      # 每20秒POST_TIME一次
      if ct % 20 == 0:
        uid = self.__usr['id']
        tid = self.__playlist[0]['tid']
        self.__api.post_time(uid, self.__cmbt, tid, ct)

      self.__timer = Timer(1, self.__on_time)
      self.__timer.start()


  def login(self, email, password):
    '''
    登录. 同时将数据保存
    '''
    if not email or not password:
      raise JW(u"请输入完整的邮箱和密码")

    login_ret = self.__api.login(email, password)
    if not login_ret:
      raise JW(u"登录不成功, 请确认账号密码正确")

    self.__usr = login_ret['usr']
    self.__playlist.append(login_ret['pld'])
    self.__cmbt = login_ret['pld']['cmbt']


  def fetch_all(self):
    '''
    一次性获取playlist, track, trackinfo
    '''
    # 获取所有参数信息
    uid = self.__usr['id']
    mid = self.__playlist[0]['mid']
    tid = self.__playlist[0]['tid']

    # 更新播放列表
    if len(self.__playlist) <= 1:
      pls_ret = self.__api.fetch_pls(self.__cmbt, uid)
      if not pls_ret:
        raise JE(u"获取播放列表失败")

      self.__playlist.extend(pls_ret)

    # 更新歌曲URL
    url = self.__api.fetch_track(mid)
    if not url:
      raise JC(u"获取歌曲URL失败")
    self.__playlist[0]['url'] = url

    # 更新歌曲信息
    info = self.__api.fetch_track_info(uid, tid)
    if not info:
      raise JE(u"获取歌曲信息失败")
    self.__playlist[0]['info'] = info


  def love(self):
    uid = self.__usr['id']
    tid = self.__playlist[0]['tid']

    love_ret = self.__api.post_love(uid, tid, self.__cmbt)
    self.__playlist[0]['info']['lvd'] = 'l'
    if not love_ret:
      raise JW(u"桃心没点亮")


  def hate(self):
    uid = self.__usr['id']
    tid = self.__playlist[0]['tid']

    hate_ret = self.__api.post_hate(uid, tid, self.__cmbt)
    if not hate_ret:
      raise JW(u"没讨厌成功")
    self.__next()


  def print_info(self):
    '''
    打印当前播放歌曲的信息
    '''
    singer = self.__playlist[0]['info']['cmps_info']['singer']
    n = self.__playlist[0]['n']
    loved = self.__playlist[0]['info']['lvd']

    loved = u'真爱' if loved == 'l' else u'母鸡'
    raise JI(
        u"关键词: %s\n歌  手: %s\n歌  名: %s\n爱不爱: %s" % (
            self.__cmbt,
            singer,
            n,
            loved
        )
    )


  def play(self):
    '''
    播放
    '''
    try:
      url = self.__playlist[0]['url']
    except KeyError as e:
      raise JC(u"没有歌曲URL", e)

    self.__mplayer.loadfile(url)
    # 开启本次的timer, 第一次的时间间隔为5秒
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
    uid = self.__usr['id']
    tid = self.__playlist[0]['tid']
    d = self.__playlist[0]['d']

    self.__api.post_end(uid, tid, d)
    self.__next()


  def next(self):
    '''
    人肉点击"下一曲"
    '''
    uid = self.__usr['id']
    tid = self.__playlist[0]['tid']
    # 听歌超过10秒为True
    next_flag = self.__playlist[0].get('next_flag', False)
    # 听歌超过时长一半为True
    half_flag = self.__playlist[0].get('half_flag', False)

    self.__api.post_next(uid, tid, next_flag, half_flag)
    self.__next()


  def update_cmbt(self, cmbt):
    '''
    更新关键词
    @ cmbt: 新的关键词
    '''
    uid = self.__usr['id']
    tid = self.__playlist[0]['tid']
    cmbt = cmbt.decode("utf-8")
    pls = self.__api.fetch_pls(cmbt, uid)
    if not pls:
      raise JI(u"这个关键词找不到啊")
    else: # 成功则更换
      self.__playlist = [ self.__playlist[0] ]
      self.__playlist.extend(pls)
      self.__cmbt = cmbt
      self.__next()


if __name__ == '__main__':
  p = Player()
  p.login('your-email', 'your-password')
  p.fetch_all()
  p.play()
