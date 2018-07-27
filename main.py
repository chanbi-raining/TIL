import pymysql.cursors

# Connect to the database
connection = pymysql.connect(
    host = 'astronaut.snu.ac.kr',
    port = 3306,
    user = 'BDE-2018-15',
    password = '80c405901278',
    db = 'BDE-2018-15',
    charset = 'utf8',
    autocommit = True,
    cursorclass = pymysql.cursors.DictCursor)

table = ['Building', 'Performance', 'Audience']
tname = [x.lower()+'s' for x in table]
fields = [['id', 'name', 'location', 'capacity', 'assigned'], 
         ['id', 'name', 'type', 'price','booked'], ['id', 'name', 'gender', 'age']]
space = [5, 30, 10, 10, 5]


# ID Check
def id_check(num, tnum):
    check = 'SELECT id FROM %s' % tname[tnum]
    cursor.execute(check)
    results = cursor.fetchall()
    ids = []
    for i in results:
        ids.append(i['id'])
    if num == '':
        return False
    elif int(num) not in ids:
        return False
    return True
    
with connection.cursor() as cursor:
    print('='*60)
    for i, j in enumerate(tname):
        print(str(i+1)+'. print all '+j)
    for i, j in enumerate(tname):
        print(str(4+i*2)+'. insert a new', j[:-1], '\n'+str(5+i*2)+'. remove a', j[:-1])
    print('10. assign a performance to a building') 
    print('11. book a performance')
    print('12. print all performances assigned to a building')
    print('13. print all audiences who booked for a performance') 
    print('14. print ticket booking status of a performance\n15. exit')
    print('='*60)
    order = int(input('Select your action: ')) - 1
            
    while order != 14:
        
        while order < 0 or order > 13:
            print('You have selected a wrong number. Please choose an integer between 1 and 15.')
            order = int(input('Select your action: ')) - 1
            
        while 0 <= order <= 13:
            
            cancel = 0 # if error, turns 1
            
            if order <= 2:
                sql = ['select * from buildings order by id', 
                       'select * from performances  order by id',
                       'select * from audiences  order by id']
                cursor.execute(sql[order])
                result = cursor.fetchall()
                
                print('-' * 60)
                for i, num in enumerate(fields[order]):
                    print(str(num).ljust(space[i]), end = '')
                print('\n', '-'*60)
                
                for row in result:
                    for i in range(len(fields[order])):
                        print(str(row[fields[order][i]]).ljust(space[i]), end = '')
                    if row != result[-1]:
                        print()                        
                print('\n', '-'*60)
                
            if order in [3, 5, 7]:
                ins = (order-3)//2
                input1 = input(table[ins]+' '+fields[ins][1]+': ')
                input1 = input1[:200] if len(input1) > 200 else input1 # cut the string to 200 letters
                input2 = input(table[ins]+' '+fields[ins][2]+': ')
                input2 = input2[:200] if len(input2) > 200 else input2 # cut the string to 200 letters
                if order == 7:
                    input2.upper()
                    while input2 not in ['M', 'F', 'O']:
                        print('Your input in gender is wrong. Type M for male, F for female, and O for other.')
                        input2 = input(table[ins]+' '+fields[ins][2]+': ')
                        
                input3 = eval(input(table[ins]+' '+fields[ins][3]+': '))
                while input3 < 0:
                    print('Your input is a negative integer. Please try again.')
                    input3 = eval(input(table[ins]+' '+fields[ins][3]+': '))
                if order == 7:
                    while input3 <= 0 or input3 > 100:
                        print('Are you sure of your age? Please try again.')
                        input3 = eval(input(table[ins]+' '+fields[ins][3]+': '))
                        
                sql = "INSERT INTO "+table[ins].lower()+"s ("+ fields[ins][1]+", "+fields[ins][2]+\
                ", "+fields[ins][3]+") VALUES (%s, %s, %s)"
                cursor.execute(sql, (input1, input2, input3))
                print('A '+table[ins].lower()+' is successfully inserted')
                
            if order in [4, 6, 8]:
                ins = (order-4)//2
                input13 = input(table[ins]+' '+fields[ins][0].upper()+': ')
                if not id_check(input13, ins):
                    print('You have chose a wrong', table[ins], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    if order == 4:
                        sql = 'SELECT p_id FROM assign WHERE b_id ='+input13
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if result:
                            # first, delete from reserve
                            for row in result:
                                sql = 'DELETE FROM reserve WHERE p_id ='+str(row['p_id'])
                            cursor.execute(sql)
                            
                            # then, delete from assign
                            sql = 'DELETE FROM assign WHERE b_id ='+input13
                            cursor.execute(sql)
                    
                    if order == 6:
                        # first, delete reserve
                        sql = 'DELETE FROM reserve where p_id ='+input13
                        cursor.execute(sql)                        
                        
                        # then, check assign
                        sql = 'SELECT b_id FROM assign where p_id ='+input13
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if result: # update the buildings table
                            for row in result:
                                sql = 'UPDATE buildings SET assigned = assigned - 1 WHERE id = '+str(row['b_id'])
                                cursor.execute(sql)
                            #delete the assigned table
                        sql = 'DELETE FROM assign WHERE p_id ='+input13
                        cursor.execute(sql)
                    
                    if order == 8:
                        # first, check if reserved
                        sql = 'SELECT COUNT(seatno) as R FROM reserve WHERE a_id ='+input13
                        cursor.execute(sql)
                        r = cursor.fetchone()['R']
                        
                        sql = 'SELECT distinct p_id from reserve where a_id = '+input13
                        cursor.execute(sql)
                        perid = cursor.fetchall()
                        per = []
                        for row in perid:
                            per.append(row['p_id'])
                        
                        if r:
                            sql = 'DELETE FROM reserve WHERE a_id ='+input13
                            cursor.execute(sql)
                            for i in per:
                                sql = 'UPDATE performances SET booked = booked -'+str(r)+' where id = '+str(i)
                                cursor.execute(sql)                
                    
                    sql = 'delete from %s where id = %s' % (tname[ins], input13)
                    cursor.execute(sql)
                    print('Successfully deleted a '+table[ins].lower())
                
            if order == 9:
                input5 = input('Building ID: ')
                if not id_check(input5, 0):
                    print('You have chose a wrong', table[0], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    input6 = input('Performance ID: ')
                    if not id_check(input6, 1):
                        print('You have chose a wrong', table[1], 'ID. Please try again.')
                        cancel = 1
                if not cancel:
                    sql = "SELECT COUNT(*) AS C FROM assign WHERE p_id = "+input6
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if result['C'] == 0:         
                        sql = "INSERT INTO assign (b_id, p_id) values (%s, %s)"
                        cursor.execute(sql, (input5, input6))
                        sql = "UPDATE buildings SET assigned = assigned + 1 where id ="+ input5 
                        cursor.execute(sql)
                        print("Successfully assigned a performance")
                    else:
                        print("The performance you chose is already assigned")
                
                
            if order == 10:
                input7 = input('Performance ID: ')
                if not id_check(input7, 1):
                    print('You have chose a wrong', table[1], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    sql = 'SELECT COUNT(*) AS c FROM assign WHERE p_id = '+input7
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result[0]['c'] == 0:
                        print('The performance you chose is yet to be assigned.')
                        cancel = 1
                        
                if not cancel:
                    input8 = input('Audience ID: ')
                    if not id_check(input8, 2):
                        print('This ID is not registered as an audiece. Please try again.')
                        cancel = 1
                if not cancel:
                    input9 = input('Seat number: ').split(',')
                    seatno = sorted(list(map(lambda x: eval(x), input9)))
                    sql = 'SELECT price FROM performances WHERE id ='+input7
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    price = res['price']
                
                    if len(set(seatno)) != len(seatno):
                        print('There are duplicates in your seat number. Check them again.')
                        cancel = 1
                    elif not cancel: 
                        sql = 'SELECT capacity FROM buildings where id = \
                                (SELECT b_id FROM assign WHERE p_id = '+input7+')'
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        cap = result['capacity']
                        sql = 'SELECT seatno FROM reserve WHERE p_id ='+input7
                        cursor.execute(sql)
                        status = cursor.fetchall()
                        l_sta = []
                        for row in status:
                            if row['seatno'] in seatno:
                                print('The seat number %d is already booked.' % row['seatno'])
                                cancel = 1
                        for no in seatno:
                            if no > cap:
                                print('The seat number %d is over the capacity.' % no)
                                cancel = 1
                                break
                        if not cancel:
                            for seat in seatno:
                                sql = "INSERT INTO reserve (p_id, a_id, seatno) values (%s, %s, %s)"
                                cursor.execute(sql, (input7, input8, seat))
                            sql = 'UPDATE performances SET booked = booked + %s WHERE id = %s'
                            cursor.execute(sql, (len(seatno), input7))
                            print("Successfully booked a performance")
                            print("Total ticket price is %d" % (price * len(seatno))) 
                    
            if order == 11:
                input10 = input(table[0]+' '+fields[0][0].upper()+': ')
                if not id_check(input10, 0):
                    print('You have chose a wrong', table[0], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    sql = 'SELECT * FROM performances where id in\
                            (SELECT p_id FROM assign where b_id ='+input10+') order by id'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    
                    if not result:
                        print('There are no performances assigned to the building')
                    
                    else:
                        print('-'*60)
                        for i, num in enumerate(fields[1]):
                            print(str(num).ljust(space[i]), end = '')
                        print('\n', '-'*60)
                        
                        for row in result:
                            for i in range(len(fields[1])):
                                print(str(row[fields[1][i]]).ljust(space[i]), end = '')
                            if row != result[-1]:
                                print()
                                
                        print('\n', '-'*60)
            
            if order == 12:
                input11 = input(table[1]+' '+fields[1][0].upper()+': ')
                if not id_check(input11, 1):
                    print('You have chose a wrong', table[1], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    sql = 'SELECT * FROM audiences WHERE id IN \
                            (SELECT a_id FROM reserve WHERE p_id ='+input11+') order by id'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    
                    if not result:
                        print('There are no bookings for this performance')
                    else:
                        print('-'*60)
                        for i, num in enumerate(fields[2]):
                            print(str(num).ljust(space[i]), end = '')
                        print('\n'+'-'*60)
                        
                        for row in result:
                            for i in range(len(fields[2])):
                                print(str(row[fields[2][i]]).ljust(space[i]), end = '')
                            if row != result[-1]:
                                print()
                                
                        print('\n'+'-'*60)
            
            if order == 13:
                input12 = input(table[1]+' '+fields[1][0].upper()+': ')
                if not id_check(input12, 1):
                    print('You have chose a wrong', table[1], 'ID. Please try again.')
                    cancel = 1
                if not cancel:
                    sql = 'SELECT capacity FROM buildings where id = \
                            (SELECT b_id FROM assign WHERE p_id = '+input12+')'
                    cursor.execute(sql)
                    result = cursor.fetchone()

                    cap = result['capacity']
                    capacity = list(range(1, cap+1))
                    sql = 'SELECT seatno, a_id FROM reserve WHERE p_id ='+input12+' order by seatno'
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if not res: 
                        print('There are no bookings for the performace you chose')            
                    else:
                        seat_st = ['']*cap
                        for row in res:
                            seat_st[row['seatno']-1] = row['a_id']
                        
                        print('-'*60)
                        for i, num in enumerate(['seat_number', 'audience_id']):
                            print(str(num).ljust(30), end = '')
                        print('-'*60)
                        
                        for i in range(cap):
                            print(str(capacity[i]).ljust(30), seat_st[i])
                        print('-'*60)
            
            order = int(input('Select your action: ')) - 1
            
    if order == 14:
        order += 1
        print('Bye!')
        connection.close()
