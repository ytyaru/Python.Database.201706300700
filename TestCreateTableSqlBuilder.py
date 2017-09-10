import unittest
from CreateTableSqlAnalyzer import CreateTableSqlAnalyzer
from CreateTableSqlBuilder import CreateTableSqlBuilder
class TestCreateTableSqlBuilder(unittest.TestCase):
    def test_create_table(self):
        sql = '''create table TBL_NM(Id integer primary key, Name text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id   integer primary key,
    Name text    not null
);''')
    
    def test_type(self):
        sql = '''create table TBL_NM(Id integer, Name text, Tax real, Image blob, Null null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)        
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id    integer,
    Name  text,
    Tax   real,
    Image blob,
    Null  null
);''')
    
    def test_Autoincrement(self):
        sql = '''create table TBL_NM(Id integer primary key autoincrement);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id integer primary key autoincrement
);''')
    
    def test_NotNull(self):
        sql = '''create table TBL_NM(Name text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text not null
);''')
    
    def test_Unique(self):
        sql = '''create table TBL_NM(Name text unique);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text unique
);''')
    
    def test_PrimaryKey(self):
        sql = '''create table TBL_NM(Name text primary key);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text primary key
);''')
    
    def test_Default_text(self):
        sql = '''create table TBL_NM(Name text default 'def_str');'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text default 'def_str'
);''')
    
    def test_Default_integer(self):
        sql = '''create table TBL_NM(Age integer default 123);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Age integer default 123
);''')
    
    def test_Default_escape(self):
        sql = '''create table TBL_NM(Name text default 'I''am andy.');'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text default 'I''am andy.'
);''')
    
    def test_Check(self):
        sql = '''create table TBL_NM(Name text check('FixedName' == Name));'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text check('FixedName' == Name)
);''')
    
    def test_Check_space(self):
        sql = '''create table TBL_NM(Name text check   (   'FixedName'   ==   Name   )   );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Name text check('FixedName' == Name)
);''')
    
    def test_Constraints(self):
        sql = '''create table TBL_NM(
    Id      integer primary key autoincrement unique not null default 0 check (Id<100),
    Name    text);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id   integer primary key autoincrement unique not null default 0 check(Id<100),
    Name text
);''')
    
    def test_ForeignKey(self):
        sql = '''create table TBL_NM(
    Id          integer primary key,
    AccountId   integer,
    foreign key(AccountId) references ParentTable(Id));'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id        integer primary key,
    AccountId integer,
    foreign key(AccountId) references ParentTable(Id)
);''')
    
    def test_quotation(self):
        sql = '''create table "TBL_NM"("Id" integer primary key, "Name" text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table "TBL_NM"(
    "Id"   integer primary key,
    "Name" text    not null
);''')
    
    def test_quotation_escape(self):
        sql = '''create table "T""B""L_NM"("I""d" integer primary key, "N""a""me" text not null);'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table "T""B""L_NM"(
    "I""d"     integer primary key,
    "N""a""me" text    not null
);''')
    
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
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id    integer primary key autoincrement unique not null default 0 check(Id<100),
    Key   integer not null,
    Name  text    not null,
    Rate  real    default 0.5 check(0 <= Tax && (Tax <= 1 || Tax <= 1)),
    Image blob,
    Null  null,
    foreign key(Key) references SomeTable(SomeId)
);''')
    
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
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table """T""BL NM"""(
    "I""d"       integer primary key autoincrement unique not null default 0 check(Id<100),
    """K"" ey""" integer not null,
    "N""""ame"   text    not null check("N""""ame" == 'ABC' || "N""""ame" == 'DEF'),
    """R""ate""" real    default 0.5 check(0 <= Tax && (Tax <= 1 || Tax <= 1)),
    "I""mage"    blob,
    "N""ull"     null,
    MyColumn     text,
    foreign key("""K"" ey""") references "Some ""Table"("Some"" Id")
);''')
    
    def test_const_sequence(self):
        sql = '''create table TBL_NM(
    Id      integer      check ( Id < 100 ) default 0 primary key autoincrement unique not null,
    Key     integer      not    null
    );'''
        c = CreateTableSqlAnalyzer()
        tblnm, coldef = c.Load(sql)
        b = CreateTableSqlBuilder()
        sql = b.Build(tblnm, coldef)
        print(sql)
        self.assertEqual(sql, '''create table TBL_NM(
    Id  integer primary key autoincrement unique not null default 0 check(Id < 100),
    Key integer not null
);''')


if __name__ == '__main__':
    unittest.main()
