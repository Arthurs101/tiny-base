'''
Module for classes declarations,constants used throughout the application
'''
#object used to interact with a table:
class TableStatusException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(message)
class ActionOnDisavledTableException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(message)

class TableDescriptor(object):
    '''
    Object oriented to interact with as a table
    handlight inserts, searchs , updates and deletes
    also for handling the metadata
    '''
    def __init__(self,metadata,registers):
        self.is_enabled = metadata['isActive']
        self.name = metadata['tableName']
        self.columnFamilies = metadata['columnFamilies']
        self.lastRowKeter = metadata['lastRowKey']
        self.registers = registers
    def __str__(self):
        '''
        returns its information as HTable format
        ROW         Column+cell
        value here  column=family:column timestamp=number value=value
        '''
    def isEnabled(self):
        return self.is_enabled
    def disable(self):
        if self.is_enabled:
            self.is_enabled = False
        else:
            raise TableStatusException("can't disable an already disabled table")
    def enable(self):
        if not self.is_enabled:
            self.is_enabled = True
        else:
            raise TableStatusException("can't enable an already enable table")
    def addRegister(self,args):
        pass