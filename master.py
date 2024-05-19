import tableManager

c = input('Lil Base@local: ')
c = c.replace(',','').split(' ')
if c[0].lower() == 'create':
    print(tableManager.createTable(c[1:]))