# *-* coding:utf-8 *-*
#
#
#
#
"""
"""



from base import Base,Configer
from manager import MysqlManager,RedisManager

class Loader(object):

    def __init__(self):
        
        self._config = {}
        self._config_handler = None
        
        self._err_code = {}

        self._mysql_manager = None
        self._redis_manager = None

    def load_config(self,config_path):
    
        configer = Configer(config_path)
        self._config_handler = configer
        self._config = configer.config

    def load_err_code(self):
        
        err_code = {'SUC' : {'code':0,'message':'success'},
                    'ARG' : {'code':1,'message':'invalid arguments'},
                    'SVR' : {'code':2,'message':'server error'},
                    'TOKEN' : {'code':3,'message':'invalid token'},
                    'KEY' : {'code':4,'message':'key not exist'},
                    'EXT' : {'code':5,'message':'key exist'},
                    'PWD' : {'code':6,'message':'password wrong'}
                    }

        self._err_code = err_code

    def load_mysql_manager(self):
        
        self._mysql_manager = MysqlManager()

    def load_redis_manager(self):
        
        self._redis_manager = RedisManager()

    @property
    def config(self):
        
        return self._config

    @property
    def config_handler(self):
        
        return self._config_handler

    @property
    def err_code(self):

        return self._err_code

    @property
    def mysql_manager(self):
        
        return self._mysql_manager

    @property
    def redis_manager(self):
        
        return self._redis_manager


loader = Loader()

def load_config():

    loader.load_config()

def load_err_code():

    loader.load_err_code()
 
def load_mysql_manager():

    loader.load_mysql_manager()   

def load_redis_manager():

    loader.load_redis_manager()   
