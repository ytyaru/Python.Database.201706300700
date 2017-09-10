import re
p = re.compile(r'foreign key[ ]*\((?P<word>\w+)\)[ ]+references[ ]+(?P<table>\w+)[ ]*\((?P<column>\w+)\)')
m = p.search('foreign key(Id) references ParentTable(Column)')
print(m.group('word'), m.group('table'), m.group('column'))

m = p.search('foreign key   (Id)       references       ParentTable(Column)')
print(m.group('word'), m.group('table'), m.group('column'))

m = p.search('foreign key   (Id)       references       ParentTable        (Column)')
print(m.group('word'), m.group('table'), m.group('column'))

