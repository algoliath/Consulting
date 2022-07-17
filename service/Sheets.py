from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from util import FilterUtil

TABLE_RANGE = 'A1:300'


def build_sheet(credentials) -> object:
    service = build('sheets', 'v4', credentials=credentials)
    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet


class Sheets:

    def __init__(self, cred):
        self.sheet = build_sheet(cred)

    def get_content(self, sid):
        # Get existing chart id here, if there are not charts, it's left as -1.
        sheet_id = 0
        chart_id = -1
        response = self.sheet.get(spreadsheetId=sid, ranges=[], includeGridData=False).execute()
        sheet_array = response.get('sheets')
        # read charts
        for sheet in sheet_array:
            # if sheet.get('properties').get('title') == title:
            chart_array = sheet.get('charts')
            if chart_array:
                if len(chart_array) != 0:
                    chart_id = chart_array[0].get('chartId')
            sheet_id = sheet.get('properties').get('sheetId')
            break
        return sheet_id, chart_id

    def update_dto_map(self, sheet_ids, dto_map):
        try:
            for sid in sheet_ids:
                result = self.read_cells(sid, dto_map, 'A1:F30')
                print(f'result={result}')
        except Exception as error:
            print(error)
            raise error

    def update(self, sid, table_info, chart_info):
        self.update_format(sid, table_info, chart_info)
        self.update_cells(sid, table_info)

    def update_format(self, sid, table_info, chart_info):
        gid, cid = self.get_content(sid)
        # update info
        table = table_info['table']
        table_format = table_info['table_format']
        n_col = table_info['n_col']

        # optional info
        chart_format = chart_info.get('chart_format')
        chart_mode = chart_info.get('chart_mode')

        # request list
        requests = []

        # update chart format
        if chart_format:
            if chart_mode == 'update':
                requests.append(chart_format.update_chart(gid, cid, table_info))
            if chart_mode == 'delete':
                requests.append(chart_format.delete_chart(cid))

        # update table format
        if table_format:
            requests.append(table_format.table_format(gid))
            trigger_update_id = table_info.get('trigger_update_range')
            for file_id in trigger_update_id:
                requests.append(table_format.update_table(gid, file_id, n_col))

        request_body = {
            'requests': requests
        }
        # update cell formats
        if request_body:
            self.sheet.batchUpdate(
                spreadsheetId=sid,
                body=request_body
            ).execute()

    def update_cells(self, sid, table_info):
        table = table_info['table']
        table_range = f'A1:{len(table)}'
        # clear existing cells
        self.clear_cells(sid, table_range)
        request_body = {
            'values': table
        }
        # update cell values
        result = self.sheet.values().update(
            spreadsheetId=sid,
            range=table_range,
            valueInputOption='RAW',
            body=request_body).execute()
        print('{0} cells updated'.format(result.get("updated cells")))

    def read_cells(self, sid, dto_map, table_range):
        result = self.sheet.values().get(spreadsheetId=sid,
                                         range=table_range).execute()
        values = result.get('values', [])
        if len(values) < 2:
            return

        # read columns from sheet header
        columns = values[0]
        values = values[1:]

        dto_map[sid] = []
        if not values:
            print('No data found.')
            return
        try:
            if not values:
                print('No data found.')
                return
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                i = 0
                dto = {}
                for col in columns:
                    dto[col.upper().strip()] = row[i]
                    i += 1
                dto_map[sid].append(dto)
        except HttpError as err:
            print(err)
        return result

    def clear_cells(self, sid, table_range):
        # delete table cells
        self.sheet.values().clear(
            spreadsheetId=sid,
            range=table_range
        ).execute()


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """


if __name__ == '__main__':
    main()
