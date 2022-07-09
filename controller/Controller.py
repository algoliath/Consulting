import time
import datetime
import main.googleAPI.util.FilterUtil as Filter
import main.googleAPI.util.MapUtil as Map

GOOGLE_ACCOUNT = '2016123304@yonsei.ac.kr'

MIMETYPES = ['application/vnd.google-apps.document', 'application/vnd.google-apps.spreadsheet',
             'application/vnd.google-apps.folder']

CURRENT_DATE = str(datetime.datetime.now()).split(' ')[0]
QUERY_READ = f"'{GOOGLE_ACCOUNT}' in writers and mimeType = '{MIMETYPES[0]}'"
QUERY_WRITE = f"'{GOOGLE_ACCOUNT}' in writers and mimeType = '{MIMETYPES[1]}'"
QUERY_LOG_FILE = f"name contains 'Time Log {CURRENT_DATE}' and mimeType = '{MIMETYPES[1]}'"
QUERY_LOG_FOLDER = f"name contains 'Time Log' and mimeType = '{MIMETYPES[2]}'"
LOG_FILE_NAME = 'Time Log'


# helper function to match parameter map to the template requirements
def adapt_helper(read_file, param_map, adaptors):
    # update time log data
    try:
        for read_id in param_map.keys():
            for adaptor in adaptors:
                if adaptor.supports(param_map[read_id]):
                    adaptor.handle(read_id, read_file[read_id], param_map[read_id])
        return param_map
    except Exception as error:
        print(f'batch_read_update:{error}')
        raise error


# helper function to convert parameter map into template form
def convert_helper(sheets, property_map, param_map, converters, chart_update_mode, trigger_update_range):
    # update stats data
    write_file = property_map.keys()
    key = ''
    val = ''
    table_info = {}
    chart_info = {}
    try:
        for sid in write_file:
            title = property_map[sid].get('name')
            print(f'title={title}')
            for converter in converters:
                if converter.support(title):
                    info = converter.convert(param_map)
                    if len(info) == 2:
                        table, table_format = info
                    elif len(info) == 5:
                        table, table_format, chart_format, key, val = info
                    # map table update information
                    table_info = Map.convert_to_map(table=table,
                                                    table_format=table_format,
                                                    n_col=table[0][:1],
                                                    trigger_update_range=trigger_update_range)
                    # map chart update information
                    if key and val:
                        table_info['key'] = key
                        table_info['val'] = val
                        chart_info = Map.convert_to_map(chart_format=chart_format,
                                                        chart_update_mode=chart_update_mode)
                    print(f'table = {table}')
                    print(f'table_info = {table_info}')
                    print(f'chart_info = {chart_info}')
                    # update
                    sheets.update(sid, table_info, chart_info)
                    break
    except Exception as error:
        print(f'batch_write_update:{error}')
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
        # create folder if missing
        if not log_dir:
            log_dir = drive.create_folder(LOG_FILE_NAME)
        # create file if missing
        if not log_file:
            log_dir = log_dir[0] if type(log_dir) == 'list' else log_dir
            drive.create_file({'name': LOG_FILE_NAME + ' ' + CURRENT_DATE, 'mimeType': MIMETYPES[1],
                               'parents': log_dir})

    def run_app(self):
        drive = self.drive
        docs_id = []
        sheets_id = []
        time_end = 10000000
        try:
            for i in range(0, time_end):
                # select mode
                mode = 'batch' if i % 30 == 0 else 'trigger'
                # get docs, sheets files id from the drive
                docs_id = drive.read_files(QUERY_READ, MIMETYPES[0], mode)
                sheets_id = drive.read_files(QUERY_WRITE, MIMETYPES[1], mode)
                self.update(docs_id, sheets_id, drive, read_update_mode=mode, write_update_mode='update')
                time.sleep(20)
        except Exception as error:
            print(f'main_event:{error}')
        finally:
            self.update(docs_id, sheets_id, drive, read_update_mode='batch', write_update_mode='delete')

    def update(self, docs_id, sheets_id, drive, read_update_mode, write_update_mode):
        docs = self.docs
        sheets = self.sheets
        update_range = []
        try:
            read_file = drive.update_and_read_files(docs_id, read_update_mode, 'docs', 'webViewLink, modifiedTime')
            write_file = drive.update_and_read_files(sheets_id, read_update_mode, 'sheets', 'name')
            param_map = docs.update_param_map(docs_id)
            print(f'param_map={param_map}')
            param_map = adapt_helper(read_file, param_map, self.adaptors)
            print(f'param_map={param_map}')
            if read_update_mode == 'trigger':
                update_range = Filter.get_target_index(docs_id, param_map)
            convert_helper(sheets, write_file, param_map, self.converters, write_update_mode, update_range)
        except Exception as error:
            print(f'update:{error}')
            raise error


if __name__ == '__main__':
    pass

# def batch_files_update(drive, param_map):
#     try:
#         drive.update_param_map(param_map)
#         for file_id in param_map.keys():
#             # build parameters
#             name = param_map[file_id]['Student Name']
#             course = param_map[file_id]['Course']
#             file_name = name + "_" + course
#             # update file name
#             target_id = drive.search_files(f"name contains '{file_name}'")
#             if file_id not in target_id:
#                 drive.update_files([file_id], {'name': file_name})
#             target_id = drive.search_files(f"name contains '{file_name}'")
#             # find file id
#             target_file = drive.inflate_files(target_id[0], 'id, name, parents')
#             # get parent file which is a folder
#             parent_id = target_file.get('parents')
#             parent_file = drive.inflate_files(parent_id[0], 'id, name')
#             folder = drive.search_files(f"name contains '{name}' and mimeType = '{MIMETYPES[2]}'")
#             if len(folder) == 0 or not parent_id:
#                 folder = [drive.create_folder(name)]
#             # change the file's directory if the title doesn't match
#             if parent_file.get('name') != target_file.get('name'):
#                 drive.move_folder(file_id, target_file.get('parents'), folder[0])
#
#     except Exception as error:
#         print(f'run time error occurred: {error}')
