class Column:
    def __init__(self, name:str, typ:Column.Type, *args):
        self.__name = name
        self.__type = typ
        self.__constraints = []
        for arg in args:
            if not isinstance(arg, Column.Constraint): continue
            self.__constraints.append(arg)
    @property
    def Name(self): return self.__name
    @property
    def Type(self): return self.__type
    @property
    def Constraints(self): return self.__type

    class Type: pass
    class Text(Type): pass
    class Integer(Type): pass
    class Real(Type): pass
    class Blob(Type): pass
    class Null(Type): pass
    
    class Constraint: pass
    class Default(Constraint):
        def __init__(self, value):
            self.__value = value
        @property
        def Value(self): return self.__value
    class Check(Constraint):
        def __init__(self, expression_string):
            self.__expression_string = expression_string
        @property
        def ExpressionString(self): return self.__expression_string
    class NotNull(Constraint):
        pass
    class Unique(Constraint):
        pass
    class PrimaryKey(Constraint): # autoincrement
        def __init__(self, is_autoincrement=False):
            self.__is_autoincrement = is_autoincrement
        @property
        def IsAutoincrement(self): return self.__is_autoincrement
    class ForeignKey(Constraint):
        def __init__(self, references_table_type, references_column_name):
            self.__references_table_type = references_table_type
            self.__references_column_name = references_column_name
        @property
        def ReferencesTableType(self): return self.__references_table_type
        @property
        def ReferencesColumnName(self): return self.__references_column_name

