import tableManager

c = input('Tini-Base@local: ')
c = c.replace(',','').split(' ')
if c[0].lower() == 'create':
    print(tableManager.createTable(c[1:]))