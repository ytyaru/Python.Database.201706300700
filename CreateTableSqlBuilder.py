class CreateTableSqlBuilder:
    def __init__(self):
        self.__indent = 4
        
    def Build(self, table_name, columns):
        return '''create table {0}(
{1}
);'''.format(table_name, self.__BuildColumnDefine(columns))
        
    def __BuildColumnDefine(self, columns):
        print(columns)
        col_def = ''
        nmlen = self.__GetNamesMaxLen(columns)
        tylen = self.__GetTypesMaxLen(columns)
        for c in columns:
            tmp_def = c['name'].ljust(nmlen) + ' ' + c['type'].ljust(tylen) + self.__BuildConstraints(c['constraints'] if 'constraints' in c else None)
            tmp_def = ' '*self.__indent + tmp_def.strip() + ',' + '\n'
            col_def += tmp_def
        foreign_def = self.__BuildForeignKeys(columns)
        if '' == foreign_def: col_def = col_def[:-1] # ,を削除する
        else: col_def += foreign_def        
        col_def = col_def[:-1] # 末尾の
        return col_def
    
    def __GetNamesMaxLen(self, columns):
        return len(max([v for c in columns for k,v in c.items() if 'name' == k], key=lambda x: len(x)))
    
    def __GetTypesMaxLen(self, columns):
        return len(max([v for c in columns for k,v in c.items() if 'type' == k], key=lambda x: len(x)))
    
    def __BuildConstraints(self, constraints):
        if None is constraints: return ''
        const_def = ''
        if 'primary_key' in constraints: const_def += ' primary key'
        if 'autoincrement' in constraints: const_def += ' autoincrement'
        if 'unique' in constraints: const_def += ' unique'
        if 'not_null' in constraints: const_def += ' not null'
        if 'default' in constraints: const_def += ' default ' + constraints['default']
        if 'check' in constraints: const_def += ' check(' + constraints['check'] + ')'
        return const_def
    
    def __BuildForeignKeys(self, columns):
        """
        for c in columns:
            if 'constraints' in c:
                if 'foreign_key' in c['constraints']:
        """
        foreigns = {c['name']:c['constraints']['foreign_key'] for c in columns if 'constraints' in c and 'foreign_key' in c['constraints']}
        if {} == foreigns: return ''
        print(list(foreigns.keys())[0])
        table_name = foreigns[list(foreigns.keys())[0]]['table']
        return ' '*self.__indent + 'foreign key({0}) references {1}({2}),'.format(
                ', '.join(foreigns.keys()), 
                table_name,
                ', '.join([v['column'] for k,v in foreigns.items()]))

