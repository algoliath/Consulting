import time
import datetime
import util.FilterUtil as Filters
import util.MapUtil as Mapping

GOOGLE_ACCOUNT = '2016123304@yonsei.ac.kr'

MIMETYPES = ['application/vnd.google-apps.document', 'application/vnd.google-apps.spreadsheet',
             'application/vnd.google-apps.folder']

CURRENT_DATE = str(datetime.datetime.now()).split(' ')[0]
QUERY_DOCS = f"'{GOOGLE_ACCOUNT}' in writers and mimeType = '{MIMETYPES[0]}'"
QUERY_SHEETS = f"'{GOOGLE_ACCOUNT}' in writers and mimeType = '{MIMETYPES[1]}'"
QUERY_LOG_FILE = f"name contains 'Time Log {CURRENT_DATE}' and mimeType = '{MIMETYPES[1]}'"
QUERY_LOG_FOLDER = f"name contains 'Time Log' and mimeType = '{MIMETYPES[2]}'"
LOG_FILE_NAME = 'Time Log'


# helper function to match parameter map to the template requirements
def read_helper(prop_map, dto_map, adaptors):
    # update time log data
    try:
        for adaptor in adaptors:
            adaptor.handle(dto_map, prop_map)
        return dto_map
    except Exception as error:
        print(f'read_update:{error}')
        raise error


# helper function to convert parameter map into template form
def write_helper(sheets, property_map, converters, chart_update_mode, trigger_update_range):
    write_file = property_map.keys()
    key = ''
    val = ''
    chart_info = {}
    try:
        for sid in write_file:
            title = property_map[sid].get('name')
            for converter in converters:
                if converter.support(title):
                    info = converter.convert()
                    if len(info) == 2:
                        table, table_format = info
                    else:
                        table, table_format, chart_format, key, val = info
                    # mapping table update information
                    table_info = Mapping.convert_to_map(table=table,
                                                        table_format=table_format,
                                                        n_col=table[0][:1],
                                                        trigger_update_range=trigger_update_range)
                    # mapping chart update information
                    if key and val:
                        table_info['key'] = key
                        table_info['val'] = val
                        chart_info = Mapping.convert_to_map(chart_format=chart_format,
                                                            chart_update_mode=chart_update_mode)
                    print(f'table = {table}')
                    print(f'table_info = {table_info}')
                    print(f'chart_info = {chart_info}')
                    # update
                    sheets.update(sid, table_info, chart_info)
                    break
    except Exception as error:
        print(f'write_update:{error}')
        raise error


class Controller:

    def __init__(self, docs, sheets, drive, adaptors, converters):
        # declare main variables
        self.docs = docs
        self.drive = drive
        self.sheets = sheets
        self.adaptors = adaptors
        self.converters = converters
        # get data from google drive api(should be sync )
        log_dir = drive.search_files(QUERY_LOG_FOLDER)
        log_file = drive.search_files(QUERY_LOG_FILE)
        # create log folder if missing
        if not log_dir:
            log_dir = drive.create_folder(LOG_FILE_NAME)
        # create log file if missing
        if not log_file:
            log_dir = log_dir[0] if type(log_dir) == 'list' else log_dir
            drive.create_file({'name': LOG_FILE_NAME + ' ' + CURRENT_DATE, 'mimeType': MIMETYPES[1],
                               'parents': log_dir})

    def daemon_process(self):
        drive = self.drive
        doc_ids = []
        sheet_ids = []
        time_end = 10000000
        try:
            for i in range(0, time_end):
                # select mode
                mode = 'batch' if i % 30 == 0 else 'trigger'
                # get docs, sheets files id from the drive
                doc_ids = drive.read(QUERY_DOCS, MIMETYPES[0], mode)
                sheet_ids = drive.read(QUERY_SHEETS, MIMETYPES[1], mode='batch')
                self.update(doc_ids, sheet_ids, read_mode=mode, write_mode='update')
                time.sleep(20)
        except Exception as error:
            print(f'main_event:{error}')
        finally:
            self.update(doc_ids, sheet_ids, read_mode='batch', write_mode='delete')

    def update(self, doc_ids, sheet_ids, read_mode, write_mode):
        docs = self.docs
        drive = self.drive
        sheets = self.sheets
        target_ids = []
        sheets_dto_map = {}
        try:
            # get file properties
            docs_prop_map = drive.update_and_read(doc_ids, read_mode, 'docs', params='webViewLink,modifiedTime')
            sheets_prop_map = drive.update_and_read(sheet_ids, read_mode,'sheets', params='name')
            # get parameters
            docs_dto_map = docs.update_dto_map(doc_ids)
            # add parameters -> dto
            docs_dto_map = read_helper(docs_prop_map, docs_dto_map, self.adaptors)
            if read_mode == 'trigger':
                target_ids = Filters.filter_id(doc_ids, docs_dto_map)
            sheets.update_dto_map(sheet_ids, sheets_dto_map)
            print(f'sheets_dto_map={sheets_dto_map}')
            read_helper(sheets_prop_map, sheets_dto_map, self.adaptors)
            # convert dto into table
            write_helper(sheets, sheets_prop_map, self.converters, write_mode, target_ids)
        except Exception as error:
            print(f'update:{error}')
            raise error


if __name__ == '__main__':
    pass

