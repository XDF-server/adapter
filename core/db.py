# *-* coding:utf-8 *-*

import MySQLdb 
import redis
from redis.exceptions import RedisError

from base import Base,INFO,ERROR
from exception import MysqlException,RedisException

class Mysql(object):

    def __init__(self,**args):
    
        self._connect_flag = False

        self._cur = None
        self._conn = None

        self.reset(**args)

    def reset(self,**args):

        mysql_config = {'host':args['host'],'port':int(args['port']),'user':args['user'],
                        'passwd':args['password'],'charset':args['charset'],'connect_timeout':int(args['timeout'])}

        #status: 0 free;1 used;
        self._status = 0
        self._event_flag = False
        self._sql = ''

        if self._connect_flag:
            self._cur.close()
            self._conn.close() 

        try:
            self._conn = MySQLdb.connect(**mysql_config)
            self._cur = self._conn.cursor()
            self._connect_flag = True

        except MySQLdb.Error,e:
            self._connect_flag = False
            ERROR('Mysql Error -- msg[Connect Failed]')
            raise MysqlException('Connect Failed')

    def start_event(self):

        self._conn.autocommit(False)
        self._conn.begin()
        self._event_flag = True

    def exec_event(self,sql,**kwds):

        if self.event_flag:
            res = self.query(sql,**kwds)
            return res

        else:
            ERROR('Mysql Error -- [Not Start Event]')
            raise MysqlException('Not Start Event')

    def end_event(self):
        
        if self._event_flag:
            self._conn.commit()
            self._conn.autocommit(True)
            self._event_flag = False

    def query(self,sql,**kwds):

        try:
            self._sql = sql % kwds
            self._cur.execute(self.sql)  
            INFO('Mysql -- execute SQL[%s]' % (self.sql))

        except MySQLdb.Error,e:
            self._event_flag = False
            ERROR('Mysql Error -- SQL[%s] -- msg[Mysql Execute Failed%s]' % (self.sql,e))
            raise MysqlException('Mysql Execute Failed')
        
        except:
            ERROR('Mysql Error -- msg[Sql Format Failed] -- SQL[%s]' % self.sql)
            raise MysqlException('Sql Format Failed')
    
        if self._cur.rowcount:
            return True
        
        else:
            return False

    def rollback(self):
        
        self._conn.rollback()

    def fetch(self):
        
        return self._cur.fetchone()

    def fetchall(self):
        
        return self._cur.fetchall()

    def commit(self):

        self._conn.commit()

    @property
    def id(self):

        return int(self._conn.insert_id())

    @property
    def sql(self):
                
        return self._sql

    @property
    def status(self):

        return self._status

    @status.setter
    def status(self,status):
        
        self._status = status    

    def __def__(self):

        self._cur.close()
        self._conn.close()


class Redis(object):
        
    def __init__(self,**args):
        
        self._redis = None

        self.reset(**args)
        
    def reset(self,**args):

        redis_config = {'host':args['host'],'port':int(args['port']),'password':args['password'],
                        'db':int(args['db']),'socket_timeout':int(args['timeout']),'charset':args['charset']}

        self._name = ''
        
        self._redis = redis.StrictRedis(**redis_config)

    def hmset(self,name,arg_dict):
        
        try:
            self._redis.hmset(name,arg_dict)       
            INFO('Redis hmset -- redis command[hmset %s %s]' % (name,arg_dict))

        except RedisError:
            raise RedisException

    def hset(self,name,key,value):

        try:
            self._redis.hset(name,key,value)       
            INFO('Redis hset -- redis command[hset %s %s %s]' % (name,key,value))

        except RedisError:
            raise RedisException

    def hget(self,name,key):

        try:
            value = self._redis.hget(name,key)
            INFO('Redis hget -- redis command[hget %s %s]' % (name,key))

        except RedisError:
            raise RedisException

        return value 
    
    def hgetall(self,name):

        try:
            values =  self._redis.hgetall(name)       
            INFO('Redis hgetall -- redis command[hgetall %s]' % name)

        except RedisError:
            raise RedisException

        return values

    def exists(self,name):

        try:
            ret = self._redis.exists(name)       
            INFO('Redis exists -- redis command[exists %s]' % (name))

        except RedisError:
            raise RedisException

        return ret 

    def setex(self,name,time,value):

        try:
            self._redis.setex(name,time,value)
            INFO('Redis setex -- redis command[setex %s %s %s]' % (name,time,value))

        except ReidsError:
            raise RedisExceptions

    def expire(self,name,time):
        
        try:
            self._redis.expire(name,time)
            INFO('Redis expire -- redis command[expire %s %d]' % (name,time))

        except ReidsError:
            raise RedisExceptions

    def delete(self,*name):
    
        try:
            self._redis.delete(*name)
            INFO('Redis delete -- redis command[delete %s]' % name)

        except ReidsError:
            raise RedisException

    @property
    def name(self):

        return self._name

    @name.setter
    def name(self,name):

        self._name = name
