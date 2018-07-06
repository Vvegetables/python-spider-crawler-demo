import sys

'''
这些模块路径会在服务器上出错，这个问题 我至今未找到问题所在。很遗憾。
'''

sys.path

print sys.path
from moduletestmain.sub1.ssub1 import ssub1
 
ssub1()