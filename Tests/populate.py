import sqlite3
from random import randint



def generate(items):
    # Generate the data
    for i in range(items):
        CLIENT_IP = "192.168.0."
        client = str(randint(100,199))
        CLIENT_IP += client
        CLIENT_PORT = str(randint(1000,9000))
        MEMORY_FREE = str(randint(100000000, 999999999))
        MEMORY_PERCENT = str(randint(10,100))
        MEMORY_AVAILABLE = str(randint(1000000000,9999999999))
        MEMORY_TOTAL = str(randint(1000000000,9000000000))
        MEMORY_USED = str(randint(1000000000,9000000000))
        CPU = str(randint(0,100))
        UPTIME = str(randint(0,999999))
        try:
            insert_text(CLIENT_IP, CLIENT_PORT, MEMORY_FREE, MEMORY_PERCENT, MEMORY_AVAILABLE, MEMORY_TOTAL, MEMORY_USED, CPU, UPTIME)
            print("Item/Items {0} entered into database." .format(i+1))
        except Exception:
            print("Data not entered!")


def create_table(db_name,table_name,sql):
	with sqlite3.connect(db_name) as db:
		cursor=db.cursor()
		cursor.execute('PRAGMA foreign_keys=ON')
		cursor.execute("select name from sqlite_master where name=?",(table_name,))
		result=cursor.fetchall()
		kepp_table=True
		if len(result) == 1:
			response = input("The table {0} alerady exists, do yoy wish to recreate it (y/n):".format(table_name))
			if response== "y":
				kepp_table=False
				print('The {0} table will be recreated- all existing data will be lost'.format(table_name))
				cursor.execute('drop table if exists {0}'.format(table_name))
				db.commit()
			else:
				print("The existing table was kept")
		else:
			kepp_table=False
		if not kepp_table:
			cursor.execute(sql)
			db.commit()


# CREATE DATABASE - BUILD THE COLLONS

def create_table_for_doc(db_name):

	sql="""CREATE TABLE IF NOT exists INFORMATION(
			ID INTEGER,
			CLIENT_IP text,
			CLIENT_PORT text,
			MEMORY_FREE text,
			MEMORY_PERCENT text,
			MEMORY_AVAILABLE text,
			MEMORY_TOTAL text,
			MEMORY_USED text,
			CPU text,
			UPTIME text,
			primary key(ID))"""

	create_table(db_name,'INFORMATION',sql)

def insert_text(CLIENT_IP, CLIENT_PORT, MEMORY_FREE, MEMORY_PERCENT, MEMORY_AVAILABLE, MEMORY_TOTAL,MEMORY_USED,CPU,UPTIME):

		with sqlite3.connect("client_data.db") as db:
			cursor=db.cursor()
			data=(CLIENT_IP, CLIENT_PORT, MEMORY_FREE, MEMORY_PERCENT, MEMORY_AVAILABLE, MEMORY_TOTAL,MEMORY_USED,CPU,UPTIME)
			sql="INSERT INTO INFORMATION(CLIENT_IP, CLIENT_PORT, MEMORY_FREE, MEMORY_PERCENT, MEMORY_AVAILABLE, MEMORY_TOTAL, MEMORY_USED, CPU, UPTIME) values (?,?,?,?,?,?,?,?,?)"
			cursor.execute(sql,data)
			db.commit()

# START THE DECRYPTION PROCESS

def main():
    create_table_for_doc("client_data.db")
    items= input("How many items you want to generate?:")
    items=int(items)
    generate(items)


if __name__ == "__main__":
    print("Process started...")
    main()
