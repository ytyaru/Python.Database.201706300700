import re
p = re.compile(r'foreign key[ ]*\((?P<word>\w+)\)')
m = p.search('foreign key(Id)')
print(m.group('word'))

m = p.search('foreign key   (Id)')
print(m.group('word'))
