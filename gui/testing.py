
import psycopg2 as ps2
import misc

conn = ps2.connect(dbname='IceCreamCompany', user='genmanager',
                       password='admin', host='localhost')
cursor = conn.cursor()
print(misc.selectFromBD1(cursor, 'select * from allOrders;'))

conn.close()
