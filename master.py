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
        if len(c) < 2:
            print("Error: Missing table name and columns.")
        else:
            try:
                table = tableManager.createTable(c[1:])
                print(f"Table '{table.name}' created with columns: {table.columnFamilies}")
            except Exception as e:
                print(f"Error: {e}")
    elif command == 'put':
        if len(c) < 3:
            print("Error: Missing table name and register data.")
        else:
            print('put instance')
            tableManager.addRegisters(c[1], c[2:])
    elif command == 'exit':
        run = False
        tableManager.saveTables()
        print('exiting tiny base')
    elif command == 'scan':
        if len(c) < 2:
            print("Error: Missing table name.")
        else:
            tableManager.scanTable(c[1])
    elif command == 'list':
        print(tableManager.listTables())
    elif command == 'delete':
        if len(c) < 2:
            print("Error: Missing table name.")
        else:
            tableManager.dropTable(c[1])
    elif command == 'alter':
        if len(c) < 4:
            print("Error: Missing parameters for alter table.")
        else:
            try:
                operation = c[2].upper()  # ADD, DROP, MODIFY
                column_name = c[3]
                column_type = c[4] if len(c) > 4 else None
                tableManager.alterTable(c[1], operation, column_name, column_type)
                print(f"Table '{c[1]}' altered: {operation} {column_name} {column_type}")
            except Exception as e:
                print(f"Error: {e}")
    elif command == 'describe':
        if len(c) < 2:
            print("Error: Missing table name.")
        else:
            try:
                schema = tableManager.describeTable(c[1])
                print(f"Table '{c[1]}' schema: {schema}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print('unknown')
