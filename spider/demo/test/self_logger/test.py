#coding=utf-8
import logging
'''
logger:记录器，暴露了应用程序代码能直接使用的接口
handler：处理器，将记录器产生的日志记录发送至合适的目的地
filter：过滤器，提供了更好的粒度控制，它可以决定输出拿些日志记录
formatter：格式化器，指明了输出中日志记录的布局
'''

#日志配置
logging.basicConfig(filename='logger.log',level=logging.INFO)

logger = logging.getLogger('main')
logger.setLevel(logging.error) #设置日志级别为ERROR，即只有日志级别大于等于ERROR的日志才会输出
logger.addHandler(logging.FileHandler)

#指定输出格式
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

#日志输出
logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')

