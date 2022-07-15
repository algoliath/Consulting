from repo.Repository import Repository


class DocsRepository(Repository):

    def __init__(self, db_connection):
        self.connection = db_connection
        self.columns = self.get_columns(db_connection)

    def save(self, dto_map):
        rows = []
        query = """
                INSERT INTO DOCS VALUES(%s, %s, %s, %s)
                """
        connect = self.connection
        try:
            for doc_id in range(len(dto_map)):
                row = []
                for col in self.columns:
                    row.append(dto_map[str(doc_id)].get(col[0], 1))
                rows.append(row)
            with connect.cursor() as cursor:
                cursor.executemany(query, rows)
        except connect.error() as error:
            print(error)

    def read(self):
        query = """
                SELECT * FROM DOCS
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def get_columns(self):
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DOCS'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        return result
