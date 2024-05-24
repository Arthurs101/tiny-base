import tableManager
run = True
while run:
    c = input('Tini-Base@local: ')
    c = c.replace(',',' ').split(' ')
    c = [element.replace("'",'').replace('"','') for element in c if element != ''] 
    if c[0].lower() == 'create':
        print(tableManager.createTable(c[1:]))
    elif c[0].lower() == 'put':
        print('put instance')
        tableManager.addRegisters(c[1],c[2:])
    elif c[0].lower() == 'exit':
        run = False
        tableManager.saveTables()
        print('exiting tiny base')
    elif c[0].lower() == 'scan':
        tableManager.scanTable(c[1])
    elif c[0] == 'list':
        print(tableManager.listTables())
    else:
        print('unknown')