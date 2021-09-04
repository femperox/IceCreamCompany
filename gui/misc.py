import psycopg2 as ps2

def selectFromBD(cursor, query):

    cursor.execute(query)
    result = cursor.fetchall()
    return result

def transaction(conn, query):

    cursor = conn.cursor()
    result = cursor.execute(query)
    conn.commit()
    cursor.close()


def connect(userName, userPassw):
    return ps2.connect(dbname='IceCreamCompany', user=userName,
                       password=userPassw, host='localhost')

