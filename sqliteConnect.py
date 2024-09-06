import sqlite3


def selectSQL(sql):
    conn = sqlite3.connect('instance/TaichungCityBusStop.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()    

    return data

def getHeader(table):

    conn = sqlite3.connect('instance/TaichungCityBusStop.db')
    cursor = conn.cursor()
    sql = "PRAGMA table_info({})".format(table)
    cursor.execute(sql)
    headerInfo = cursor.fetchall()
    cursor.close()
    conn.close()    

    headerName = []

    for header in headerInfo:
        headerName.append(header[1])

    return headerName


