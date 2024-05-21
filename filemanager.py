'''
Module in charge of writing the datafiles
'''
import os
import json
from typing import List
from appConstants import TableDescriptor
import re

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
            "lastRowKey":0,

        },
        "tableRegisters":[],
    }
    JSON =  json.dumps(tmp,indent=4)
    with open(f"./files/tables/{tableName}.json",'w') as f:
        f.write(JSON)
        del JSON
    return tmp
def loadTables() -> List[TableDescriptor]:
    '''
    Method to load the tables on the filesystem
    return list of table descriptors
    '''
    tds = []
    for tableJson in os.listdir('./files/tables/'):
        with open(f"./files/tables/{tableJson}", 'r') as f:
            json_t = json.load(f)
            tds.append(TableDescriptor(json_t['tableMetadata'],json_t['tableRegisters']))
    del tableJson, json_t
    return tds