# *-* coding:utf-8 *-*

from design_model import singleton
from db import Mysql,Redis
import loader

class MysqlManager(object):

    def __init__(self):

        self.reset()

    def reset(self):
        
        self._mysql_pools = {}
                
        mysql_components = loader.loader.config_handler.get_components('mysql')

        for name,value in mysql_components.items():
            mysql_config = loader.loader.config[name]
            max_connections = int(mysql_config['max_connections'])
    
            mysql_pool = []		
        
            for i in range(max_connections):
                mysql = Mysql(**mysql_config)
                mysql_pool.append(mysql)
        
            self._mysql_pools[value['object']] = mysql_pool
    
    def __getattr__(self,name):

        for mysql in self._mysql_pools[name]:
            if not mysql.status:
                mysql.status = 1
                return mysql

        print '连接数已满'



class RedisManager(object):

    def __init__(self):
    
        self.reset()

    def reset(self):
    
        self._redis_pool = {}

        redis_components = loader.loader.config_handler.get_components('redis')

        for name,value in redis_components.items():
            redis_config = loader.loader.config[name]
            
            redis = Redis(**redis_config)
            redis.name = name
            self._redis_pool[value['object']] = redis

    def __getattr__(self,name):

        return self._redis_pool[name]


	
		
		
		

		

