#!/usr/bin/python2.7
# *-*coding:utf8*-*
#
# Copyright 2015 Adapter
#

"""Service entrance.

Add handler and load super global variables here.

"""


from tornado import httpserver,ioloop,web
from tornado.options import options

from core.loader import loader

options.define('port',default = 6666,help = 'this is default port',type = int)
options.define('config',default = 'config.ini',help = 'this is default config path',type = str)

if __name__ == '__main__':
    
    options.parse_command_line()

    loader.load_config(options.config)
    loader.load_err_code()
    loader.load_mysql_manager()
    loader.load_redis_manager()

    from handler.user import RegisterByPhone,LoginByToken,Login,Logout

    application = web.Application(handlers = [
    (r'/register_by_phone',RegisterByPhone),
    (r'/login',Login),
    (r'/login_by_token',LoginByToken),
    (r'/logout',Logout)
    ])

    http_server = httpserver.HTTPServer(application,xheaders = True)

    http_server.listen(options.port)

    ioloop.IOLoop.instance().start()



