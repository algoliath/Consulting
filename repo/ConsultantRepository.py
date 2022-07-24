from domain.factory import Columns
from repo.model.Repository import Repository
import logging as log

log.getLogger('Consultant-Repo').setLevel('DEBUG')


class ConsultantRepository(Repository):

    def __init__(self, db_connection):
        self.connection = db_connection
        self.columns = Columns.consultant_table()

    def save(self, dto_map):
        rows = self.convert_dto(dto_map, self.columns)
        log.info(f'consultant save rows={rows}')
        query = """
                INSERT INTO CONSULTANT
                VALUES(%s, %s, %s, %s)
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    def update(self, dto_map):
        log.info(f'columns={self.columns}')
        rows = self.convert_dto(dto_map, self.columns[1:] + [self.columns[0]])
        log.info(f'consultant update rows={rows}')
        query = """
                UPDATE CONSULTANT SET 
                NAME = %s,
                EMAIL = %s,
                PHONE_NUMBER = %s
                WHERE CONSULTANT_ID = %s
                """
        connect = self.connection
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        connect.commit()

    def read(self):
        query = """
                SELECT * FROM CONSULTANT
                """
        connect = self.connection
        with connect.cursor(buffered=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        log.debug(f'result={result}')
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
            log.info(error)
        return rows
