import pathlib
import databases.DatabaseLoader

l = databases.DatabaseLoader.DatabaseLoader(pathlib.Path('.').resolve())
print('l.Databases:', l.Databases)
for key, db in l.Databases.items():
#    print(key, db)
#    print(db.DatasetDb)
    for t in db.Tables:
        print(t.Name, 'レコード数', db.DatasetDb[t.Name].count())

