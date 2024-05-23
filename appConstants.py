'''
Module for classes declarations,constants used throughout the application
'''
#object used to interact with a table:
from datetime import datetime
import calendar

class TableStatusException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(message)
class ActionOnStateException(Exception):
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
        self.versions = metadata['versions']
        self.registers = registers
    def __str__(self):
        '''
        returns its information as HTable format
        ROW         Column+cell
        value here  column=family:column timestamp=number value=value
        '''
        str_self = "ROW\t\tCOLUMN+CELL\n"
        for row , data in self.registers.items():
            for col_family , column in data.items():
                for cell,timestamps in column.items():
                    last = list(timestamps.keys())[-1]
                    str_self += f"{row}\t\tcolumn={col_family}:{cell}, {last.replace("timestamp","timestamp=")} , value={timestamps[last]}\n"
        return str_self

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
    def addRegister(self,data):
        '''
        add a reginter to the table
        recevive a dictionary for  aregister 
        {'rowKey': data,
          'column_family':{
          'column':value
          }
        }
        '''
        
        if self.is_enabled:
            for colFamily in [_ for _ in list(data.keys()) if _ != 'rowKey']:
                if colFamily in self.columnFamilies:
                    for column, value in data[colFamily].items():
                        if data['rowKey'] not in self.registers:
                            self.registers[data['rowKey']] = {colFamily:{column:{f"timestamp{calendar.timegm(datetime.now().timetuple())}":value}}}
                        else:
                            self.registers[data['rowKey']][colFamily][column][f"timestamp{calendar.timegm(datetime.now().timetuple())}"]= value
                else:
                    raise Exception("Column family not found in table")
            pass
        else:
            raise ActionOnStateException('Table is not enabled')
        pass
    def dicTable(self):
        '''
        returns a dictionary containing all the information 
        of the table
        useful for writing it into a json file
        '''
        tmp =  {
        "tableMetadata":{
            "tableName":self.name,
            "isActive": self.is_enabled,
            "columnFamilies":self.columnFamilies,
            "verisions":self.versions,        },
        "tableRegisters":self.registers}
        return tmp 