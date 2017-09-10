import os
from databases.Database import Database
from databases.Table import Table
class Apis(Database):
    class Apis(Table):
        @property
        def CreateTableSql(self): return """create table Apis(
    Id                  integer primary key,
    Name                text unique not null,
    HttpMethod          text not null check(HttpMethod='GET' or HttpMethod='POST' or HttpMethod='DELETE' or HttpMethod='PATCH' or HttpMethod='HEAD' or HttpMethod='PUT' or HttpMethod='OPTIONS' or HttpMethod='TRACE' or HttpMethod='LINK' or HttpMethod='UNLINK'),
    Endpoint            text not null,
    AuthMethods         text not null,
    Grants              text,
    SuccessStatusCode   integer check(100<=SuccessStatusCode and SuccessStatusCode<=599),
    DocumentUrl         text
);
    """

        
