# -*- encoding: utf-8 -*-
import net
import json
import time
import random
import re


class API(object):
  def __init__(self):
    self.__version = 1.0
    self.__net = net.Net()
    self.__login_url = 'http://jing.fm/api/v1/sessions/create'
    self.__track_info_url = 'http://jing.fm/api/v1/music/fetch_track_infos'
    self.__track_url = 'http://jing.fm/api/v1/media/song/surl'
    self.__pls_url = 'http://jing.fm/api/v1/search/jing/fetch_pls'
    self.__love_song_url = 'http://jing.fm/api/v1/music/post_love_song'

    self.__time_post_url = 'http://jing.fm/api/v1/click/playdata/post'
    self.__end_post_url = 'http://jing.fm/api/v1/click/playduration/post'
    self.__next_post_url = 'http://jing.fm/api/v1/music/post_next'
    self.__heard_song_url = 'http://jing.fm/api/v1/music/post_heard_song'
    self.__hate_song_url = 'http://jing.fm/api/v1/music/post_hate_song'

    self.__cover_url = 'http://img.jing.fm/album'

    self.__info = None
    self.__header_dict = None



  @staticmethod
  def __success(result):
    if not result:
      return None
    try:
      result_json = json.loads(result)
    except:
      return None

    success = result_json.get('success', False)
    if success:
      ret = result_json.get('result', True)
      return ret

  def __make_header(self):
    self.__header_dict = {
      "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
      "Host" : "jing.fm",
      "Jing-A-Token-Header" : self.__info['jing-a-token-header'],
      "Jing-R-Token-Header" : self.__info['jing-r-token-header'],
      "Origin" : "http://jing.fm",
      "Referer" : "http://jing.fm/",
      "X-Requested-With" : "XMLHttpRequest",
    }


  def login(self, email, password):
    param_dict = {
      "email" : email,
      "pwd" : password,
      }
    info, result = self.__net.request(self.__login_url, "POST", param_dict)
    result = self.__success(result)
    if result and info:
      self.__info = dict(info)
      self.__make_header()
    return result


  def fetch_pls(self, cmbt, usr_id):
    param_dict = {
      "q" : cmbt,
      "ps" : '5',
      "st" : '0',
      "u" : usr_id,
      "tid" : "0",
      "mt" : "",
      "ss" : "true",
      }
    _, result = self.__net.request(self.__pls_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def fetch_track(self, mid):
    param_dict = {
      "mid" : mid,
      "type" : "NO",
      "isp" : "CC",
    }
    _, result = self.__net.request(self.__track_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def fetch_track_info(self, uid, tid):
    param_dict= {
      "uid" : uid,
      "tid" : tid,
    }
    _, result = self.__net.request(self.__track_info_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def post_time(self, uid, cmbt, tid, ct):
    param_dict = {
      "uid" : uid,
      "cmbt" : cmbt,
      "tid" : tid,
      'ct' : ct,
    }
    _, result = self.__net.request(self.__time_post_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def post_heard_song(self, uid, tid):
    param_dict = {
      "uid" : uid,
      "tid" : tid,
    }
    _, result = self.__net.request(self.__heard_song_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def post_end(self, uid, tid, d):
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "d" : d,
    }
    _, result = self.__net.request(self.__end_post_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def fetch_cover(self, cover_file):
    if len(cover_file) != 17:
      return
    AT_url = "%s/AT/%s/%s/%s/%s/AT%s" % (
      self.__cover_url,
      cover_file[:4],
      cover_file[4:8],
      cover_file[8:10],
      cover_file[10:12],
      cover_file,
    )
    AM_url = "%s/AM/%s/%s/%s/%s/AM%s" % (
      self.__cover_url,
      cover_file[:4],
      cover_file[4:8],
      cover_file[8:10],
      cover_file[10:12],
      cover_file
    )
    return AT_url, AM_url

  def post_next(self, uid, tid, next_flag, half_flag):
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "next" : next_flag,
      "half" : half_flag,
    }
    _, result = self.__net.request(self.__heard_song_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def post_love_song(self, uid, tid, cmbt):
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "c" : '1',
      "cmbt" : cmbt,
    }
    _, result = self.__net.request(self.__love_song_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)

  def post_hate_song(self, uid, tid, cmbt):
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "c" : '1',
      "cmbt" : cmbt,
    }
    _, result = self.__net.request(self.__hate_song_url, "POST", param_dict, self.__header_dict)
    return self.__success(result)
  
  def download(self, url, filepath):
    _, result = self.__net.request(url, "GET")
    fsave = open(filepath, "wb")
    fsave.write(result)
    fsave.close()


if __name__ == "__main__":
  c = API()
  print "login:", 
  login_data = c.login("resonx@gmail.com", "411100")
  print login_data

  cmbt = login_data['pld']['cmbt']
  usr_id = str(login_data['usr']['id'])
  print "cmbt: %s; usr_id: %s" % (cmbt, usr_id)
  print "pls:",
  pls_data = c.fetch_pls(cmbt, usr_id)
  print pls_data

  cover_file = login_data['pld']['fid']
  cover1, cover2 = c.fetch_cover(cover_file)
  print cover1, cover2

  uid = str(login_data['usr']['id'])
  tid = str(login_data['pld']['tid'])
  print "uid %s\ttid %s" % (uid, tid)
  info_data = c.fetch_track_info(uid, tid)
  print "info", info_data


  '''
  print "track:", c.fetch_track()
  print "info:", c.fetch_track_info()
  print "time:", c.time_post(66)
  time.sleep(10)
  print "time:", c.time_post(26)
  time.sleep(10)
  print "time:", c.time_post(36)
  time.sleep(2)
  print "heard:", c.heard_song()
  '''

