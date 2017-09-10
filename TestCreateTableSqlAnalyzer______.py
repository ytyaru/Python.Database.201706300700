import unittest
from CreateTableSqlAnalyzer import CreateTableSqlAnalyzer
class TestCreateTableSqlAnalyzer(unittest.TestCase):

    def test_foreignkey_multi(self):
        sql = '''create table "TBL_NM"(
    "Id"        integer primary key,
    "AccountId" integer,
    "SecondId"  integer,
    foreign key ("AccountId", "SecondId") references Parent (Id, Uid)
);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('foreign_key' in coldef[1]['constraints'])
        self.assertTrue('table' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('column' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('Parent', coldef[1]['constraints']['foreign_key']['table'])
        self.assertTrue('Id', coldef[1]['constraints']['foreign_key']['column'])
        
        self.assertTrue('foreign_key' in coldef[2]['constraints'])
        self.assertTrue('table' in coldef[2]['constraints']['foreign_key'])
        self.assertTrue('column' in coldef[2]['constraints']['foreign_key'])
        self.assertTrue('Parent', coldef[2]['constraints']['foreign_key']['table'])
        self.assertTrue('Uid', coldef[2]['constraints']['foreign_key']['column'])



if __name__ == '__main__':
    unittest.main()
