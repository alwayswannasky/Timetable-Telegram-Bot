import config
import cx_Oracle

with cx_Oracle.connect(config.orcl_user, config.orcl_password, config.orcl_dns, encoding="UTF-8") as connection:
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE TABLE couples(День_недели VARCHAR2(2 CHAR) NOT NULL,Курс NUMBER (1) NOT NULL,Специальность "
                       "VARCHAR2(5 CHAR) NOT NULL,Пара NUMBER (1) NOT NULL,Название_предмета VARCHAR2(100 CHAR) NOT NULL,"
                       "Тип_предмета VARCHAR2(10 CHAR),Преподаватель VARCHAR2(20 CHAR),Номер_ауд VARCHAR2(10 CHAR),"
                       "Тип_недели NUMBER(1) NOT NULL, Подгруппа NUMBER(1) NOT NULL)")

        cursor.execute('CREATE TABLE subscription(ИД NUMBER(10) NOT NULL,ИМЯ VARCHAR2(10 CHAR),'
                       'СПЕЦИАЛЬНОСТЬ VARCHAR2(5 CHAR) NOT NULL,КУРС NUMBER (1) NOT NULL,'
                       'CONSTRAINT Subscription_PK PRIMARY KEY (ИД))')

        file = open('data.txt', 'r', encoding='utf8')
        for line in file:
            cursor.execute(line[:-2])

        connection.commit()

        print('База данных создана!')
    except cx_Oracle.DatabaseError:
        print("База данных уже создана!")
