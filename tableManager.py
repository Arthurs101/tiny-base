'''
Module in charge of manipulating the tables
'''
from typing import List
from filemanager import *
from appConstants import *
import re

global tables
tables = {}

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
    tables[name] = TableDescriptor(tt['tableMetadata'], tt['tableRegisters'])
    return tables[name]

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
        print(f"ERROR, couldn't complete operation, reason \n {e}")

def enableTable(tableName):
    '''
    Enables the table given
    '''
    try:
        tables[tableName].enable()
    except Exception as e:
        print(f"ERROR, couldn't complete operation, reason: \n {e}")

def addRegisters(tableName, args):
    """
    This function adds a register to the table given

    Args:
        tableName (str): Name of the table to add the register to.
        args (list): List containing arguments for register creation:
            - args[0]: Row key for the register.
            - args[1]: Column name in format "columnFamily:columnQualifier".
            - args[2]: Value to be added to the specified column.
    """
    column_family, column_qualifier = args[1].replace("\"", "").replace("'", "").split(':')
    data = {'rowKey': args[0],
            column_family: {
            column_qualifier: args[2].replace('"', '').replace("'", "")
            }
        }
    if tableName in tables:
        tables[tableName].addRegister(data)
    else:
        raise Exception("table not found")

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
    if tableName in tables:
        return tables[tableName].scanSelf()
    else:
        raise ValueError("Table does not exist.")
        return None

def saveTables():
    for _, table in tables.items():
        writeTable(table)
def dropTable(tableName):
    try:
        if tables[tableName].isDisabled():
            del tables[tableName]
            deleteTable(tableName)
        else:
            raise Exception("Table not disabled")
    except KeyError:
        raise KeyError("Table not found")


def dropTables():
    for _ in list(tables.keys()):
        if tables[_].isDisabled():
            del tables[_]
            deleteTable(_)

def deleteFromTable(tableName,rowKey,columnName=None,timestamp=None):
    '''
    Delete cell from table indicating row key and column name
    tableName: str
        name of the table
    rowKey: str
        the row key to delete
    columnName: str
        has to be on the following format columnFamily:columnQualifier
        carefull, it may be optional, but not specified will delete the entire row
        if the columnQualifier is not specified will delete all the info on the column family
    timestamp: int
        specifies the timestamp to delete
    '''
    if tableName not in tables:
        raise Exception('table not found')
    tables[tableName].deleteRegister(rowKey,columnName=None,timestamp=None)
    return "succes"


def alterTable(tableName, operation, column_name, column_type=None):
    '''
    Alters the structure of a table
    '''
    if tableName not in tables:
        raise ValueError("Table does not exist.")
    
    columnFamilies = tables[tableName].columnFamilies
    
    if operation == 'ADD':
        if column_name in columnFamilies:
            raise ValueError("Column already exists.")
        columnFamilies[column_name] = column_type
    
    elif operation == 'DROP':
        if column_name not in columnFamilies:
            raise ValueError("Column does not exist.")
        del columnFamilies[column_name]
        for register, _ in tables[tableName].registers.items():
            del tables[tableName].registers[register][column_name]
    elif operation == 'MODIFY':
        if column_name not in columnFamilies:
            raise ValueError("Column does not exist.")
        columnFamilies[column_name] = column_type
    
    else:
        raise ValueError("Invalid operation.")

def describeTable(tableName):
    '''
    Describes the structure of a table
    '''
    if tableName not in tables:
        raise ValueError("Table does not exist.")
    
    columnFamilies = tables[tableName].columnFamilies
    return columnFamilies

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
        return len(tables[tableName].registers)
    except KeyError:
        print("Table not found")
        return None

tables = loadTables()
