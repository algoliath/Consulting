from converter.model.Converter import Converter
from domain.factory.table import Columns
from request.request_form.sheet.table.BasicFormat import BasicFormat


class TimeTableConverter(Converter):

    def __init__(self, connection, current_date):
        self.current_date = current_date
        self.connection = connection

    def convert(self):
        try:
            connection = self.connection
            query = """
                     SELECT *
                     FROM DOCS
                    """
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(f'result={result}')

            header = []
            for col in Columns.time_table():
                header.append(col)
            table = [header]
            for row in result:
                table.append(row)

            # table = sorted(table, key=lambda rows: rows[0])
            table_format = BasicFormat()
            print(f'table={table}')
            return table, table_format

        except Exception as error:
            print(f'time_table_converter={error}')
            raise error

    def support(self, file_name):
        print(f'file_name={file_name}')
        return f'Time Log {self.current_date}' in file_name
