import os
from databases.Database import Database
from databases.Table import Table
class Accounts(Database):
    class Accounts(Table):
        @property
        def CreateTableSql(self): return """create table Accounts(
        Id          integer primary key,
        Username    text not null,
        MailAddress text unique not null,
        Password    text not null,
        CreatedAt   text,
        UpdatedAt   text
    );
"""
        @property
        def InitializeRecords(self): return [
            {'Id': 0, 'Username': 'user0', 'MailAddress': 'mail0', 'Password': 'pass0', 'CreatedAt': '2000/01/01 00:00:00', 'UpdatedAt': '2000/01/01 00:00:00'},
            {'Id': 1, 'Username': 'user1', 'MailAddress': 'mail1', 'Password': 'pass1', 'CreatedAt': '2000/01/02 00:00:00', 'UpdatedAt': '2000/01/01 00:00:00'},
            {'Id': 2, 'Username': 'user2', 'MailAddress': 'mail2', 'Password': 'pass2', 'CreatedAt': '2000/01/03 00:00:00', 'UpdatedAt': '2000/01/01 00:00:00'},
            {'Id': 3, 'Username': 'user3', 'MailAddress': 'mail3', 'Password': 'pass3', 'CreatedAt': '2000/01/04 00:00:00', 'UpdatedAt': '2000/01/01 00:00:00'},
        ]
        @property
        def Tsv(self): return """0	user0	mail0	pass0	2000/01/01 00:00:00	2000/01/01 00:00:00
0	user0	mail0	pass0	2000/01/01 00:00:00	2000/01/01 00:00:00
1	user1	mail1	pass1	2000/01/02 00:00:00	2000/01/01 00:00:00
2	user2	mail2	pass2	2000/01/03 00:00:00	2000/01/01 00:00:00
3	user3	mail3	pass3	2000/01/04 00:00:00	2000/01/01 00:00:00
"""

