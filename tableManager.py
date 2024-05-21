'''
Module in charge of mannipulating the tables
'''
from typing import List
from filemanager import *
from appConstants import *

global tables
tables = []

def createTable(args:list):
    #asumes table name as first argument
    name = args.pop(0)
    #next are the column families
    if existsTable(name): raise Exception("Table already exists")
    
    #call the write function
    tt =  newTable(name,args)
    return TableDescriptor(tt['tableMetadata'],tt['tableRegisters'])
def listTable(rgx_name=None) -> List[str]:
    '''
    Method for de DDL instruction of list
    Returns a list object of strings representing the table names
    ...
    '''
    return [table.name for table in tables] if not rgx_name else [table.name for table in tables if re.search(rf"{rgx_name}", table.name)]
    
if __name__ == '__main__':
    tables = loadTables()
