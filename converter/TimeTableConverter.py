from converter.interface.Converter import Converter
from request.request_form.sheet.table.TimeLogFormat import TimeLogFormat


class TimeTableConverter(Converter):

    def __init__(self, repository, current_date):
        self.current_date = current_date
        self.repository = repository

    def convert(self):
        try:
            repository = self.repository
            rows = repository.read()
            columns = repository.get_columns()
            header = []
            for col in columns:
                header.append(col)
            table = [header]
            for row in rows:
                table.append(row)
            # sort (options)
            # table = sorted(table, key=lambda rows: rows[0])
            table_format = TimeLogFormat()
            print(f'table={table}')
            return table, table_format
        except Exception as error:
            print(f'time_table_converter={error}')
            raise error

    def support(self, file_name):
        print(f'file_name={file_name}')
        return f'Time Log {self.current_date}' in file_name
