from datetime import datetime
#import models
from hashlib import md5
import requests
import json
from math import radians, cos, sin, asin, sqrt
import base64

geo_distace=500
face_score=80



def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    print('0')
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    print(new_md5.hexdigest())
    # 加密
    return new_md5.hexdigest()

def time_diff_now(d):
    if d==null:
        return 10000
    now = datetime.now()
    d1 = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S.%f')
    d2 = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
    delta=d2-d1
    return delta.days*24*60*60+delta.seconds

def data_dif(d1,d2):
    f=datetime.strptime(d1,'%Y-%m-%d')
    l=datetime.strptime(d2,'%Y-%m-%d')
    days=(l-f).days
    return days
def time_dif(d1,d2):
    f=datetime.strptime(d1,'%H:%M')
    try:
        l=datetime.strptime(d2,'%H:%M:%S.%f')
    except:
        l=datetime.strptime(d2,'%H:%M:%S')
    second=(l-f).seconds
    return second

def get_token():
    url='https://aip.baidubce.com/oauth/2.0/token'

    data={"grant_type":"client_credentials", "client_id":"GvHXiXf1VRTSheKox1a1jy7E", "client_secret":"vjfRfVragvhNRNFw206zwdF6tlEq6BqH"}

    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    html = requests.post(url, headers = headers,  data=data)
    if (html.content):
        data=json.loads(html.text)
    return(data['access_token'])


def base64encode(path):
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s

def distance(a,b,c,d):
    print(a)
    print(c)
    lon1, lat1, lon2, lat2 = map(radians, [float(a), float(b), float(c), float(d)])
    print(lon1)
    print(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    d = c * r
    print("距离")
    print(d)
    if d*1000<geo_distace:
        return True
    return False




def face_det(pic1,pic2):
    url='https://aip.baidubce.com/oauth/2.0/token'

    data={"grant_type":"client_credentials", "client_id":"GvHXiXf1VRTSheKox1a1jy7E", "client_secret":"vjfRfVragvhNRNFw206zwdF6tlEq6BqH"}

    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    html = requests.post(url, headers = headers,  data=data)
    if (html.content):
        data=json.loads(html.text)
    access_token=(data['access_token'])
    url='https://aip.baidubce.com/rest/2.0/face/v3/match'
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    params = json.dumps(
        [{"image": base64encode(pic1), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
        {"image": pic2, "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}])
    request_url = url + "?access_token=" + access_token
    respose=requests.post(request_url,data=params,headers=headers)
    data=json.loads(respose.text)
    print('score:')
    print(data['result']['score'])
    if(data['result']['score']):
        if (data['result']['score'])>face_score:
            return True
    return False

distance('114.358817','30.538998','114.35893','30.53898')



