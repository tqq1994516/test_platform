import hashlib


def genearteMD5(str):
    h = hashlib.md5('tian'.encode('utf-8'))
    h.update(str.encode('utf-8'))
    return h.hexdigest()
