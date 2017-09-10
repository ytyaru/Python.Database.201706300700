import os
from databases.Database import Database
#from databases.ChildDatabase import ChildDatabase
from databases.Table import Table
import databases.GitHub.Accounts
class Repositories(Database):
    @property
    def ParentTableType(self): return databases.GitHub.Accounts.Accounts.Accounts
    @property
    def ParentTableKeyColumnName(self): return 'Username'
    class Repositories(Table):
        @property
        def CreateTableSql(self): return """create table Repositories(
    Id          integer primary key,
    IdOnGitHub  integer unique not null,
    Name        text not null,
    Description text,
    Homepage    text,
    CreatedAt   text not null,
    PushedAt    text not null,
    UpdatedAt   text not null,
    CheckedAt   text not null
);
"""

