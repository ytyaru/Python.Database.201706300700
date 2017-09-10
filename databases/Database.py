from abc import ABCMeta, abstractmethod
import pathlib
import dataset
import inspect
import importlib
import databases.Table
class Database():
    def __init__(self):
        self.__path = None
        self.__tables = None
        self.__filename = None
    
    # DBファイルがなければ作成。テーブルがなければ作成。dataset.connect()の戻り値を返す。
    def Initialize(self, dir_path:pathlib.PurePath, prefix=None):
        self.__dir_path = dir_path
        self.__prefix = prefix
        self.__dir_path = pathlib.Path(self.__dir_path).resolve()
        self.__dir_path.mkdir(parents=True, exist_ok=True)
        if not self.__dir_path.is_dir(): raise Exception('引数dir_pathにはディレクトリのパスを指定してください。: {0}'.format(self.__dir_path))
        self.__CreateTableInstances()

    # 本クラス継承クラスの定義内でTable継承クラスを定義するとそのインスタンスを生成する。
    def __CreateTableInstances(self):
        self.__tables = []
        classes = inspect.getmembers(self, inspect.isclass)
        for c in classes:
            name, typ = c
#            print(name, typ)
            if 'ParentTableType' == name: continue
            if 'Table' == name and 'databases.Table' == typ.__module__: continue
            if issubclass(typ, databases.Table.Table): self.__tables.append(typ())
    
    @property
    def Tables(self): return self.__tables
#    @property
#    def Path(self): return self.__path
    @property
    def DirectoryPath(self): return self.__dir_path
#    @property
#    def Filename(self): return self.__filename
    @property
    def Extension(self): return 'sqlite3'
#    @property
#    def DatasetDb(self): return self.__db
    
    @property
    def ParentTableType(self): return None
    @property
    def ParentTableKeyColumnName(self): return None    
    
    def LoadChildDbFilenames(self):
        if None is self.ParentTableType: return None
        self.__child_db_filenames = []
        for parent_datasetDb in self.__GetParentDb():
#            print('ppppppppppppppppppppppppppppppppppppppppppppp', parent_datasetDb[self.ParentTableType.__name__].count())
            for record in parent_datasetDb[self.ParentTableType.__name__].find():
                prefix = ''  if None is self.__prefix else self.__prefix
                self.__child_db_filenames.append(prefix + self.__class__.__name__ + '.' + record[self.ParentTableKeyColumnName] + '.' + self.Extension)
        return self.__child_db_filenames
    
    def __LoadChildDbs(self):
        for parent_datasetDb in self.__GetParentDb():
            for record in parent_datasetDb[self.ParentTableType.__name__].find():
                prefix = ''  if None is self.__prefix else self.__prefix
                child_db = copy.copy(self) # Database型
                child_db.__file_name = prefix + self.__class__.__name__ + '.' + record[self.ParentTableKeyColumnName] + '.' + self.Extension
                child_db.__path = self.__dir_path / self.__file_name
                child_db.__db = dataset.conntect('sqlite:///' + str(child_db.__path))
                yield child_db
    
    def __GetParentDb(self):
        for c in inspect.getmembers(importlib.import_module(self.ParentTableType.__module__), inspect.isclass):
            name, typ = c
            if 'Database' == name and 'databases.Database' == typ.__module__: continue # 継承クラスの実装ファイルで「from 
            if not issubclass(typ, databases.Database.Database): continue
            db = typ()
            prefix = typ.__module__.replace('databases.', '')
            if 0 < len(prefix): prefix = prefix[:prefix.rindex('.')+1]
            db.Initialize(self.__dir_path, prefix)
            file_path = self.__dir_path / (prefix + db.__class__.__name__ + '.' + self.Extension)
            datasetDb = dataset.connect('sqlite:///' + str(file_path))
            yield datasetDb
