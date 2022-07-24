import mysql.connector as connector


def student_table():
    """
    DEFINE TABLES: DOCS, STUDENT, TUTOR, CONSULTING
    """
    with connection.cursor(buffered=True) as cursor:
        query = "SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DOCS'"
        cursor.execute(query)
        if not cursor.fetchone():
            query = f"""
                    CREATE TABLE DOCS( 
                    DOCS_ID VARCHAR(100) PRIMARY KEY,
                    STUDENT_ID VARCHAR(100) NOT NULL,
                    TUTOR_ID VARCHAR(100) NOT NULL,
                    CONSULTANT_ID VARCHAR(100) NOT NULL,
                    COURSE VARCHAR(50) NOT NULL,
                    COURSE_DATE VARCHAR(10) NOT NULL,
                    TIME_LOG VARCHAR(30) NOT NULL,
                    TIME_LAST_MODIFIED VARCHAR(30) NOT NULL,
                    URL VARCHAR(100) NOT NULL)
                    """
            cursor.execute(query)
        else:
            query = f"""
                    ALTER TABLE DOCS MODIFY COLUMN SPENT_HOURS VARCHAR(30) NOT NULL 
                    """
            cursor.execute(query)


def docs_table():
    # STUDENT
    with connection.cursor(buffered=True) as cursor:
        query = "SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'STUDENT'"
        cursor.execute(query)
        if not cursor.fetchone():
            query = f"""
                        CREATE TABLE STUDENT( 
                        STUDENT_ID VARCHAR(100) PRIMARY KEY,
                        NAME VARCHAR(100) NOT NULL,
                        EMAIL VARCHAR(50) NOT NULL,
                        PHONE_NUMBER VARCHAR(10) NOT NULL,
                        CURRENT_PACKAGE VARCHAR(10) NOT NULL,
                        CURRENT_APPS VARCHAR(100) NOT NULL)
                        """
            cursor.execute()
        else:
            query = f"""
                    ALTER TABLE DOCS MODIFY COLUMN SPENT_HOURS VARCHAR(30) NOT NULL 
                    """
            cursor.execute(query)


def tutor_table():
    # TUTOR
    with connection.cursor(buffered=True) as cursor:
        query = "SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TUTOR'"
        cursor.execute(query)
        if not cursor.fetchall():
            query = f"""
                    CREATE TABLE TUTOR( 
                    TUTOR_ID VARCHAR(100) PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    EMAIL VARCHAR(50) NOT NULL,
                    PHONE_NUMBER VARCHAR(10) NOT NULL)
                    """
            cursor.execute(query)


def consultant_table():
    # CONSULTANT
    with connection.cursor(buffered=True) as cursor:
        query = "SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'CONSULTANT'"
        cursor.execute(query)
        if not cursor.fetchall():
            query = f"""
                        CREATE TABLE CONSULTANT( 
                        CONSULTANT_ID VARCHAR(100) PRIMARY KEY,
                        NAME VARCHAR(100) NOT NULL,
                        EMAIL VARCHAR(50) NOT NULL,
                        PHONE_NUMBER VARCHAR(10) NOT NULL)
                        """
            cursor.execute(query)
        else:
            query = f"""
                        DELETE FROM CONSULTANT
                        """
            cursor.execute(query)
            connection.commit()


if __name__ == '__main__':
    connection = connector.connect(host='localhost',
                                   user='root',
                                   password='db_password',
                                   database='consulting')
    consultant_table()
