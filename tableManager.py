'''
Module in charge of mannipulating the tables
'''
from typing import List
from filemanager import *
from appConstants import *

global tables
tables = {}

def createTable(args:list):
    '''
    returns a table descriptor object 
    raises Exception if table already exists
    '''
    #asumes table name as first argument
    name = args.pop(0)
    name = name.rstrip().strip().replace('"','').replace("'",'')
    #next are the column families
    if existsTable(name): raise Exception("Table already exists")
    
    #call the write function
    args = [arg.rstrip().strip().replace('"','').replace("'",'') for arg in args]

    tt =  newTable(name,args)
    return TableDescriptor(tt['tableMetadata'],tt['tableRegisters'])
def listTables(rgx_name=None) -> List[str]:
    '''
    Method for de DDL instruction of list
    Returns a list object of strings representing the table names
    ...
    '''
    return [table.name for table in list(tables.values())] if not rgx_name else [table.name for table in list(tables.values()) if re.search(rf"{rgx_name}", table.name)]

def disableTable(tableName):
    try:
        tables[tableName].disable()
    except Exception as e:
        print(f"ERROR, couldn complete operation, reason \n {e.message}")

def enableTable(tableName):
    try:
        tables[tableName].enable()
    except Exception as e:
        print(f"ERROR, couldn complete operation, reason: \n {e.message}")
def addRegisters(tableName,data):
    print("table name" + tableName)
    print("args" + "".join(data))
    pass
def scanTable(tableName):
    print(tables[tableName])

tables = loadTables()