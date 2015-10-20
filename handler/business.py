# *-*coding:utf8*-*

from hashlib import sha1,md5
import random
import time

class User(object):

    @staticmethod
    def gen_uid(unique_value):

        return sha1(unique_value).hexdigest()

    @staticmethod
    def gen_token(uid,host,remote_ip):

        return sha1(uid + host + remote_ip + str(time.time())).hexdigest()

    @staticmethod
    def gen_sessionid(token):

        return sha1(token + str(random.random())).hexdigest()

    @staticmethod
    def encrypt_password(password):

        return md5(password).hexdigest()



        
