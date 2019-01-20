from django.conf import settings
import hashlib


# 加密  用 setting  中的   SECRET_KEY  加盐
def set_password(password):
    strs = '{}{}'.format(password, settings.SECRET_KEY)
    h = hashlib.md5(strs.encode('utf-8'))
    return h.hexdigest()
