import re
#p = re.compile(r'foreign key[ ]*\(["]?(?P<key>\w+["]?)\)[ ]+references[ ]+(?P<table>\w+)[ ]*\((?P<column>\w+)\)')
#p = re.compile(r'foreign[ ]+key[ ]*\([ ]*(?P<key>\w+)[ ]*\)[ ]+references[ ]+(?P<table>\w+)[ ]*\([ ]*(?P<column>\w+)[ ]*\)')
#p = re.compile(r'foreign[ ]+key[ ]*\([ ]*["]?(?P<key>\w+)["]?[ ]*\)[ ]+references[ ]+["]?(?P<table>\w+)["]?[ ]*\([ ]*["]?(?P<column>\w+["]?[ ]*)\)')

#p = re.compile(r'foreign[ ]+key[ ]*\([ ]*["]*(?P<key>\w+)["]*[ ]*\)[ ]+references[ ]+["]*(?P<table>\w+)["]*[ ]*\([ ]*["]*(?P<column>\w+)["]*[ ]*\)')
#p = re.compile(r'foreign[ ]+key[ ]*\((?P<key>.+)\)[ ]+references[ ]+(?P<table>.+)[ ]*\((?P<column>.+)\)')
#p = re.compile(r'foreign[ ]+key[ ]*\([\s]*(?P<key>.+)[\s]*\)[ ]+references[ ]+(?P<table>.+)[ ]*\([\s]*(?P<column>.+)[\s]*\)')
#p = re.compile(r'foreign[\s]+key[\s]*\([\s]*(?P<key>.+)[\s]*\)[\s]+references[\s]+(?P<table>.+)[\s]*\([\s]*(?P<column>.+)[\s]*\)') # ()内後ろのスペースがとれない
p = re.compile(r'foreign[\s]+key[\s]*\((?P<key>.+)\)[\s]+references[\s]+(?P<table>.+)[\s]*\((?P<column>.+)\)')

m = p.search('foreign key(Id) references ParentTable(Column)')
print(m.group('key'), m.group('table'), m.group('column'))

m = p.search('foreign key   (Id)       references       ParentTable(Column)')
print(m.group('key'), m.group('table'), m.group('column'))

m = p.search('foreign key   (Id)       references       ParentTable        (Column)')
print(m.group('key'), m.group('table'), m.group('column'))

m = p.search('foreign key   ("Id")       references       ParentTable        (Column)')
print(m.group('key'), m.group('table'), m.group('column'))

m = p.search('foreign key   (  "Id"  )    references    "ParentTable"     (  "Column"  )')
print(m.group('key'), m.group('table'), m.group('column'))
print('[', m.group('key'), ']')
print('[', m.group('table'), ']')
print('[', m.group('column'), ']')
print('[', m.group('key').strip(), ']')
print('[', m.group('table').strip(), ']')
print('[', m.group('column').strip(), ']')

m = p.search('foreign key   ("I""d")       references       ParentTable        (Column)')
print(m.group('key'), m.group('table'), m.group('column'))

