import tableManager
'''
This module must be the controller to communicate GUI with tableManager
'''
run = True
while run:
    c = input('Tini-Base@local: ')
    c = c.replace(',', ' ').split(' ')
    c = [element.replace("'", '').replace('"', '') for element in c if element != ''] 
    
    command = c[0].lower()
    
    if command == 'create':
        print(tableManager.createTable(c[1:]))
    elif command == 'put':
        print('put instance')
        tableManager.addRegisters(c[1], c[2:])
    elif command == 'exit':
        run = False
        tableManager.saveTables()
        print('exiting tiny base')
    elif command == 'scan':
        tableManager.scanTable(c[1])
    elif command == 'list':
        print(tableManager.listTables())
    elif command == 'delete':
        tableManager.dropTable(c[1])
    elif command == 'alter':
        operation = c[2].upper()  # ADD, DROP, MODIFY
        column_name = c[3]
        column_type = c[4] if len(c) > 4 else None
        tableManager.alterTable(c[1], operation, column_name, column_type)
    elif command == 'describe':
        print(tableManager.describeTable(c[1]))
    else:
        print('unknown')
