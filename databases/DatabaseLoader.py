from abc import ABCMeta, abstractmethod
import os
import pathlib
import importlib
import dataset
import inspect
import copy
import databases.Table
class DatabaseLoader(metaclass=ABCMeta):
    def __init__(self, path_dir_root):
        self.__path_dir_root = path_dir_root
        self.Initialize()
    
    @property
    def Databases(self): return self.__databases

    """
    DB定義pyファイルを探す。インスタンス化する。Initialize()する(DB,Table作成)。dataset.connect()する。
    """
    def Initialize(self):
        self.__databases = {}
        # https://docs.python.jp/3/library/inspect.html
        self.__this_path = pathlib.PurePath(importlib.import_module(self.__module__).__file__) # databases.DatabaseLoader.__file__
        print(self.__this_path)
        db_root_path = self.__this_path.parent / '..' / 'res'
        for directory in self.__GetLoadTargetDirs():
            for module in self.__LoadModules(directory):
                for type_db in self.__CreateDatabaseInstances(module):
                    db = type_db()                    
                    filename_prefix = self.__ClassToDbNamePrefix(type_db)
                    if None is not db.ParentTableType and None is not db.ParentTableKeyColumnName:
                        db.Initialize(db_root_path, prefix=filename_prefix)
                        print(db, 'db.LoadChildDbFilenames():', db.LoadChildDbFilenames())
                        for file_name in db.LoadChildDbFilenames():
                            # DBファイル作成
                            dbc = DatabaseLoader.DbCreator(db_root_path / file_name)
                            dbc.Create(db)
                            # DBプロパティ設定
                            childdb = copy.copy(db)
                            childdb.__dict__['Filename'] = file_name
                            childdb.__dict__['Path'] = db_root_path / file_name
                            childdb.__dict__['DatasetDb'] = dataset.connect('sqlite:///' + str(childdb.Path))
                            self.__databases.update({childdb.Filename: childdb})
                    else:
                        db.Initialize(db_root_path, prefix=filename_prefix)
                        file_name = filename_prefix + db.__class__.__name__ + '.' + db.Extension if None is not filename_prefix else self.__target_db.__class__.__name__ + '.' + db.Extension
                        path = db_root_path / file_name
                        dbc = DatabaseLoader.DbCreator(path)
                        dbc.Create(db)
                        db.__dict__['Filename'] = file_name
                        db.__dict__['Path'] = path
                        db.__dict__['DatasetDb'] = dataset.connect('sqlite:///' + str(db.Path))
                        # ファイル名から拡張子を省いたkey名で登録する
                        self.__databases.update({db.Filename: db})
        
    # Database検索ディレクトリを抽出する
    def __GetLoadTargetDirs(self):
        p = pathlib.Path(self.__this_path.parent)
        for child in p.iterdir():
            if not child.is_dir(): continue
            yield child
        
    # pyファイルをモジュールとして読み込む
    def __LoadModules(self, target_dir):
        # https://docs.python.jp/3/library/pathlib.html
        for child in target_dir.glob('**/*.py'):
            module = importlib.import_module(self.__PathToImport(child))
            yield module
    
    def __PathToImport(self, path):
        rel_path = path.relative_to(self.__path_dir_root)
        module_name = str(rel_path.with_suffix('')).replace('/', '.')
        return module_name
    
    def __ClassToDbNamePrefix(self, db_class):
        prefix = db_class.__module__.replace('databases.', '')
        return prefix[:prefix.rindex('.')+1]
    
    def __CreateDatabaseInstances(self, module):
        classes = inspect.getmembers(module, inspect.isclass)
        for c in classes:
            name, typ = c
            if 'Database' == name and 'databases.Database' == typ.__module__: continue # 継承クラスの実装ファイルで「from databases.Database import Database」とするとメンバに含まれる
            if not issubclass(typ, databases.Database.Database): continue
            yield typ

    class DbCreator:
        def __init__(self, db_path:pathlib.PurePath):
            self.__db_path = pathlib.Path(db_path).resolve()
        def Create(self, db):
            if not self.__db_path.is_file():
                with open(self.__db_path, mode='w', encoding='utf-8') as f: f.write('')
            print('*********{0}'.format(self.__db_path))
            datasetDb = dataset.connect('sqlite:///' + str(self.__db_path))
            self.__CreateTables(db, datasetDb)
            return datasetDb
        def __CreateTables(self, db, datasetDb):
            for table in db.Tables:
                if table.Name not in datasetDb.tables:
                    print('***', db, datasetDb, table)
                    datasetDb.query(table.CreateTableSql)
                    if None is not table.InitializeRecords and 0 == datasetDb[table.Name].count():
                        try:
                            datasetDb.begin()
                            for record in table.InitializeRecords:
                                datasetDb[table.Name].insert(record)
                            datasetDb.commit()
                        except:
                            datasetDb.rollback()
                            raise
