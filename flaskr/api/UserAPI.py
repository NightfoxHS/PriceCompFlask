from flask_restful import Resource
from flask import jsonify, request, session
from flaskr import db
from flaskr.models.User import User
from flaskr.utils.auth import getToken, auth


class UserRegister(Resource):
    '''
        0. 不需要登录
        1. 用户注册
        2. 不传id键
        3. 最少要传username和password键
        4. 用户在注册时未设置的可空字段, 可以传值为null的键, 或不传该键
    '''
    def post(self):
        print('Now registering...')
        
        # jsonUser键名应与models中实体User定义名一致
        jsonUser = request.get_json(force=True) # 获取请求中的用户json数据
        
        sameUser = User.query.filter_by(username=jsonUser.get('username')).first()
        if sameUser:
            return jsonify({
                'registerStatus': 1 # 错误：用户名已存在
            })
        
        plength = len(jsonUser.get('password'))
        if plength < 8 or plength > 16:
            return jsonify({
                'registerStatus': 2 # 错误：密码长度不在8~16范围内
            })
        
        user = User()
        user.setUser(jsonData=jsonUser)
        try:
            db.session.add(user)
            db.session.commit()
            pass
        except:
            return jsonify({
                'registerStatus': 3 # 错误：持久化过程发生错误
            })
        
        return jsonify({
            'registerStatus': 0 # 成功：注册完成
        })


class UserLogin(Resource):
    '''
        0. 不需要登录
        1. 用户登录
        2. 只传username和password键
    '''
    def post(self):
        loginInfoJson = request.get_json(force=True)
        username = loginInfoJson.get('username')
        hashpassword = loginInfoJson.get('password')

        targetUser = User.query.filter_by(username=username).first()
        if targetUser:
            if hashpassword == targetUser.password:
                token = getToken(username,hashpassword)
                return jsonify({
                    'loginStatus': 0,  # 成功：登录完成
                    'token': token
                })
            else:
                return jsonify({
                    'loginStatus': 1 # 失败：密码错误
                })
        else:
            return jsonify({
                'loginStatus': 2 # 失败：用户名不存在
            })


class UserUpdate(Resource):
    '''
        0. 需要登录
        1. 修改当前已登录账户信息
        2. 不传id键(不允许修改id)
        3. 不需要修改的信息(密码除外, 见4)请传递原值
        4. 若要清空某可选字段, 将相应的键的值置null
        5. 若不需要修改密码, password键传null值或干脆不传password键, 也可以传原值(原值只能由用户自己填写)
    '''
    @auth.login_required
    def post(self):
        jsonUser = request.get_json(force=True)
        currentUser = User.query.filter_by(username=auth.current_user().username).first()    # 当前已登录的账户记录

        sameNameUser = User.query.filter_by(username=jsonUser.get('username')).first()  # 用户要改成的名字对应的记录
        if sameNameUser and sameNameUser.id != currentUser.id:
            return jsonify({
                'updateStatus': 1 # 错误：新用户名已被他人占用
            })

        try:
            currentUser.setUser(jsonData=jsonUser)
            db.session.commit()
        except:
            return jsonify({
                'updateStatus': 3 # 错误：数据库交互发生错误
            })
        
        return jsonify({
            'updateStatus': 0 # 成功：修改账户信息成功
        })


class UserCancel(Resource):
    '''
        0. 需要登录
        1. 注销当前已登录账户
        2. 不需要传数据
    '''
    @auth.login_required
    def delete(self):
        print('Now Cancelling...')
        user = User.query.filter_by(username=auth.current_user().username).first()

        try:
            db.session.delete(user)
            db.session.commit()
        except:
            return jsonify({
                'cancelStatus': 1 # 错误：未能成功删除
            })
        
        session.clear()
        return jsonify({
            'cancelStatus': 0 # 成功：成功删除账户, 前端应跳转至登录/注册页
        })


class UserSearch(Resource):
    '''
        0. 需要登录
        1. 获取当前已登录的账户信息
        2. 不需要传递数据
        3. 获得的密码是哈希值, 不具有意义
    '''
    @auth.login_required
    def get(self):
        print("Now searching current account info...")
        try:
            currentUser = User.query.filter_by(id=session.get('id')).first()
        except:
            return None # 查询错误返回空
        return jsonify(dict(currentUser))   # 查询成功返回当前账户的json

