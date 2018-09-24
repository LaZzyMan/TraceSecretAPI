import requests
import json
import datetime
import math
from pymongo import MongoClient

class URL:
    def __init__(self):
        client = MongoClient()
        db = client.TraceSecret
        self.coll = db.StayPoint
        self.urls = {'stayPoint': "http://yingyan.baidu.com/api/v2/analysis/staypoint",
                     'geocoder': 'http://api.map.baidu.com/geocoder/v2/',
                     'imageView': 'http://api.map.baidu.com/panorama/v2'}
        today = datetime.datetime.today()
        self.startTime = datetime.datetime(today.year, today.month, today.day, 0, 0, 0).timestamp() - 86400*4
        self.endTime = self.startTime + 86399

    def getJSON(self, method, params):
        params['ak'] = "jxYzgW7Tp6kXeOlFCSvlsU2WbBZAmAgk"
        params['service_id'] = '150540'
        headers = {
            'cache-control': "no-cache",
            'postman-token': "b3da556e-0d5f-320b-2f8c-68cc4e1e9c62"
        }
        response = requests.request("GET", method, headers=headers, params=params)
        return json.loads(response.text)

    def getFile(self, method, params, filename):
        params['ak'] = "jxYzgW7Tp6kXeOlFCSvlsU2WbBZAmAgk"
        params['service_id'] = '150540'
        headers = {
            'cache-control': "no-cache",
            'postman-token': "b3da556e-0d5f-320b-2f8c-68cc4e1e9c62"
        }
        response = requests.request("GET", method, headers=headers, params=params)
        open('static/pointImages/'+filename, 'wb').write(response.content)


    def getStayPoint(self, id):
        timeArray = []
        timeInterval = math.floor((self.endTime - self.startTime)/6)
        for i in range(6):
            timeArray.append({'index': i,
                              'startTime': self.startTime+i * timeInterval,
                              'endTime': self.startTime + (i+1)*timeInterval})
        timeArray[5]['endTime'] = self.endTime

        params = {"entity_name": id,
                  "process_option": "need_denoise= 1,need_vacuate=0,need_mapmatch=1,transport_mode=2"}
        stayPoint = []
        for t in timeArray:
            params['start_time'] = int(t['startTime'])
            params['end_time'] = int(t['endTime'])
            result = self.getJSON(self.urls['stayPoint'], params)
            if result['status'] == 0:
                if result['staypoint_num'] == 0:
                    continue
                for point in result['stay_points']:
                    filename = id + '_' + str(point['start_time']) + '.jpg'
                    point['poiid'] = self.getImageView(point['stay_point']['latitude'], point['stay_point']['longitude'], filename)
                    point['url'] = filename
                    point['user'] = id
                    self.coll.insert_one(point)
                    stayPoint.append(point)
        if len(stayPoint) == 0:
            return {'state': 1}
        else:
            return {'state': 0, 'num': len(stayPoint)}

    def getAddress(self, lat, lon):
        geocoderParams = {
            'location': str(lat) + ',' + str(lon),
            'pois': 1,
            'radius': 100,
            'output': 'json'}
        result = self.getJSON(self.urls['geocoder'], geocoderParams)
        if result['status'] == 0:
            return result['result']

    def getImageView(self, lat, lon, filename):
        address = self.getAddress(lat, lon)
        params = {'location': str(lon) + ',' + str(lat),
                  'width': 400,
                  'height': 400}
        if len(address['pois']) == 0:
            self.getFile(self.urls['imageView'], params, filename)
            return 'null'
        else:
            params['poiid'] = address['pois'][0]['uid']
            self.getFile(self.urls['imageView'], params, filename)
            return params['poiid']


