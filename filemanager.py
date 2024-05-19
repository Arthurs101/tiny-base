'''
Module in charge of writing the datafiles
'''
import os
import json
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