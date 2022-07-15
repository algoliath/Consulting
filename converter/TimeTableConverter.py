from converter.interface.Converter import Converter
from request.request_form.sheet.table.TimeLogFormat import TimeLogFormat


class TimeTableConverter(Converter):

    def __init__(self, docs_repository, current_date):
        self.current_date = current_date
        self.repo = docs_repository

    def convert(self):
        repo = self.repo
        table = [repo.get_columns()]
        table += repo.read()
        table = sorted(table, key=lambda rows: rows[0])
        table_format = TimeLogFormat()
        return table, table_format

    def support(self, file_name):
        return f'Time Log {self.current_date}' in file_name
