import requests
import json

import base64
url='https://aip.baidubce.com/rest/2.0/face/v3/match'
headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}


def base64encode(path):
	with open(path, 'rb') as f:
		base64_data = base64.b64encode(f.read())
		s = base64_data.decode()
		return s



params = json.dumps(
    [{"image": base64encode('pic1.jpg'), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
     {"image": base64encode('pic2.jpg'), "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}])
access_token = '24.5aebb7b7924572c01e121a30255b73c1.2592000.1564937272.282335-16723292'
request_url = url + "?access_token=" + access_token
respose=requests.post(request_url,data=params,headers=headers)

data=json.loads(respose.text)
print(data['result']['score'])


