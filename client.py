# -*- encoding: utf-8 -*-
import api
import Queue
import mplayer


class Client(object):
  def __init__(self):
    super(Client, self).__init__()
    self.__api = api.API()
    self.__play_list = Queue.Queue()
    self.__player = mplayer.Player()
    self.__cur_track = None
    self.__user = None
    self.__cmbt = None

  def __del__(self):
    self.__player.quit()

  def __update_playlist(self):
    ''' 更新歌曲列表 '''
    if self.__play_list.empty():
      pls_dict = self.__api.fetch_pls(self.__cmbt, self.__user['id'])
      for item in pls_dict['items']:
        self.__play_list.put(item)

  def __update_cur_track(self):
    ''' 更新当前播放歌曲的信息 '''
    self.__cur_track = self.__play_list.get()
    track_url = self.__api.fetch_track(self.__cur_track['mid'])
    self.__cur_track['url'] = track_url
    at_cover, am_cover = self.__api.fetch_cover(self.__cur_track['fid'])
    self.__cur_track['at_cover'] = at_cover
    self.__cur_track['am_cover'] = am_cover
    self.__cur_track.update( self.__api.fetch_track_info(self.__user['id'], self.__cur_track['tid']) )
    self.__cur_track['next_flag'] = False
    self.__cur_track['half_flag'] = False

  def __next(self):
    ''' 下一曲，原始封装 '''
    self.__update_playlist()
    self.__update_cur_track()
    self.play()

  def end_next(self):
    ''' 当前歌曲播放完毕，下一曲 '''
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    total_time = int(self.__cur_track['d'])
    self.__api.post_end(uid, tid, total_time)
    self.__next()

  def heard_song(self):
    ''' 听过该首歌
    播放时长超过总时长一半时触发 '''
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    self.__api.post_heard_song(uid, tid)
    self.__cur_track['half_flag'] = True # 超过一半
  
  def post_time(self, cur_time):
    ''' 传递给服务器
    表明当前歌曲听到哪了 '''
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    self.__cur_track['next_flag'] = True # 超过10秒
    self.__api.post_time(uid, self.__cmbt, tid, cur_time)
    
  def init(self, username, password):
    # login
    login_dict = self.__api.login(username, password)
    if not login_dict:
      return False, u'登陆失败'
    self.__play_list.put(login_dict['pld'])
    self.__user = login_dict['usr']
    self.__cmbt = login_dict['pld']['cmbt']
    # fetch play list
    self.__update_playlist()
    self.__update_cur_track()
    return True, None

  def next_btn(self):
    ''' 点击下一曲按钮
    和播放完毕不同，点击下一曲会告知服务器，可能会影响你的喜爱榜
    '''
    self.__next()
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    next_flag = self.__cur_track['next_flag']
    half_flag = self.__cur_track['half_flag']
    return self.__api.post_next(uid, tid, next_flag, half_flag)

  def love_btn(self):
    ''' 是否喜欢当前播放的这首歌，可多次点击
    在不喜欢的状态点就变成“喜欢”
    在喜欢的状态点就变成“不喜欢”
    '''
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    cmbt = self.__cmbt
    return self.__api.post_love_song(uid, tid, cmbt)

  def hate_btn(self):
    ''' 是否讨厌当前播放的这首歌　'''
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    cmbt = self.__cmbt
    self.__next()
    return self.__api.post_hate_song(uid, tid, cmbt)

  def skip(self, time_gap=5):
    self.__player.time_pos += time_gap

  def pause(self):
    self.__player.pause()
    
  def play(self):
    url = self.__cur_track['url']
    singer = self.__cur_track['cmps_info']['singer']
    name = self.__cur_track['n']
    self.__player.loadfile(url)
    #ct = int(self.__cur_track.get('ct', 0))
    #self.__player.time_pos = ct

  def volume(self, vol):
    self.__player.volume = vol

  def download(self, url, path):
    ''' 封装一个下载的功能 '''
    self.__api.download(url, path)
    

  def status(self, key):
    # 当前时刻
    if key == 'ct':
      try:
        return int(self.__player.time_pos)
      except TypeError:
        return 0
    # 当前歌曲的总时长
    elif key == 'd':
      try:
        return int(self.__cur_track['d'])
      except TypeError:
        return 0
    # 歌曲名
    elif key == 'n':
      return self.__cur_track['n']
    # 歌手
    elif key == 'singer':
      return self.__cur_track['singer']
    # 用户输入的"keyword"
    elif key == 'cmbt':
      return self.__cmbt
    # 封面url
    elif key == 'cover_url':
      return self.__cur_track['am_cover']
    # 当前音量
    elif key == 'vol':
      return self.__player.volume
    # 是否喜欢
    elif key == "love":
      return self.__cur_track['lvd']

