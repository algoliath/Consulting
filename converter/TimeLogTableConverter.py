from main.googleAPI.converter.Converter import Converter
from main.googleAPI.request.request_form.sheet.table.LogTableFormat import LogTableFormat


class TimeLogTableConverter(Converter):

    def __init__(self, adaptor, current_date):
        self.adaptor = adaptor
        self.current_date = current_date

    def convert(self, param_map):
        adaptor = self.adaptor
        columns = adaptor.get_attr()
        table = [columns]
        for doc_id in param_map.keys():
            params = param_map[doc_id]
            print(f'params = {params}')
            if adaptor.supports(params) and adaptor.validates(params):
                row = []
                values = param_map[doc_id]
                for k in columns:
                    row.append(values[k])
                table.append(row)
        table = sorted(table, key=lambda rows: rows[0])
        table_format = LogTableFormat()
        return table, table_format

    def support(self, file_name):
        return f'Time Log {self.current_date}' in file_name
