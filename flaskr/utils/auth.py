from itsdangerous import URLSafeSerializer
from flaskr.models.User import User
from flaskr import auth
from flask import current_app



def getToken(username, hashpassword):
    '''
        生成并返回token
        token中包括私钥、用户名、哈希密码
    '''
    s = URLSafeSerializer('secret_key', current_app.config['SECRET_KEY'])

    userInfo = {'username': username, 'password': hashpassword}
    token = s.dumps(userInfo)

    return token

@auth.verify_token
def verify_token(token):
    '''
        验证token
    '''
    print(token)
    s = URLSafeSerializer('secret_key', current_app.config['SECRET_KEY'])

    try:
        userInfo = s.loads(token)
    except:
        return False    # 验证失败：token错误或过期
    username = userInfo['username']
    hashpassword = userInfo['password']
    targetUser = User.query.filter_by(username=username).first()
    if targetUser:
        if hashpassword == targetUser.password:
            return True     # 验证成功
    return False    # 验证失败：用户信息错误