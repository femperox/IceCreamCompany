import psycopg2 as ps2

def selectFromBD(cursor, query):

    cursor.execute(query)
    result = cursor.fetchall()
    return result

def selectFromBDWithConn(userName, userPassw, query):

    conn = connect(userName, userPassw)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def connect(userName, userPassw):
    return ps2.connect(dbname='IceCreamCompany', user=userName,
                       password=userPassw, host='localhost')
