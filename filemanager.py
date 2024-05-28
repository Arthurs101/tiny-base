'''
Module in charge of writing the datafiles
'''
import os
import json

from appConstants import TableDescriptor
import re

def ensure_directory_exists(path):
    '''
    Creates the directory if it does not exist
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def existsTable(tableName):
    '''
    checks if table exists on the filesystem
    '''
    return os.path.exists('./files/tables/'+tableName+'.json')

def newTable(tableName,families):
    '''
    Writes a new table file into the filesystem
    '''
    tmp =  {
        "tableMetadata":{
            "tableName":tableName,
            "isActive": True,
            "columnFamilies":{family:[] for family in families},
            "versions":3
        },
        "tableRegisters":{},
    }
    JSON =  json.dumps(tmp,indent=4)
    with open(f"./files/tables/{tableName}.json",'w') as f:
        f.write(JSON)
        del JSON
    return tmp

def loadTables() -> dict:
    '''
    Method to load the tables on the filesystem
    return list of table descriptors
    '''
    tds = {}
    for tableJson in os.listdir('./files/tables/'):
        with open(f"./files/tables/{tableJson}", 'r') as f:
            json_t = json.load(f)
            tds[json_t['tableMetadata']['tableName']] = TableDescriptor(json_t['tableMetadata'],json_t['tableRegisters'])
    return tds

def writeTable(table):
    'writes table descriptor into a file'
    
    JSON =  json.dumps(table.dicTable(),indent=4)
    with open(f"./files/tables/{table.name}.json",'w') as f:
        f.write(JSON)
        del JSON

def deleteTable(tableName):
    '''
    Deletes a table from filesystem
    '''
    os.remove(f"./files/tables/{tableName}.json")


#always ensure directory exists
#before any call
ensure_directory_exists('./files/tables/')  