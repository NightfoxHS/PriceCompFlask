from datetime import datetime
from flaskr import db
from flaskr.utils.hashpsw import getHash

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80))
    gender = db.Column(db.String(4))
    birthday = db.Column(db.Date)
    mailaddr = db.Column(db.String(80))
    phonenum = db.Column(db.String(11))
    qq = db.Column(db.String(13))
    intro = db.Column(db.String(80))

    def setUser(self, jsonData):
        self.username = jsonData.get('username')
        if jsonData.get('password'):
            self.password = getHash(jsonData.get('password'))    # hash
        self.nickname = jsonData.get('nickname')
        self.gender = jsonData.get('gender')
        birStr = jsonData.get('birthday')
        if birStr:
            year, mon ,day = jsonData.get('birthday').split('-')
            self.birthday = datetime(int(year), int(mon), int(day))
        self.mailaddr = jsonData.get('mailaddr')
        self.phonenum = jsonData.get('phonenum')
        self.qq = jsonData.get('qq')
        self.intro = jsonData.get('intro')

    def keys(self):
        return ('id', 'username', 'password', 'nickname', 'gender', 'birthday', 'mailaddr', 'phonenum', 'qq', 'intro')


    def __getitem__(self, item):
        return getattr(self, item)


    def __repr__(self):
        return '<User %r>' % self.username
