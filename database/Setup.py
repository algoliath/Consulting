import mysql.connector as connector
import domain.table.ColumnFactory as column_factory

connection = connector.connect(host='localhost',
                               user='root',
                               password='db_password',
                               database='consulting')


if __name__ == '__main__':
    with connection.cursor() as cursor:
        DOCS_ID, STUDENT_ID, TUTOR_ID, COURSE, COURSE_DATE, TIME_LOG, TIME_LAST_MODIFIED, URL = column_factory.time_table()
        create_query = f"""
        CREATE TABLE DOCS(
        {DOCS_ID} VARCHAR(100) PRIMARY KEY,
        {STUDENT_ID} VARCHAR(100) NOT NULL,
        {TUTOR_ID} VARCHAR(100) NOT NULL,
        {COURSE} VARCHAR(50) NOT NULL,
        {COURSE_DATE} VARCHAR(10) NOT NULL,
        {TIME_LOG} VARCHAR(10) NOT NULL, 
        {TIME_LAST_MODIFIED} VARCHAR(100),
        {URL} VARCHAR(100), 
        """
        cursor.execute(create_query)
        result = cursor.fetchall()
        for row in result:
            print(row)



