from converter.model.Converter import Converter
from domain.factory.Attributes import get_attributes
from domain.factory.table import Columns
from request.request_form.docs.table.BasicTableFormat import BasicTableFormat
from request.request_form.sheet.table.StatsTableFormat import StatsTableFormat
from request.request_form.sheet.chart.StatsChartFormat import StatsChartFormat


# def build_stats_param(adaptor, param_map, key, val):
#     stats = {}
#     column = {}
#     for doc_id in param_map.keys():
#         params = param_map[doc_id]
#         if adaptor.supports() and adaptor.validates(params):
#             k = param_map[doc_id][key]
#             v = param_map[doc_id][val]
#             column[v] = ''
#             if k not in stats:
#                 stats[k] = {}
#             if v not in stats[k]:
#                 stats[k][v] = 0
#             stats[k][v] += 1
#     # print(stats)
#     return stats


class StatsTableConverter(Converter):

    def __init__(self, k, v, connection):
        self.k = k
        self.v = v
        self.connection = connection
        pass

    def support(self, file_name):
        split = file_name.split('/')
        return 'Chart' in file_name and len(split) == 3

    def convert(self):
        k = get_attributes(self.k)
        v = get_attributes(self.v)
        connection = self.connection
        query = """
                 SELECT *
                 FROM CONSULTANT 
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            print(f'result={result}')

        header = []
        for col in k:
            header.append(col)
        table = [header]
        for row in result:
            table.append(row)

        table_format = BasicTableFormat()
        chart_format = StatsChartFormat("line")
        return table, table_format, chart_format, k, v

