from domain.factory import Columns
from repo.model.Repository import Repository


class StudentRepository(Repository):

    def __init__(self, db_connection):
        self.connection = db_connection
        self.columns = Columns.student_table()

    def save(self, dto_map):
        rows = self.convert_dto(dto_map, self.columns)
        query = """
                INSERT INTO STUDENT VALUES(%s, %s, %s, %s, %s, %s)
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    def update(self, dto_map):
        rows = self.convert_dto(dto_map, self.columns[1:] + [self.columns[0]])
        query = """
                UPDATE STUDENT SET NAME = %s,
                                   EMAIL = %s,
                                   PHONE_NUMBER = %s,
                                   CURRENT_PACKAGE = %s,
                                   CURRENT_APPS = %s
                WHERE STUDENT_ID = %s
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    def read(self):
        query = """
                SELECT * FROM STUDENT
                """
        connect = self.connection
        with connect.cursor(buffered=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

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
