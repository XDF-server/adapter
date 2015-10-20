# *-*coding:utf8*-*
# 
# Copyright 2015 Adapter
#

"""
    Api of user
    ===========
"""

from business import User
from core.base import INFO,ERROR
from core.api import API
from core.exception import MysqlException,RedisException


TOKEN_EXPIRE_TIME =  604800
SESSION_EXPIRE_TIMe = 3600

class RegisterByPhone(API):
    """
        register_by_phone (http post)
        -----------------------------
        Register by phone,phone number is unique in application.

        Args:
            #. phone_number
               Phone number,max length is 11.
            #. password
               Rsa encrypt password with public key.
        
        Returns:
            #. code:0
               Register successful.
            #. code:1
               In arguments not match or ensential key is empty.
            #. code:3
               Server exception,may be mysql service hang out.
            #. code:5
               Register phone exist.

    """
    def post(self):

        if self.check_arguments('phone_number','password','os'):
            self.end('ARG')
            return

        if self.check_arguments_empty('phone_number','password','os'):
            self.end('ARG')
            return

        phone_number = self.arguments['phone_number']
        password = self.arguments['password']

        encrypt_password = User.encrypt_password(password)

        uid = User.gen_uid(phone_number)

        INFO('Register -- uid[%s]' % uid)

        register_sql = "insert into adapter.adapter_login_info (user_id,user_phone,user_password) values ('%(user_id)s','%(user_phone)s','%(user_password)s');"
        user_info = {'password':password,'phone':phone_number,'email':'','name':'','sns':''}

        try:
            if self.redis_user.exists(uid):
                self.end('EXT')
                return 

            self.mysql_master.start_event()
            self.mysql_master.query(register_sql,user_id = uid,user_phone = phone_number,user_password = encrypt_password)
        
            self.redis_user.hmset(uid,user_info)

        except MysqlException:
            self.rollback()
            self.end('SVR')
            return 
        
        except RedisException:
            self.end('SVR')
            return 

        self.mysql_master.end_event()

        self.end('SUC')

class LoginByToken(API):
    """
        login_by_token (http get)
        -------------------------
        Login by token,server pass token when login.

        Args:
            #. token
               phone number,max length is 11.

        Returns:
            #. code:0
               Login successful.
               Return sessionid and token.
            #. code:1
               In arguments not match or ensential key is empty.
            #. code:3
               Server exception,maybe redis service hang out.
            #. code:4
               Token not exist,maybe token expired or illegal token.

    """
    def get(self):

        if self.check_arguments('token'):
            self.end('ARG')
            return

        if self.check_arguments_empty('token'):
            self.end('ARG')
            return

        token = self.arguments['token']

        try:
            if self.redis_token.exists(token):
                uid = self.redis_token.hget(token,'uid')
                
                new_token = User.gen_token(uid,self.host,self.remote_ip)
                new_sessionid = User.gen_sessionid(token)
                token_info = {'uid':uid,'sessionid':new_sessionid}
                self.redis_token.hmset(new_token,token_info)
                self.redis_token.expire(new_token,TOKEN_EXPIRE_TIME)
                self.redis_token.delete(token)

                session_info = {'uid':uid,'token':token}
                self.redis_session.hmset(new_sessionid,session_info)
                #self.expire(new_sessionid,SESSION_EXPIRE_TIME)

                INFO('UserLOginByTOken -- token[%s] -- session[%s] -- uid[%s]' % (new_token,new_sessionid,uid))

                ret_dict = {'token':new_token,'sessionid':new_sessionid}

                self.end('SUC',**ret_dict)
                return 

            else:
                self.end('KEY')
                return 
        
        except RedisException:
                self.end('SVR')
                return

class Login(API):
    """
        login (http get)
        ----------------
        Login by identify id and password.

        Args:
            #. identify_id
               Identify id in application,it's phone or email now.
            #. password
               Rsa encrypt password with public key.

        Returns:
            #. code:0
               Login successful.
               Return sessionid and token.
            #. code:1
               In arguments not match or ensential key is empty.
            #. code:3
               Server exception,maybe redis service hang out.
            #. code:4
               Token not exist,maybe token expired or illegal token.

    """
    def get(self):

        if self.check_arguments('identify_id','password'):
            self.end('ARG')
            return

        if self.check_arguments_empty('identify_id','password'):
            self.end('ARG')
            return

        identify_id = self.arguments['identify_id'] 
        password = self.arguments['password'] 

        try:
            uid = User.gen_uid(identify_id)

            if password == self.redis_user.hget(uid,'password'):
                token = User.gen_token(identify_id,self.host,self.remote_ip) 
                sessionid = User.gen_sessionid(token)

                token_info = {'uid':uid,'sessionid':sessionid}
                self.redis_token.hmset(token,token_info)
                self.redis_token.expire(token,TOKEN_EXPIRE_TIME)
                
                session_info = {'uid':uid,'token':token}
                self.redis_session.hmset(sessionid,session_info)

                INFO('Login -- token[%s] -- sessionid[%s] -- uid[%s]' % (token,sessionid,uid))

                ret_dict = {'token':token,'sessionid':sessionid}
                self.end('SUC',**ret_dict)

            else:
                self.end('PWD')
                return
    
        except RedisException:
            self.end('SVR')
            return

class Logout(API):
    """
        logout (http get)
        -----------------
        Logout by sessionid.

        Args:
            #. sessionid
               Sessionid id a unique id of online.

        Returns:
            #. code:0
               Login successful.
               Return sessionid and token.
            #. code:1
               In arguments not match or ensential key is empty.
            #. code:3
               Server exception,maybe redis service hang out.
            #. code:4
               Token not exist,maybe token expired or illegal token.

    """

    def get(self):
        
        if self.check_arguments('sessionid'):
            self.end('ARG')
            return

        if self.check_arguments_empty('sessionid'):
            self.end('ARG')
            return      

        sessionid = self.arguments['sessionid']

        try:
            self.redis_session.delete(sessionid)

            INFO('Logout -- sessionid[%s]' % sessionid)

            self.end('SUC')
        
        except RedisException:
            self.end('SVR')
            return 
               
 
