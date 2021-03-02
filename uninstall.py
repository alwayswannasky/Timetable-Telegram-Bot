import config
import cx_Oracle

with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
    cursor = connection.cursor()
    try:
        cursor.execute("drop table couples")
        cursor.execute("drop table subscription")

        connection.commit()

        print('База данных удалена!')
    except cx_Oracle.DatabaseError:
        print("База данных не создана!")
