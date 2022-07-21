from repo.model.Repository import Repository


class DocsRepository(Repository):

    def __init__(self, db_connection):
        self.connection = db_connection
        self.columns = self.get_columns()

    def save(self, dto_map):
        rows = self.convert_dto(dto_map, self.columns)
        print(f'save rows:{rows}')
        query = """
                INSERT INTO DOCS VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    def update(self, dto_map):
        rows = self.convert_dto(dto_map, self.columns[1:]+[self.columns[0]])
        print(f'update rows:{rows}')
        query = """
                UPDATE DOCS SET STUDENT_ID = %s,
                                TUTOR_ID = %s,
                                CONSULTANT_ID = %s,
                                COURSE = %s,
                                COURSE_DATE = %s,
                                TIME_LOG = %s,
                                TIME_LAST_MODIFIED = %s,
                                URL = %s,
                                SPENT_HOURS = %s
                WHERE DOCS_ID = %s
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    # read row excluding columns
    def read(self):
        query = """
                SELECT * FROM DOCS
                """
        connect = self.connection
        with connect.cursor(buffered=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        print(f'result={result}')
        return result

    def get_columns(self):
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DOCS'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        columns = []
        for col in result:
            columns.append(col[0])
        return columns

    def convert_dto(self, dto_map, columns):
        rows = []
        try:
            for doc_id in dto_map:
                row = []
                for col in columns:
                    formatted = col.replace('_', ' ')
                    row.append(dto_map[doc_id].get(formatted))
                rows.append(row)
        except Exception as error:
            print(error)
        return rows
