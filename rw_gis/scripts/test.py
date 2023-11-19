from rw_gis import db

def main():
    connection = db.get_connection()
    with connection:
        with connection.cursor() as cur:
            sql = "select * from company limit 1"
            cur.execute(sql)
            rows = cur.fetchall()
            print(rows)

if __name__ == '__main__':
    main()
