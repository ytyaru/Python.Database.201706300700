import re
p = re.compile(r'foreign key (?P<word>\b\w+)')
m = p.search( '(((( foreign key Lots of punctuation )))' )
print(m)
print(m.groups())
print(m.group('word'))
