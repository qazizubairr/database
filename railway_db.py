import psycopg2
import psycopg2.extras
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        def send_csv_to_psql(connection,csv,table_):
    
            sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
            file = open(csv, "r", encoding='utf-8')
            table = table_
            with connection.cursor() as cur:
                cur.execute("truncate " + table + ";")  #avoiding uploading duplicate data!
                cur.copy_expert(sql=sql % table, file=file)
                connection.commit()
        #         cur.close()
        #         connection.close()
            return connection.commit()
        send_csv_to_psql(conn,'countries1.csv','countries_info')
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')

        # # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
# addr_df_.to_csv('address_Python_convertR.csv',index=False)


# conn.autocommit = True  # read documentation understanding when to Use & NOT use (TRUE)



