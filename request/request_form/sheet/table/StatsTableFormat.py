from main.googleAPI.request.request_form.sheet.table.BasicTableFormat import BasicTableFormat


class StatsTableFormat(BasicTableFormat):

    def __init__(self, sheet_id, chart_id):
        self.sheet_id = sheet_id
        self.chart_id = chart_id
        pass

    def cell_format(self):
        pass

    def chart_format(self):
        pass
