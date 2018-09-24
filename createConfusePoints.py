from Model.Urls import URL
from pymongo import MongoClient
import random
import requests
import json

if __name__ == '__main__':
    client = MongoClient()
    coll1 = client.weibodata.location
    coll2 = client.TraceSecret.ConfusePoint
    points = coll1.find({'city': '武汉'})
    i = 0
    for point in points:
        if i > 200:
            break
        params = {'location': point['location']['lon'] + ',' + point['location']['lat'],
                  'width': 400,
                  'height': 400}
        params['ak'] = "jxYzgW7Tp6kXeOlFCSvlsU2WbBZAmAgk"
        params['service_id'] = '150540'
        headers = {
            'cache-control': "no-cache",
            'postman-token': "b3da556e-0d5f-320b-2f8c-68cc4e1e9c62"
        }
        response = requests.request("GET", 'http://api.map.baidu.com/panorama/v2', headers=headers, params=params)
        try:
            result = json.loads(response.text)
        except:
            i += 1
            open('static/confuseImages/' + str(i) + '.jpg', 'wb').write(response.content)
            point['url'] = str(i) + '.jpg'
            coll2.insert_one(point)
