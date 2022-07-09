from main.googleAPI.request.request_form.sheet.table.BasicTableFormat import BasicTableFormat


class LogTableFormat(BasicTableFormat):

    def __init__(self):
        pass

    def table_format(self, sheet_id):
        formats = [{
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS"
                },
                "properties": {
                    "pixelSize": 2500
                },
                "fields": "pixelSize"
            },
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS"
                },
                "properties": {
                    "pixelSize": 30
                },
                "fields": "pixelSize"
            }
        }]
        return formats

    def update_table(self, sheet_id, row, n_col):
        ranges = [{
            "sheetId": sheet_id,
            "startRowIndex": row,
            "startColumnIndex": col_index
        } for col_index in range(n_col)]
        formats = [{
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.1,
                                "green": 0.3,
                                "blue": 0.8
                            }
                        }
                    }]
                }],
                "range": r,
                "fields": "*"
            }} for r in ranges]
        return formats



