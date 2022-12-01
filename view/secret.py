import hashlib


def check(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest() == "41198a3a3426d0f1245ec7120d517272"
