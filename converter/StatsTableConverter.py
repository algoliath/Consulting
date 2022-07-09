from main.googleAPI.converter.Converter import Converter
from main.googleAPI.request.request_form.sheet.table.StatsTableFormat import StatsTableFormat
from main.googleAPI.request.request_form.sheet.chart.StatsChartFormat import StatsChartFormat


def build_stats_param(adaptor, param_map, key, val):
    stats = {}
    column = {}
    for doc_id in param_map.keys():
        params = param_map[doc_id]
        if adaptor.supports() and adaptor.validates(params):
            k = param_map[doc_id][key]
            v = param_map[doc_id][val]
            column[v] = ''
            if k not in stats:
                stats[k] = {}
            if v not in stats[k]:
                stats[k][v] = 0
            stats[k][v] += 1
    # print(stats)
    return stats


class StatsTableConverter(Converter):

    def __init__(self, adaptor, k, v):
        self.adaptor = adaptor
        self.k = k
        self.v = v
        pass

    def support(self, file_name):
        split = file_name.split('/')
        return 'Chart' in file_name and len(split) == 3

    def convert(self, param_map):
        k = self.k
        v = self.v
        stats = build_stats_param(self.adaptor, param_map, k, v)
        columns = stats.keys()
        header = [f'{k}/{v}'] + list(columns)
        table = []
        for k in stats.keys():
            row = [k]
            values = stats[k]
            for v in columns:
                item = ''
                if v in values:
                    item = values[v]
                row.append(item)
            table.append(row)
        table = [header] + table
        table_format = StatsTableFormat()
        chart_format = StatsChartFormat()
        return table, table_format, chart_format, k, v

