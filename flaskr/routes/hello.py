from flaskr.root import root
from flaskr import db
from flaskr.models import User


@root.route('/hello')
def hello():
    db.drop_all()
    db.create_all()
    user = User(username='Jack')
    db.session.add(user)
    db.session.commit()
    jack = User.query.filter_by(username='Jack').first()
    print('done')
    return f'Hello, {jack.username}!'
