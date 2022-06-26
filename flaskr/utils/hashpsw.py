import hashlib


def getHash(psw):
    md5 = hashlib.md5()
    md5.update(psw.encode())
    return str(md5.hexdigest())