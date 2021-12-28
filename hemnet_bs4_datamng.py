import time
import mysql.connector
import json
import re
from binascii import hexlify, unhexlify


# json converter
#------------------------------------------------------------------------------
def jsonimp(data_input,outfile):
    import json
    
    data = data_input
    json_string = json.dumps(data)
    with open(outfile, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()
    return json_string


# Encoding function
#------------------------------------------------------------------------------
class BytesIntEncoder:

    @staticmethod
    def encode(b: bytes) -> int:
        return int(hexlify(b), 16) if b != b'' else 0

    @staticmethod
    def decode(i: int) -> int:
        return unhexlify('%x' % i) if i != 0 else b''



# Getting DB info to connect
#------------------------------------------------------------------------------

hostname = input('Please Enter your hostname:')
db = input('Which Database do you want to work on? ')
table = 'Hemdata'
username = input('Please Enter your username:')
pw = input('Please Enter your Password:')
cnx = mysql.connector.connect(user=username, password=pw,
                              host=hostname,
                              database=db)
cursor = cnx.cursor()
stmt = "SHOW TABLES LIKE '%s'" %(table)
cursor.execute(stmt)
result = cursor.fetchone()
if result:
    pass
else:
    table_q = 'CREATE TABLE %s (title varchar(100), area float (30), price int(20), room int(5), city varchar(50), kommun varchar(50), kommun_enc int(100), type varchar(30), type_enc int(50), url LONGTEXT);'%(table)
    cursor.execute(table_q)
    strict_q = "SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
    cursor.execute(strict_q)
    


   
# exporting modifyed data to MySQL DB and a final json file
#------------------------------------------------------------------------------ 
   
startarea = time.time()
data = []
with open('datajson.txt') as json_file:
    jdata = json.load(json_file)
add_details = ("INSERT IGNORE INTO Hemdata "
               "(title,area,price,room,city,kommun,kommun_enc,type,type_enc,url)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
for i in range(0,len(jdata)):
    title = jdata[i]['title'].strip()
    area_room = re.findall(r'\d+', str(jdata[i]['area_room']))
    try:
        if jdata[i]['type'].strip() == 'Tomter':
            area = int(''.join(area_room))
        elif len(area_room) == 2:   
            area, room = float(area_room[0]), int(area_room[1])
        elif len(area_room) == 3:      
            room = int(area_room.pop(-1))
            area = int(''.join(area_room))
        elif len(area_room) == 0:
            area, room = 0, 0    
        elif len(area_room) == 1:
            area, room = float(area_room[0]), 0
    except:
        area, room = 0, 0  
    price = re.findall(r'\d+', jdata[i]['price'])
    price = int(''.join(price))
   
    city_kommun = jdata[i]['city_kommun'].split()
    if len(city_kommun )>2:
        kommun = city_kommun[-1]
        loc = city_kommun[-2].replace(',','')
    else:
        kommun = city_kommun[-1]
        loc = 'No Info'
    url = jdata[i]['url']
    h_type = jdata[i]['type'].strip()
    kommun_enc = BytesIntEncoder.encode(kommun.encode())
    type_enc = BytesIntEncoder.encode(h_type.encode())
    
    
    hem_details = (title, area, price, room, loc, kommun,kommun_enc,
                   h_type, type_enc, url )
    cursor.execute(add_details, hem_details)
    cnx.commit()


    final_json = {"title":title ,"price":price, "area":area , 'room':room,
                   'city':loc,'url':url, 'kommun': kommun, 'kommun_enc':kommun_enc,
                   'type':h_type, 'type_enc': type_enc}
    
    data.append(final_json)


'''
To handle the data more easily for the purpose of this project, The code will 
generate a json file containing modified and clean data to use in data modeling.
-------------------------------------------------------------------------------- 
'''
   
jsonimp(data, 'final_json.txt')
cursor.close()
cnx.close()

print ('data importing to db time is %i mins:'%((time.time() - startarea)/60))


