# -*- encoding: utf-8 -*-
'''
Jing.FM的API,应该对应的是1.0版本
所有的API均是网页版的API.
'''
import net, json


class API(object):
  # 登录
  LOGIN_URL = 'http://jing.fm/api/v1/sessions/create'
  # 获取歌曲信息
  FETCH_TRACK_INFO_URL = 'http://jing.fm/api/v1/music/fetch_track_infos'
  # 获取歌曲URL
  FETCH_TRACK_URL = 'http://jing.fm/api/v1/media/song/surl'
  # 获取播放列表
  FETCH_PLS_URL = 'http://jing.fm/api/v1/search/jing/fetch_pls'
  # 获取封面
  FETCH_COVER_URL = 'http://img.jing.fm/album'
  # 喜欢
  POST_LOVE_URL = 'http://jing.fm/api/v1/music/post_love_song'
  # 讨厌
  POST_HATE_URL = 'http://jing.fm/api/v1/music/post_hate_song'
  # POST当前听了多久
  POST_TIME_URL = 'http://jing.fm/api/v1/click/playdata/post'
  # POST歌曲结束
  POST_END_URL = 'http://jing.fm/api/v1/click/playduration/post'
  # POST主动下一首
  POST_NEXT_URL = 'http://jing.fm/api/v1/music/post_next'
  # POST已经收听了该歌曲(超过一半的时间)
  POST_HEARD_URL = 'http://jing.fm/api/v1/music/post_heard_song'


  def __init__(self):
    self.__version = 1.0
    self.__net = net.Net()


  @staticmethod
  def __success(result):
    '''
    分析网站返回的json
    @ return: 如果数据正常返回result内容
    @ return: 如果数据不正常返回False
    @ return: 如果json解析错误、传入的参数不对返回None
    '''
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
    else:
      return success


  def __make_header(self, info):
    '''
    因为Jing.FM每次POST数据都需要在header中包含token信息，所以制作一个header
    @ info: 登录成功后的header信息
    '''
    self.__header_dict = {
      "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
      "Host" : "jing.fm",
      "Jing-A-Token-Header" : info['jing-a-token-header'],
      "Jing-R-Token-Header" : info['jing-r-token-header'],
      "Origin" : "http://jing.fm",
      "Referer" : "http://jing.fm/",
      "X-Requested-With" : "XMLHttpRequest",
    }


  def login(self, email, password):
    '''
    登录。并制作好header
    @ return: 成功: 返回登录后的信息
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "email" : email,
      "pwd" : password,
      }
    info, result = self.__net.request(self.__class__.LOGIN_URL, "POST", param_dict)
    result = self.__success(result)
    if result and info:
      self.__make_header(info)
    return result


  def fetch_pls(self, cmbt, uid):
    '''
    获取歌曲列表。
    @ cmbt: 当前听的关键词或者领域
    @ user_id: 用户id
    @ return: 成功: 返回歌曲列表
    @ return: 失败: 返回None或空列表[]
    '''
    param_dict = {
      "q" : cmbt,
      "ps" : '5',
      "st" : '0',
      "u" : uid,
      "tid" : "0",
      "mt" : "",
      "ss" : "true",
      }
    _, result = self.__net.request(self.__class__.FETCH_PLS_URL, "POST", param_dict, self.__header_dict)
    result = self.__success(result)
    pls = result.get('items', None)
    return pls


  def fetch_track(self, mid):
    '''
    获取歌曲URL.
    @ mid: 标记存储信息的id
    @ return: 成功: 返回歌曲URL
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "mid" : mid,
      "type" : "NO",
      "isp" : "CC",
    }
    _, result = self.__net.request(self.__class__.FETCH_TRACK_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def fetch_track_info(self, uid, tid):
    '''
    获取歌曲信息.
    @ uid: 用户id
    @ tid: 歌曲id
    @ return: 成功: 返回歌曲信息
    @ return: 失败: 返回None或False
    '''
    param_dict= {
      "uid" : uid,
      "tid" : tid,
    }
    _, result = self.__net.request(self.__class__.FETCH_TRACK_INFO_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def post_time(self, uid, cmbt, tid, ct):
    '''
    发送时间. Jing.FM需要隔一段时间发送一次时间信息. 
    应该是他们内部用户改善产品的数据.
    @ uid: 用户id
    @ cmbt: 听歌的关键词
    @ tid: 歌曲id
    @ ct: 听了多久了(s)
    @ return: 成功: 返回True
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "cmbt" : cmbt,
      "tid" : tid,
      'ct' : ct,
    }
    _, result = self.__net.request(self.__class__.POST_TIME_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def post_heard(self, uid, tid):
    '''
    发送"朕已阅"信息. Jing.FM需要在听歌超过一定时间发送一次听过的信息.
    @ uid: 用户id
    @ tid: 歌曲id
    @ return: 成功: 返回True
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "tid" : tid,
    }
    _, result = self.__net.request(self.__class__.POST_HEARD_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def post_end(self, uid, tid, d):
    '''
    发送歌曲结束信息.
    @ uid: 用户id
    @ tid: 歌曲id
    @ d: 歌曲总时长
    @ return: 成功: 返回True
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "d" : d,
    }
    _, result = self.__net.request(self.__class__.POST_END_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def fetch_cover(self, cover_file):
    '''
    获取封面.
    @ cover_file: 封面信息
    @ 返回: 大小2个封面的URL
    '''
    if len(cover_file) != 17:
      return None
    AT_url = "%s/AT/%s/%s/%s/%s/AT%s" % (
      self.__class__.FETCH_COVER_URL,
      cover_file[:4],
      cover_file[4:8],
      cover_file[8:10],
      cover_file[10:12],
      cover_file,
    )
    AM_url = "%s/AM/%s/%s/%s/%s/AM%s" % (
      self.__class__.FETCH_COVER_URL,
      cover_file[:4],
      cover_file[4:8],
      cover_file[8:10],
      cover_file[10:12],
      cover_file
    )
    return AT_url, AM_url


  def post_next(self, uid, tid, next_flag, half_flag):
    '''
    下一曲.
    @ uid: 用户id
    @ tid: 歌曲id
    @ next_flag: 听歌是否超过10秒
    @ half_flag: 听歌是否超过一半时常
    @ return: 成功: 返回True
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "next" : next_flag,
      "half" : half_flag,
    }
    _, result = self.__net.request(self.__class__.POST_NEXT_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def post_love(self, uid, tid, cmbt):
    '''
    喜欢该首歌
    @ uid: 用户id
    @ tid: 歌曲id
    @ cmbt: 听歌的关键词
    @ return: 成功: 返回一个没有意义的dict
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "c" : '1',
      "cmbt" : cmbt,
    }
    _, result = self.__net.request(self.__class__.POST_LOVE_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)


  def post_hate(self, uid, tid, cmbt):
    '''
    讨厌这首歌.
    @ uid: 用户id
    @ tid: 歌曲id
    @ cmbt: 听歌的关键词
    @ return: 成功: 返回一个没有意义的dict
    @ return: 失败: 返回None或False
    '''
    param_dict = {
      "uid" : uid,
      "tid" : tid,
      "c" : '1',
      "cmbt" : cmbt,
    }
    _, result = self.__net.request(self.__class__.POST_HATE_URL, "POST", param_dict, self.__header_dict)
    return self.__success(result)
  
  def download(self, url, filepath):
    '''
    因为API封装了网络请求, 所以封装一个下载的操作.
    @ url: 下载的URL
    @ filepath: 保存的位置
    '''
    _, result = self.__net.request(url, "GET")
    fsave = open(filepath, "wb")
    fsave.write(result)
    fsave.close()


if __name__ == "__main__":
  c = API()
  # login
  #print "login:",
  login_data = c.login("resonx@gmail.com", "411100")
  #print login_data

  '''
  cmbt = login_data['pld']['cmbt']
  uid = login_data['usr']['id']
  tid = login_data['pld']['tid']
  mid = login_data['pld']['mid']
  cover_file = login_data['pld']['fid']
  d = login_data['pld']['d']

  print "fetch_pls",
  print c.fetch_pls(cmbt, uid)

  print "fetch_track_info",
  print c.fetch_track_info(uid, tid)

  print "fetch_cover",
  print c.fetch_cover(cover_file)

  print "fetch_track",
  print c.fetch_track(mid)

  print "post_love",
  print c.post_love(uid, tid, cmbt)

  print "post_hate",
  print c.post_hate(uid, tid, cmbt)

  print "post_time",
  print c.post_time(uid, cmbt, tid, 10)

  print "post_heard",
  print c.post_heard(uid, tid)

  print "post_end",
  print c.post_end(uid, tid, d)

  print "post_next",
  print c.post_next(uid, tid, True, True)
  '''
