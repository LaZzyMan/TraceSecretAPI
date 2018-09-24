# -*- coding: UTF-8 -*-
from flask import Flask, make_response, request, jsonify, abort, send_from_directory, send_file
from flask_httpauth import HTTPBasicAuth
from Model.User import User
from werkzeug.utils import secure_filename
import json
import random
import os

TraceSecretAPI = Flask(__name__)
auth = HTTPBasicAuth()
TraceSecretAPI.config['UPLOAD_FOLDER'] = 'static/headImages/'
TraceSecretAPI.config['ALLOW_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

@auth.get_password
def get_password(username):
    if username == 'zz':
        return '20180312'
    return None
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access.'}), 403)

@TraceSecretAPI.route('/')
def hello_world():
    return 'Enter OK'

@TraceSecretAPI.route('/api/v1.0/test')
@auth.login_required
def test():
    return "Auth OK"

'''
0:成功并返回信息
1：用户不存在
2：用户名/密码错误
'''
@TraceSecretAPI.route('/api/v1.0/login', methods = ['PUT'])
@auth.login_required
def register():
    if not request.json:
        abort(404)
    user = User(request.json)
    return jsonify(user.login())

'''
0:注册成功
1：用户名已存在
'''
@TraceSecretAPI.route('/api/v1.0/register', methods = ['PUT'])
@auth.login_required
def login():
    if not request.json:
        abort(404)
    user = User(request.json)
    return jsonify(user.register())

'''
1: 上传成功
0：上传失败
'''
@TraceSecretAPI.route('/api/v1.0/uploadimage', methods = ['POST'])
def uploadimage():
    upload_file = request.files['headimage']
    if upload_file:
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(TraceSecretAPI.root_path, TraceSecretAPI.config['UPLOAD_FOLDER'], filename))
        return jsonify({'result':1})
    else:
        return jsonify({'result':0})

@TraceSecretAPI.route('/api/v1.0/download/<filename>', methods = ['GET'])
def downloadimage(filename):
    return send_from_directory('static/headImages', filename)


@TraceSecretAPI.route('/api/v1.0/editInfo', methods=['PUT'])
@auth.login_required
def editInfo():
    pass


if __name__ == '__main__':
    TraceSecretAPI.run(host='0.0.0.0', port=8080)
