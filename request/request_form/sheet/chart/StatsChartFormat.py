from request.request_form.sheet.chart.BasicChartFormat import BasicChartFormat


def is_valid(table, col):
    for j in range(1, len(table), 1):
        print(f'table row {j} col {col}: {table[j][col]}')
        if table[j][col]:
            return True
    print()
    return False


def get_series(table, col):
    series = []
    for c in col:
        if is_valid(table, col):
            series.append({"series": {
                "sourceRange": {
                    "sources": [
                        {
                            "sheetId": 0,
                            "startColumnIndex": c + 1,
                            "endColumnIndex": c + 2
                        }
                    ]
                }
            }})
    return series


class StatsChartFormat(BasicChartFormat):

    def __init__(self, chart_type):
        self.chart_type = chart_type

    # line charts
    def chart_format(self, k, v, col):
        series = get_series(col)
        chart_type = self.chart_type
        spec = {
            "title": f"Relational Database({k}/{v})",
            chart_type: {
                "chartType": "COLUMN",
                "legendPosition": "LABELED_LEGEND",
                "threeDimensional": "true",
                "domain": {
                    "sourceRange": {
                        "sources": [
                            {
                                "sheetId": 0,
                                "startColumnIndex": 0,
                                "endColumnIndex": 1
                            }
                        ]
                    }
                },
                "series": series
            }
        }
        return spec

    def add_chart(self, k, v, sheet_id, n_row, col):
        chart = {
            "addChart": {
                "chart": {
                    "spec": self.chart_format(k, v, col),
                    "position": {
                        "overlayPosition": {
                            "anchorCell": {
                                "sheetId": sheet_id,
                                "rowIndex": n_row + 1,
                                "columnIndex": 0
                            },
                            "offsetXPixels": 50,
                            "offsetYPixels": 50
                        }
                    }
                }
            }
        }
        return chart

    def update_chart(self, sheet_id, chart_id, table_info):
        k = table_info['key']
        v = table_info['val']
        n_row = table_info['n_row']
        n_col = table_info['n_col']
        chart_update = []
        if chart_id == -1:
            chart_update.append(self.add_chart(k, v, sheet_id, n_row, [col for col in range(n_col)]))
            chart_update.append({"updateChartSpec": {
                "chartId": chart_id,
                "spec": self.chart_format(k, v, [col for col in range(n_col)])
            }})
        return chart_update

    def delete_chart(self, chart_id):
        chart_delete = {
            "deleteEmbeddedObject": {
                "objectId": chart_id
            }
        }
        return chart_delete
