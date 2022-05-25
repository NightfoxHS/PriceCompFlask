from flask_restful import Resource
from flask_restful import reqparse

from flaskr.crawlers import *

class ItemAPI(Resource):
    def get(self):
        print('be called')
        parser = reqparse.RequestParser()
        parser.add_argument('keywords',required=True,help='keywords should not be empty',location='args')
        parser.add_argument('num',type=int,required=True,help='num should not be empty, or num value is not accepted',location='args')
        parser.add_argument('port',location='args')
        args = parser.parse_args()
        print(args)
        keywords = args['keywords']
        num = args['num']
        port = args['port']
        res = []

        jd = JD(keywords,num)
        sn = SN(keywords,num)
        if  port == None:
            res += jd.getItems()
            res += sn.getItems()
        else:
            if 'j' in args['port']:
                res += jd.getItems()
            if 's' in args['port']:
                res += sn.getItems()
        return res

