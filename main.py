import pymysql.cursors

# Connect to the database
connection = pymysql.connect(
    host = 'astronaut.snu.ac.kr',
    port = 3306,
    user = 'BDE-2018-15',
    password = '80c405901278',
    db = 'BDE-2018-15',
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor)

table = ['Building', 'Performance', 'Audience']
fields = [['id', 'name', 'location', 'capacity', 'assigned'], 
         ['id', 'name', 'type', 'price','booked'], ['id', 'name', 'gender', 'age']]

with connection.cursor() as cursor:
    print('='*60)
    print('1. print all buildings\n2. print all performances\n3. print all audiences\n4. insert a new building\n5. remove a building')
    print('6. insert a new performance\n7. remove a performance\n8. insert a new audience\n9. remove an audience')
    print('10. assign a performance to a building\n11. book a performance\n12. print all performances assigned to a building')
    print('13. print all audiences who booked for a performance\n14. print ticket booking status of a performance\n15. exit')
    print('='*60)
    order = int(input('Select your action: ')) - 1
    if order == 14:
        print('Bye!')
        connection.close()
    while 0 <= order <= 13:
        
        if order <= 2:
            sql = ['select * from buildings order by id', 
                   'select * from performances  order by id',
                   'select * from audiences  order by id']
            space = [5, 20, 10, 10, 5]
            cursor.execute(sql[order])
            result = cursor.fetchall()
            
            print('-'*50)
            for i, num in enumerate(fields[order]):
                print(str(num).ljust(space[i]), end = '')
            print('\n', '-'*50)
            
            for row in result:
                for i in range(len(fields[order])):
                    print(str(row[fields[order][i]]).ljust(space[i]), end = '')
                if row != result[-1]:
                    print()
                    
            print('\n', '-'*50)
            
            order = int(input('Select your action: ')) - 1
            
        if order in [3, 5, 7]:
            insert_num = (order-3)//2
            input1 = input(table[insert_num]+' '+fields[insert_num][1]+': ')
            input2 = input(table[insert_num]+' '+fields[insert_num][2]+': ')
            input3 = int(input(table[insert_num]+' '+fields[insert_num][3]+': '))
            sql = "INSERT INTO "+table[insert_num].lower()+"s ("+ fields[insert_num][1]+", "+fields[insert_num][2]+\
            ", "+fields[insert_num][3]+") VALUES (%s, %s, %s)"
            cursor.execute(sql, (input1, input2, input3))
            connection.commit()
            print('A '+table[insert_num].lower()+' is successfully inserted')
            order = int(input('Select your action: ')) - 1
            
        if order in [4, 6, 8]:
            insert_num = (order-4)//2
            order = int(input('Select your action: ')) - 1 
            
        if order == 9:
            input5 = input('Building ID: ')
            input6 = input('Performance ID: ')
            sql = "SELECT COUNT(*) AS C FROM assign WHERE p_id = "+input6
            cursor.execute(sql)
            result = cursor.fetchone()
            if result['C'] == 0:         
                sql = "INSERT INTO assign (b_id, p_id) values (%s, %s)"
                cursor.execute(sql, (input5, input6))
                sql = "UPDATE buildings SET assigned = assigned + 1"
                cursor.execute(sql)
                connection.commit()
                print("Successfully assigned a performance")
            else:
                print("The performance you chose is already assigned")
            order = int(input('Select your action: ')) - 1
            
        if order == 10:
            input7 = input('Performance ID: ')
            input8 = input('Audience ID: ')
            input9 = input('Seat number(if multiple seats, then separate them with a comma and a single space(', '): ').split(', ')
            sql = 'SELECT COUNT(*) AS C FROM assign WHERE p_id = '+input7
            cursor.execute(sql)
            result = cursor.fetchall()
            if result['C'] == 1:
                sql = "INSERT INTO reserve (p_id, a_id) values (%s, %s)"
                cursor.execute(sql, (input7, input8))
                print("Successfully booked a performance")
                print("Total ticket price is")
            elif result['C'] == 0:
                print("The preformance you chose is not assigned yet")
            
        if order == 14:
            print('Bye!')
            connection.close()