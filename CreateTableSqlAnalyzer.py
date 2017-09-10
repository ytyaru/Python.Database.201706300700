import re
class CreateTableSqlAnalyzer:
    def __init__(self):
        self.__columns = [] # [{'name': str, 'type': type, 'constraints': list}, ...]
        self.__re_create_table = re.compile(r'create[ ]+table', re.IGNORECASE)
        self.__re_autoincrement = re.compile(r'autoincrement', re.IGNORECASE)
        self.__re_not_null = re.compile(r'not[ ]+null', re.IGNORECASE)
        self.__re_unique = re.compile(r'unique', re.IGNORECASE)
        self.__re_primary_key = re.compile(r'primary[ ]+key', re.IGNORECASE)
        self.__re_default = re.compile(r'default', re.IGNORECASE)
#        self.__re_default = re.compile(r"default[\s]+(?P<value>.+)[\s]*", re.IGNORECASE) # 後続の定義まで抜き出してしまう
#        self.__re_default = re.compile(r"default[\s]+[']*(?P<value>.+)[']*", re.IGNORECASE)
#        self.__re_default = re.compile(r"default[\s]+[']*(?P<value>.+)[']*[\s]", re.IGNORECASE)
        self.__re_check = re.compile(r'check[\s]*\((?P<expression>.+)\)', re.IGNORECASE)
        self.__re_foreign_key = re.compile(r'foreign[\s]+key[\s]*\((?P<key>.+)\)[\s]+references[\s]+(?P<table>.+)[\s]*\((?P<column>.+)\)')

    """
    [{'name':'', 'type':'', 'constraints': {'primary_key': true, 'autoincrement': true, 'unique': true, 'not_null': true, 'default': 'value', 'check': 'v < 100', 'foreign_key': {'table': '', 'column': ''} }}]
    """    
    def Load(self, sql):
        self.__name, sql = self.__GetTableName(sql)
        sql = self.__GetEnd(sql)
        sql = self.__AnalizeInnerDefine(sql)
        return self.__name, self.__columns
    
    @property
    def ColumnDefines(self): return self.__columns
    
    def __GetTableName(self, sql):
        table_name = sql[:sql.index('(')]
        table_name = re.sub(self.__re_create_table, '', table_name)
        table_name = table_name.strip()
        if len(table_name) <= 0: raise Exception('テーブル名がありません。"create table SomeName(...);"のように1文字以上の名前を付けて下さい。')
        return table_name.strip(), sql[sql.index('(') + 1:]
    
    def __GetEnd(self, sql):
        sql = sql[:sql.rindex(';')]
        sql = sql[:sql.rindex(')')]
        return sql

    def __AnalizeInnerDefine(self, sql):
        self.__columns.clear()
        for column in sql.split(','):
            column = column.strip()
            try: self.__GetColumns(column)
            except (CreateTableSqlAnalyzer.NotColumnDataTypeError, CreateTableSqlAnalyzer.NotExsistColumnDataTypeError):
                coldef = self.__GetForeignKey(column)
                for forkey in coldef:
                    for col in self.__columns:
                        print(forkey, col)
                        if forkey['name'] == col['name']:
                            if 'constraints' in col: col['constraints'].update(forkey['constraints'])
                            else: col['constraints'] = forkey['constraints']
#                for col in self.__columns:
#                    if coldef['name'] == col['name']:
#                        if 'constraints' in col: col['constraints'].update(coldef['constraints'])
#                        else: col['constraints'] = coldef['constraints']
            except: raise
    
    def __GetColumns(self, col_def):
        name, defines = self.__GetNameAndOthers(col_def)
#        print(col_def)
#        print(name, defines)
        if len(defines) < 1: raise CreateTableSqlAnalyzer.NotExsistColumnDataTypeError()
#        if len(defines) < 1: raise Exception('カラム定義は"名前 型 制約1 制約2 制約3 ... ,"の書式で記入して下さい。')
        if not self.__IsValidType(defines[0]): raise CreateTableSqlAnalyzer.NotColumnDataTypeError()
        column = {}
        column.update({'name': name})
        column.update({'type': defines[0]})
        if 1 < len(defines): column.update({'constraints': self.__IsValidConstraints(defines[1:])})
        self.__columns.append(column)

    def __GetNameAndOthers(self, col_def):
        if 0 < col_def.count('"'):
            later = "" + col_def
            name, later = self.__GetQuotationInnserStr(later[later.index('"'):], '"')
            defines = [e for e in later.split(' ') if '' != e.strip()]
            return '"' + name + '"', defines
        else:        
            defines = [e for e in col_def.split(' ') if '' != e.strip()]
            return defines[0], defines[1:]
    
    class NotExsistColumnDataTypeError(Exception):
        def __init__(self): self.message = 'カラム定義は"名前 型 制約1 制約2 制約3 ... ,"の書式で記入して下さい。'
    class NotColumnDataTypeError(Exception):
        def __init__(self): self.message = 'カラムの型は "text", "integer", "real", "blob", "null" のいずれかを記入して下さい。'
    
    def __IsValidType(self, column_type_str):
        t = column_type_str.lower()
        if t == 'text' or t == 'integer' or t == 'real' or t == 'blob' or t == 'null': return True
        else: return False
    
    def __IsValidConstraints(self, constraints_defines):
        constraints = {}
        const_str = ' '.join(constraints_defines)
        flag, const_str = self.__GetFlag(const_str, self.__re_autoincrement)
        if flag: constraints.update({'autoincrement': flag})
        flag, const_str = self.__GetFlag(const_str, self.__re_not_null)
        if flag: constraints.update({'not_null': flag})
        flag, const_str = self.__GetFlag(const_str, self.__re_unique)
        if flag: constraints.update({'unique': flag})
        flag, const_str = self.__GetFlag(const_str, self.__re_primary_key)
        if flag: constraints.update({'primary_key': flag})
        value, const_str = self.__GetCheck(const_str)
        if value: constraints.update({'check': value})
        value, const_str = self.__GetDefault(const_str)
        if value: constraints.update({'default': value})
        
        return constraints

    def __GetFlag(self, const_str, reg):
        if None is reg.search(const_str): return False, const_str
        else:
            const_str = re.sub(reg, '', const_str)
            return True, const_str

    """
    def __GetDefault(self, const_str):
        match = self.__re_default.search(const_str)
        if None is match: return None, const_str
        else: return match.group('value').strip(), re.sub(self.__re_default, '', const_str)
    """
    def __GetDefault(self, const_str):
        match = self.__re_default.search(const_str)
        if None is match: return None, const_str
        else:
            const_str = re.sub(self.__re_default, '', const_str).strip()
            return self.__GetDefineValue(const_str)
    
    # スペースで区切ろうとしてもダメ。文字列'...'の中でスペースが使われる場合もあるから。default 'default value'のように。
    # https://www.dbonline.jp/sqlite/type/index4.html
    # SQLiteは文字列の場合シングルクォーテーション、識別子の場合はダブルクォーテーションで囲う。
    # default制約で文字列を指定するときもシングルクォーテーションと思われる。
    # ''内で'をエスケープするときは、''とする。2回続けて書く。
    # 数値の場合: default 0
    # 文字の場合: default 'test value'
    # 文字の場合: default 'I''am andy.'
    def __GetDefineValue(self, default_later):
        later_str = default_later.strip()
        # スペースがないならdefault_later内にはもうdefault以外の制約定義がないと判断できる（各制約はスペース区切りだから）
        # 'がないなら数値定数である。スペースを除去して返す
        if 0 == default_later.count(' '):
            const_str = default_later.replace(default_later, '')
            if 0 == default_later.count("'"):
                return default_later.strip(), const_str # default 123
            elif default_later.startswith("'") and default_later.endswith("'"):
                return default_later[default_later.index("'"):default_later.rindex("'")+1], const_str # default 'abc'
        else:
            const_str = default_later[default_later.index(' '):]
            default_value = default_later[:default_later.index(' ')]
            if 0 == default_later.count("'"): return default_value, const_str # default 123 check(...)
            inner, default_later = self.__GetQuotationInnserStr(default_later, "'") # default 'I'am andy.' check(...)
            return "'" + inner + "'", default_later
        raise Exception("Default値の取得に失敗しました。:", default_later)
    
    """
    SQLite3における'または"内の文字列を取得する。
    'は文字列リテラル値に用いる。defautl 'val ue', where 'I''am andy' == col, など。
    "は定義名に使う。 create table "TBL NM"("I""d" integer); など
    'と"はその中で2つ続けて記入するとその文字自体を表す。（'"のエスケープ）
    """
    def __GetQuotationInnserStr(self, define_later, quote):
        if None is quote or not ("'" == quote or '"' == quote): raise Exception('quoteは''または"のいずれかを指定して下さい。')
        is_escape = False
        tmp_val = define_later[define_later.index(quote)+1:]
        for i, char in enumerate(tmp_val):
            if is_escape: is_escape = False; continue
            if quote == char:
                if i+1 < len(tmp_val)-1 and quote == tmp_val[i+1]: is_escape=True; continue # ''で'をエスケープするので囲い数としてカウントしない
                return tmp_val[define_later.index(quote):i], define_later[i+2:]
        raise Exception(quote + "の数が合っていない可能性があります。:", define_later)
    
    def __GetCheck(self, const_str):
        match = self.__re_check.search(const_str)
        if None is match: return None, const_str
        else: return match.group('expression').strip(), re.sub(self.__re_check, '', const_str)
    
    def __GetForeignKey(self, const_str):
        m = self.__re_foreign_key.search(const_str)
        if None is m: return False, const_str
        else:
#            key = m.group('key').strip()
#            table = m.group('table').strip()
#            column = m.group('column').strip()
#            return {'name': key, 'constraints': {'foreign_key': {'table': table, 'column': column}}}
            keys = [v.strip() for v in m.group('key').strip().split(',')]
            table = m.group('table').strip()
            columns = [v.strip() for v in m.group('column').strip().split(',')]
            if len(keys) != len(columns): raise Exception('外部キーと参照キーの数が一致しません。:{0}'.format(const_str))
            cols = []
            for i, key in enumerate(keys):
                cols.append({'name': key, 'constraints': {'foreign_key': {'table': table, 'column': columns[i]}}})
            return cols
#            return {'name': key, 'constraints': {'foreign_key': {'table': table, 'columns': column}}}

