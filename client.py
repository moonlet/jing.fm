# -*- encoding: utf-8 -*-
import api
import Queue
import mplayer
from threading import Timer


class Client(object):
  def __init__(self):
    self.__api = api.API()
    self.__play_list = Queue.Queue()
    self.__cur_track = None
    self.__player = mplayer.Player()
    self.__user = None
    self.__cmbt = None
    self.__timer = None

  def __update_play_list(self):
    if self.__play_list.empty():
      pls_dict = self.__api.fetch_pls(self.__cmbt, self.__user['id'])
      for item in pls_dict['items']:
        self.__play_list.put(item)

  def __update_cur_track(self):
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
    self.__update_play_list()
    self.__update_cur_track()
    self.play()

  def __timer_event(self, cur_time=0):
    total_time = int(self.__cur_track['d'])
    post_time = 30 if cur_time > 30 else 10
    post_time = post_time \
      if post_time + cur_time <= total_time \
      else total_time - cur_time
    mid_time = total_time / 2
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    # 歌曲结束
    if cur_time >= total_time:
      self.__api.post_end(uid, tid, total_time)
      self.__next()
      return
    elif 0 <= cur_time - mid_time < 30:
      self.__api.post_heard_song(uid, tid)
      self.__cur_track['half_flag'] = True # 超过一半
    if cur_time > 0:
      self.__cur_track['next_flag'] = True # 超过10秒
      self.__api.post_time(uid, self.__cmbt, tid, cur_time)
    self.__timer = Timer( post_time, self.__timer_event, (cur_time + post_time,) )
    self.__timer.start()

  def init(self, username, password):
    # login
    login_dict = self.__api.login(username, password)
    self.__play_list.put(login_dict['pld'])
    self.__user = login_dict['usr']
    self.__cmbt = login_dict['pld']['cmbt']
    # fetch play list
    self.__update_play_list()
    self.__update_cur_track()

  def next_btn(self):
    ''' 点击下一曲按钮
    和播放完毕不同，点击下一曲会告知服务器，可能会影响你的喜爱榜
    '''
    self.__next()
    uid = self.__user['id']
    tid = self.__cur_track['tid']
    next_flag = self.__cur_track['next_flag']
    half_flag = self.__cur_track['half_flag']
    self.__timer.cancel()
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

  def skip(self, time_gap=5):
    self.__player.time_pos += time_gap

  def exit(self):
    self.__timer.cancel()
    self.__player.quit()

  def pause(self):
    self.__player.pause()
    
  def play(self):
    url = self.__cur_track['url']
    singer = self.__cur_track['cmps_info']['singer']
    name = self.__cur_track['n']
    ct = int(self.__cur_track.get('ct', 0))
    self.__player.loadfile(url)
    self.__player.time_pos = ct
    self.__timer_event(ct)

  def volume(self, vol):
    self.__player.volume = vol

  def download(self, url, path):
    self.__api.download(url, path)
    

  def status(self, key):
    if key == 'n':
      return self.__cur_track['n']
    elif key == 'singer':
      return self.__cur_track['singer']
    elif key == 'cmbt':
      return self.__cmbt
    elif key == 'cover_url':
      return self.__cur_track['am_cover']
    elif key == 'cover_name':
      return self.__cur_track['fid']
    elif key == 'vol':
      return self.__player.volume
    elif key == "love":
      return self.__cur_track['lvd']


if __name__ == '__main__':
  client = Client()
  client.init('resonx@gmail.com', '411100')
  client.play()
  while 1:
    cmd = raw_input()
    if cmd == "next":
      print client.next_btn()
    elif cmd == "love":
      print client.love_btn()
    elif cmd == "exit":
      client.exit()
      break
    elif cmd == "skip":
      client.skip()
    elif cmd == "vol":
      client.volume(100.0)
