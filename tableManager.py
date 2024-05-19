'''
Module in charge of mannipulating the tables
'''
from filemanager import *
def createTable(args:list):
    #asumes table name as first argument
    name = args.pop(0)
    #next are the column families
    if existsTable(name): raise Exception("Table already exists")
    
    #call the write function
    return newTable(name,args)