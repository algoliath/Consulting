import datetime
from main.googleAPI.service.Request import Request
from main.googleAPI.service.Service import Service
from main.googleAPI.service.Drive import Drive
from main.googleAPI.service.Sheets import Sheets
from main.googleAPI.service.Docs import Docs
from main.googleAPI.service.Gmail import Gmail
from main.googleAPI.auth.credentials import get_credentials
from main.googleAPI.service.Web import Web
import undetected_chromedriver as uc

CREDENTIALS = get_credentials()
CURRENT_DATE = str(datetime.datetime.now()).split(' ')[0]
MIMETYPES = ['application/vnd.google-apps.document', 'application/vnd.google-apps.spreadsheet',
             'application/vnd.google-apps.folder']
QUERY_LOG_FILE = f"name contains 'Time Log {CURRENT_DATE}' and mimeType = '{MIMETYPES[1]}'"
QUERY_LOG_FOLDER = f"name contains 'Time Log' and mimeType = '{MIMETYPES[2]}'"
QUERY_WEB_READ = "docs-homescreen-grid-item-thumbnail"
ENTITIES = ['Student Name', 'Tutor', 'Email', 'Course', 'Time Log']

LOG_TABLE_KEYS = ['Student Name', 'Tutor', 'Email', 'Date', 'Course', 'Package', 'Time Log', 'Review',
                  'Last Modified Time', 'URL']
DOCS_KEYS = ["Student Name", "Tutor", "Email", "Date", "Course", "Package", "Time Log", "Review"]
DOCS_MAIN_KEYS = ["Student Name", "Tutor", "Email", "Date", "Course", "Package"]


def build_app():
    # connect to web driver
    # wb = Web(uc.Chrome(), QUERY_WEB_READ)
    # read_file_id = wb.crawl("/d", "=w")
    # import drive and mail
    dr = Drive(cred=CREDENTIALS)
    gm = Gmail(cred=CREDENTIALS)
    # import docs and sheets
    dc = Docs(cred=CREDENTIALS, docs_key=DOCS_KEYS, docs_main_key=DOCS_MAIN_KEYS)
    sh = Sheets(cred=CREDENTIALS, req=Request(), log_table_keys=LOG_TABLE_KEYS)
    # call service app
    se = Service(dc, sh, dr, gm, QUERY_LOG_FOLDER, QUERY_LOG_FILE, CURRENT_DATE)
    return dc, sh, dr, se


class Config:
    def __init__(self, dc, sr):
        sr.event_run(dc)
        # generate files test


if __name__ == '__main__':
    docs, sheets, drive, service = build_app()
    test_config = Config(docs, service)


def create_files_test(docs, drive):
    file_id = []
    for i in range(5):
        file_map = []
        fid = drive.create_file({'name': i, 'mimeType': MIMETYPES[0]})
        for entity in ENTITIES:
            key, val = [f'{entity}', f'{entity}_{i}']
            if entity == 'Time Log':
                val = time_util.time_random()
            file_sub_map = [key, val]
            file_map.append(file_sub_map)
        docs.create_table(fid, file_map)
        file_id.append(fid)


def insert_table(self, docs_id):
    requests = ''
    self.docs_service.documents().batchUpdate(documentId=docs_id,
                                              body={'requests': requests}).execute()
