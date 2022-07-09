

class Request:

    def __init__(self):
        self.request_map = {}

    def add_request(self, sid):
        request_map = self.request_map
        request_map[sid] = ''

    def request_cell(self, sheet_id, column, update_range):
        pass

    # sid will be the existing files
    def request_chart(self, sid, sheet_id, chart_id, table, update_mode):
        pass
