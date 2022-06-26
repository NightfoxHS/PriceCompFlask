from flask_restful import Resource, reqparse
from flask import jsonify, request
from flaskr.models.User import User
from flaskr import db


class AdminSearchOneById(Resource):
    '''
        0. 获取指定id用户记录
        1. 在url中传递id
        2. 供管理员使用
    '''
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='args')
        args = parser.parse_args()
        id = args['id']
        targetUser = User.query.filter_by(id=id).first()
        if targetUser:
            return jsonify(dict(targetUser))    # 查找到，以json格式返回
        else:
            return None # 未找到，返回None

class AdminDeleteOneById(Resource):
    '''
        0. 删除指定id用户记录
        1. 用json传递id
        2. 供管理员使用
    '''
    def delete(self):
        jsonId = request.get_json(force=True)
        user = User.query.filter_by(id=jsonId.get('id')).first()
        if not user:
            return jsonify({
                'AdminStatus': 2 # 错误：用户不存在
            })
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            return jsonify({
                'AdminStatus': 1 # 错误：未能成功删除
            })
        
        return jsonify({
            'AdminStatus': 0 # 成功：成功删除账户
        })

class AdminUpdateOne(Resource):
    '''
        0. 修改指定用户记录
        1. 用json传递修改的信息, 除需要传id以外, 其余与用户api中相同
        2. 供管理员使用
    '''
    def post(self):
        jsonUser = request.get_json(force=True)
        currentUser = User.query.filter_by(id=jsonUser.get('id')).first()

        sameNameUser = User.query.filter_by(username=jsonUser.get('username')).first()  # 用户要改成的名字对应的记录
        if sameNameUser and sameNameUser.id != currentUser.id:
            return jsonify({
                'AdminStatus': 1 # 错误：新用户名已被他人占用
            })
        
        if jsonUser.get('password'):
            plength = len(jsonUser.get('password'))
            if plength < 8 or plength > 16:
                return jsonify({
                    'AdminStatus': 2 # 错误：密码长度不在8~16范围内
                })

        try:
            currentUser.setUser(jsonData=jsonUser)
            db.session.commit()
        except:
            return jsonify({
                'AdminStatus': 3 # 错误：数据库交互发生错误
            })
        
        return jsonify({
            'AdminStatus': 0 # 成功：修改账户信息成功
        })


class AdminSearchAll(Resource):
    '''
        0. 获取所有用户记录
        1. 不需要传递数据
        2. 供管理员使用
    '''
    def get(self):
        res = []
        users = User.query.all()
        for user in users:
            res.append(dict(user))
        return jsonify(res)



class AdminDeleteAll(Resource):
    '''
        0. 删除所有用户
        1. 不需要传递数据
        2. 供管理员使用
    '''
    def delete(self):
        try:
            users = User.query.all()
            for user in users:
                db.session.delete(user)
            db.session.commit()
        except:
            return jsonify({
                'AdminStatus': 1 # 清空用户数据库失败
            })
        return jsonify({
            'AdminStatus': 0 # 成功：清空用户数据库成功
        })