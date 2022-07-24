import logging as log

from converter.model.Converter import Converter
from domain.factory import Columns
from request.request_form.sheet.table.BasicFormat import BasicFormat

log.getLogger().setLevel("DEBUG")


class PaymentTableConverter(Converter):

    def __init__(self, connection, current_date):
        self.connection = connection
        self.current_date = current_date

    def convert(self, new_query=''):

        connection = self.connection
        query = """
                 SELECT CONSULTANT.CONSULTANT_ID CONSULTANT_ID, 
                        CONSULTANT.NAME CONSULTANT_NAME,
                        DOCS.STUDENT_ID STUDENT_ID, 
                        STUDENT.NAME STUDENT_NAME,
                        SUM(DOCS.SPENT_HOURS) TOTAL_HOURS_SPENT
                         
                 FROM CONSULTANT 
                 LEFT JOIN DOCS ON DOCS.CONSULTANT_ID = CONSULTANT.CONSULTANT_ID
                 LEFT JOIN STUDENT ON STUDENT.STUDENT_ID = DOCS.STUDENT_ID
                 GROUP BY CONSULTANT.CONSULTANT_ID
                 HAVING COUNT(DOCS_ID) >= 1
                """
        if new_query:
            query = new_query
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            log.debug(f'payment table result={result}')

        header = []
        for col in Columns.payment_table():
            header.append(col)
        table = [header]
        for row in result:
            table.append(row)
        # sort (options)
        # table = sorted(table, key=lambda rows: rows[0])
        table_format = BasicFormat()
        return table, table_format

    def support(self, file_name):
        return f'Payment {self.current_date}' in file_name
