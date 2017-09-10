from abc import ABCMeta, abstractmethod
import os
class Table:
    def __init__(self):
        pass
    @property
    def Name(self): return self.__class__.__name__
    @property
    @abstractmethod
    def CreateTableSql(self): pass
    @property
    def InitializeRecords(self): return None
    @property
    def Tsv(self): return None

