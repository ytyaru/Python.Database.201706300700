import unittest
from CreateTableSqlAnalyzer import CreateTableSqlAnalyzer
class TestCreateTableSqlAnalyzer(unittest.TestCase):

    def test_create_table(self):
        sql = '''create table TBL_NM(Id integer primary key, Name text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        
        self.assertEqual(tblnm, 'TBL_NM')
        self.assertEqual(coldef, c.ColumnDefines)
        self.assertTrue(isinstance(coldef, list))
        self.assertEqual(2, len(coldef))
        for cd in coldef:
            self.assertTrue('name' in cd)
            self.assertTrue('type' in cd)
            self.assertTrue('constraints' in cd)
            
        self.assertEqual('Id', coldef[0]['name'])
        self.assertEqual('integer', coldef[0]['type'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
            
        self.assertEqual('Name', coldef[1]['name'])
        self.assertEqual('text', coldef[1]['type'])
        self.assertTrue('not_null' in coldef[1]['constraints'])
        self.assertTrue(coldef[1]['constraints']['not_null'])

    def test_type(self):
        sql = '''create table TBL_NM(Id integer, Name text, Tax real, Image blob, Null null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        
        self.assertEqual(5, len(coldef))
        self.assertEqual('integer', coldef[0]['type'])
        self.assertEqual('text', coldef[1]['type'])
        self.assertEqual('real', coldef[2]['type'])
        self.assertEqual('blob', coldef[3]['type'])
        self.assertEqual('null', coldef[4]['type'])
    
    def test_Autoincrement(self):
        sql = '''create table TBL_NM(Id integer primary key autoincrement);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('autoincrement' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['autoincrement'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])

    def test_NotNull(self):
        sql = '''create table TBL_NM(Name text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('not_null' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['not_null'])

    def test_Unique(self):
        sql = '''create table TBL_NM(Name text unique);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('unique' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['unique'])

    def test_PrimaryKey(self):
        sql = '''create table TBL_NM(Name text primary key);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])

    def test_Default_text(self):
        sql = '''create table TBL_NM(Name text default 'def_str');'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("'def_str'", coldef[0]['constraints']['default'])

    def test_Default_integer(self):
        sql = '''create table TBL_NM(Age integer default 123);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("123", coldef[0]['constraints']['default'])

    def test_Default_escape(self):
        sql = '''create table TBL_NM(Name text default 'I''am andy.');'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("'I''am andy.'", coldef[0]['constraints']['default'])

    def test_Check(self):
        sql = '''create table TBL_NM(Name text check('FixedName' == Name));'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("'FixedName' == Name", coldef[0]['constraints']['check'])

    def test_Check_space(self):
        sql = '''create table TBL_NM(Name text check   (   'FixedName'   ==   Name   )   );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("'FixedName' == Name", coldef[0]['constraints']['check'])

    def test_Constraints(self):
        sql = '''create table TBL_NM(
    Id      integer primary key autoincrement unique not null default 0 check (Id<100),
    Name    text);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
        self.assertTrue('autoincrement' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['autoincrement'])
        self.assertTrue('unique' in coldef[0]['constraints'])
        self.assertTrue("Id<100", coldef[0]['constraints']['unique'])
        self.assertTrue('not_null' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['not_null'])
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("0", coldef[0]['constraints']['default'])
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("Id<100", coldef[0]['constraints']['check'])

    def test_ForeignKey(self):
        sql = '''create table TBL_NM(
    Id          integer primary key,
    AccountId   integer,
    foreign key(AccountId) references ParentTable(Id));'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertTrue('foreign_key' in coldef[1]['constraints'])
        for cd in coldef:
            if 'foreign_key' in cd['constraints']:
                self.assertEqual('AccountId', cd['name'])
                self.assertEqual('ParentTable', cd['constraints']['foreign_key']['table'])
                self.assertEqual('Id', cd['constraints']['foreign_key']['column'])

    def test_quotation(self):
        sql = '''create table "TBL_NM"("Id" integer primary key, "Name" text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertEqual(tblnm, '"TBL_NM"')
            
        self.assertEqual('"Id"', coldef[0]['name'])
        self.assertEqual('integer', coldef[0]['type'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
            
        self.assertEqual('"Name"', coldef[1]['name'])
        self.assertEqual('text', coldef[1]['type'])
        self.assertTrue('not_null' in coldef[1]['constraints'])
        self.assertTrue(coldef[1]['constraints']['not_null'])

    def test_quotation_escape(self):
        sql = '''create table "T""B""L_NM"("I""d" integer primary key, "N""a""me" text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertEqual(tblnm, '"T""B""L_NM"')
            
        self.assertEqual('"I""d"', coldef[0]['name'])
        self.assertEqual('integer', coldef[0]['type'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
            
        self.assertEqual('"N""a""me"', coldef[1]['name'])
        self.assertEqual('text', coldef[1]['type'])
        self.assertTrue('not_null' in coldef[1]['constraints'])
        self.assertTrue(coldef[1]['constraints']['not_null'])
    
    def test_multi_columns_and_space(self):
        sql = '''create table TBL_NM(
    Id      integer      primary      key      autoincrement     unique    not     null   default      0    check     (Id<100),
    Key     integer      not    null,
    Name    text         not       null,
    Rate    real   default   0.5    check   (     0 <= Tax && (Tax <= 1 || Tax <= 1)      ),
    Image   blob   ,
    Null    null,
    foreign   key   (  Key  )   references   SomeTable   (  SomeId  )
    );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertEqual(6, len(coldef))
        for i, name in enumerate(['Id', 'Key', 'Name', 'Rate', 'Image', 'Null']): self.assertEqual(name, coldef[i]['name'])
        for i, typ in enumerate(['integer', 'integer', 'text', 'real', 'blob', 'null']): self.assertEqual(typ, coldef[i]['type'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
        self.assertTrue('autoincrement' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['autoincrement'])
        self.assertTrue('unique' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['unique'])
        self.assertTrue('not_null' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['not_null'])
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("0", coldef[0]['constraints']['default'])
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("Id<100", coldef[0]['constraints']['check'])

        self.assertTrue('not_null' in coldef[1]['constraints'])
        self.assertTrue(coldef[1]['constraints']['not_null'])
        self.assertTrue('foreign_key' in coldef[1]['constraints'])
        self.assertTrue('table' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('column' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('SomeTable', coldef[1]['constraints']['foreign_key']['table'])
        self.assertTrue('SomeId', coldef[1]['constraints']['foreign_key']['column'])
        
        self.assertTrue('not_null' in coldef[2]['constraints'])
        self.assertTrue(coldef[2]['constraints']['not_null'])
        
        self.assertTrue('default' in coldef[3]['constraints'])
        self.assertEqual('0.5', coldef[3]['constraints']['default'])
        self.assertTrue('check' in coldef[3]['constraints'])
        self.assertEqual('0 <= Tax && (Tax <= 1 || Tax <= 1)', coldef[3]['constraints']['check'])

    def test_multi_columns_and_space_and_quoat_escape(self):
        sql = '''create table """T""BL NM""" (
    "I""d"      integer      primary      key      autoincrement     unique    not     null   default      0    check     (Id<100),
    """K"" ey"""    integer      not    null,
    "N""""ame"    text         not       null  check( "N""""ame" == 'ABC' || "N""""ame" == 'DEF' ),
    """R""ate"""    real   default   0.5    check   (     0 <= Tax && (Tax <= 1 || Tax <= 1)      ),
    "I""mage"   blob   ,
    "N""ull"    null,
    MyColumn    text,
    foreign   key   (  """K"" ey"""  )   references   "Some ""Table"   (  "Some"" Id"  )
    );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        self.assertEqual('"""T""BL NM"""', tblnm)
        self.assertEqual(7, len(coldef))
        for i, name in enumerate(['"I""d"', '"""K"" ey"""', '"N""""ame"', '"""R""ate"""', '"I""mage"', '"N""ull"', 'MyColumn']): self.assertEqual(name, coldef[i]['name'])
        for i, typ in enumerate(['integer', 'integer', 'text', 'real', 'blob', 'null', 'text']): self.assertEqual(typ, coldef[i]['type'])
        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
        self.assertTrue('autoincrement' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['autoincrement'])
        self.assertTrue('unique' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['unique'])
        self.assertTrue('not_null' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['not_null'])
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("0", coldef[0]['constraints']['default'])
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("Id<100", coldef[0]['constraints']['check'])

        self.assertTrue('not_null' in coldef[1]['constraints'])
        self.assertTrue(coldef[1]['constraints']['not_null'])
        self.assertTrue('foreign_key' in coldef[1]['constraints'])
        self.assertTrue('table' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('column' in coldef[1]['constraints']['foreign_key'])
        self.assertTrue('"Some ""Table"', coldef[1]['constraints']['foreign_key']['table'])
        self.assertTrue('"Some"" Id"', coldef[1]['constraints']['foreign_key']['column'])
        
        self.assertTrue('not_null' in coldef[2]['constraints'])
        self.assertTrue(coldef[2]['constraints']['not_null'])
        self.assertTrue('check' in coldef[2]['constraints'])
        self.assertEqual('"N""""ame" == \'ABC\' || "N""""ame" == \'DEF\'', coldef[2]['constraints']['check'])
        
        self.assertTrue('default' in coldef[3]['constraints'])
        self.assertEqual('0.5', coldef[3]['constraints']['default'])
        self.assertTrue('check' in coldef[3]['constraints'])
        self.assertEqual('0 <= Tax && (Tax <= 1 || Tax <= 1)', coldef[3]['constraints']['check'])

    
    def test_const_sequence(self):
        sql = '''create table TBL_NM(
    Id      integer      check ( Id < 100 ) default 0 primary key autoincrement unique not null,
    Key     integer      not    null
    );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)

        self.assertTrue('primary_key' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['primary_key'])
        self.assertTrue('autoincrement' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['autoincrement'])
        self.assertTrue('unique' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['unique'])
        self.assertTrue('not_null' in coldef[0]['constraints'])
        self.assertTrue(coldef[0]['constraints']['not_null'])
        self.assertTrue('default' in coldef[0]['constraints'])
        self.assertEqual("0", coldef[0]['constraints']['default'])
        self.assertTrue('check' in coldef[0]['constraints'])
        self.assertEqual("Id < 100", coldef[0]['constraints']['check'])

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
