create table Parent(
    Id      integer,
    Name    text
);
create table Child(
    Id          integer,
    ParentId    integer,
    Name        text,
    foreign key(Id) references Parent (Id)
);
