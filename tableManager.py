'''
Module in charge of manipulating the tables
'''
from typing import List
from filemanager import *
from appConstants import *
import re

global tables
tables = {}

class TableDescriptor:
    def __init__(self, metadata, registers):
        self.metadata = metadata
        self.registers = registers

def createTable(args: list):
    '''
    returns a table descriptor object 
    raises Exception if table already exists
    '''
    # assumes table name as first argument
    name = args.pop(0)
    name = name.rstrip().strip().replace('"', '').replace("'", '')
    # next are the column families
    if existsTable(name): raise Exception("Table already exists")
    
    # call the write function
    args = [arg.rstrip().strip().replace('"', '').replace("'", '') for arg in args]

    tt = newTable(name, args)
    return TableDescriptor(tt['tableMetadata'], tt['tableRegisters'])

def listTables(rgx_name=None) -> List[str]:
    '''
    Method for the DDL instruction of list
    Returns a list object of strings representing the table names
    '''
    return [table.name for table in list(tables.values())] if not rgx_name else [table.name for table in list(tables.values()) if re.search(rf"{rgx_name}", table.name)]

def disableTable(tableName):
    '''
    Disables the table given
    '''
    try:
        tables[tableName].disable()
    except Exception as e:
        print(f"ERROR, couldn't complete operation, reason \n {e.message}")

def enableTable(tableName):
    '''
    Enables the table given
    '''
    try:
        tables[tableName].enable()
    except Exception as e:
        print(f"ERROR, couldn't complete operation, reason: \n {e.message}")

def addRegisters(tableName, args):
    data = {'rowKey': args[0],
            f'{args[1].split(":")[0].replace('"', '').replace("'", "")}': {
            f'{args[1].split(":")[1].replace('"', '').replace("'", "")}': args[2].replace('"', '').replace("'", "")
            }
    }
    if tableName in tables:
        tables[tableName].addRegister(data)
    else:
        print("Table not found")

def getRegister(tableName, rowKey, versions=1, column=None):
    '''
    Returns the register for the given table using a row key
    '''
    try:
        tmp = tables[tableName].getRegister(rowKey)
        if column:
            colFamily, columnQualifier = column.split(':')
            tmp = {colFamily: {columnQualifier: tmp[colFamily][columnQualifier]}}
        # reduce into the amount of versions
        for columnFamily, columnQualifier in tmp.items():
            # go from last to first using the amount of versions
            for cell, timestamps in columnQualifier.items():
                cell_versions = list(timestamps.keys())
                cell_versions.reverse()
                if len(cell_versions) > versions:
                    cell_versions = cell_versions[:versions]
                latest_timestamps = {tt: timestamps[tt] for tt in cell_versions}
                columnQualifier[cell] = latest_timestamps
            tmp[columnFamily] = columnQualifier
        return tmp
    except KeyError:
        print("Table or row not found")
        return None

def scanTable(tableName):
    print(tables[tableName])

def saveTables():
    for _, table in tables.items():
        writeTable(table)

def dropTable(tableName):
    try:
        del tables[tableName]
        deleteTable(tableName)
    except KeyError:
        print("Table not found")

def dropTables():
    for _ in list(tables.keys()):
        del tables[_]
        deleteTable(_)

def alterTable(tableName, operation, column_name, column_type=None):
    '''
    Alters the structure of a table
    '''
    if tableName not in tables:
        raise ValueError("Table does not exist.")
    
    schema = tables[tableName].metadata
    
    if operation == 'ADD':
        if column_name in schema:
            raise ValueError("Column already exists.")
        schema[column_name] = column_type
    
    elif operation == 'DROP':
        if column_name not in schema:
            raise ValueError("Column does not exist.")
        del schema[column_name]
    
    elif operation == 'MODIFY':
        if column_name not in schema:
            raise ValueError("Column does not exist.")
        schema[column_name] = column_type
    
    else:
        raise ValueError("Invalid operation.")

def describeTable(tableName):
    '''
    Describes the structure of a table
    '''
    if tableName not in tables:
        raise ValueError("Table does not exist.")
    
    schema = tables[tableName].metadata
    return schema

def truncateTable(tableName):
    '''
    Truncates all data in the table
    '''
    if tableName in tables:
        tables[tableName].registers.clear()
    else:
        print("Table not found")

def count(tableName):
    '''
    Returns the number of rows in the table
    '''
    try:
        return tables[tableName].size()
    except KeyError:
        print("Table not found")
        return None

tables = loadTables()
