# *-* coding:utf-8 *-*
#
#
#
"""
"""



import ConfigParser
import hashlib
import re
from tornado.log import app_log

from design_model import singleton

class Base(object):

	@staticmethod
	def enum(**enums):
		
		return type('Enum',(),enums)

	@staticmethod
	def check_arguments(keys,essential_keys):

		keys = set(keys)
		essential_keys = set(essential_keys)

		if keys == essential_keys:
			return False
		else:
			return True

	@staticmethod
	def isset(v):

		try:
			type(eval(v))

		except:
			print False
			return False
		else:
			print True
	
			return True
	@staticmethod
	def empty(s):

		return True if 0 == len(s) else False

	@staticmethod
	def md5(s):

		md = hashlib.md5()
		md.update(s)
		return md.hexdigest()

@singleton
class Configer(object):

	def __init__(self,ini_path = ''):
		self.reset(ini_path)

	def reset(self,ini_path):
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(ini_path)
		
		config_dict = {}
		
		for section in self.cf.sections():
			options_list = self.cf.items(section)

			config_dict[section] = {}

			for option_tuple in options_list:
				key = option_tuple[0]
				value = option_tuple[1]
				config_dict[section][key] = value

		self.config_dict = config_dict

	def get_components(self,component):

		components_dict = {}
		component_exp = r'(%s):(\w*)' % component

		exp = re.compile(component_exp)

		for section in self.cf.sections():
			match = exp.match(section)
			
			if match:
				components_dict[section] = {'component':match.group(1),'object':match.group(2)}
	
		return components_dict		

	@property
	def config(self):
			return self.config_dict

def ERROR(msg):
    
    app_log.error(msg) 

def INFO(msg):
    
    app_log.info(msg)

if __name__ == '__main__':

	#keys = set(['a','b'])
	#enssential = set(['c'])
	#print Base.check_parameter(keys,enssential)
	#print keys < enssential

	#print Base.empty('1')
	#c = Configer('../config.ini')

	#print c.config['LOG']['info']
	#print c.get_components('mysql')
    logger = Logger('/home/zhangchunyang/api.log')
    log = logger.get_logger()
    log.info('nihao')
