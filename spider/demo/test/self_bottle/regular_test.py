#coding=utf-8
import re
# k = re.match(r'[^/]+','hello world')
# print k.group(0) #() == 0, () == 1 ...

#python 正则表达式分组的概念，然后不捕获分组，然后不转义的标志r(给正则表达式使用)
def _re_flatten(p):
    ''' Turn all capturing groups in a regular expression pattern into
        non-capturing groups. '''
    if '(' not in p: return p
    return re.sub(r'(\\*)(\(\?P<[^>]+>|\((?!\?))',
        flatten, p)
    
def flatten(m):
    print m.group(0),m.group(1),m.group(2)
    return m.group(0) if len(m.group(1)) % 2 else m.group(1) + '(?:'

#(?:)匹配但是不捕获
    
# k2 = re.match('(?=hopeful)hope','hopeful')
# print k2.groups()
# 
# k2 = re.match('hope(?=ful)','hopeful')
# print k2.group()

print _re_flatten(r'\\(h)')

print '*' * 10
m = re.match(r'\\*','(h)')
print m.group()
print '*' * 10

# m = re.search('\\\\','(\\\\)') #== m = re.search(r'\\','(\)')
# print m.group(0)


# m2 = re.match('(?!\?)','(a)')
# print m2.group()

m = re.match(r'\d+','888')
print m.group()


rule_syntax = re.compile('(\\\\*)'\
        '(?:(?::([a-zA-Z_][a-zA-Z_0-9]*)?()(?:#(.*?)#)?)'\
          '|(?:<([a-zA-Z_][a-zA-Z_0-9]*)?(?::([a-zA-Z_]*)'\
            '(?::((?:\\\\.|[^\\\\>]+)+)?)?)?>))')

ru = rule_syntax.finditer('\\adfasdfa')
print 1
for u in ru:
    print ru.start()

print 'qq'.endswith('.q')
print '//'.count('/')