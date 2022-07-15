from datetime import datetime
from adaptor.TimeTableAdaptor import TimeTableAdaptor
from converter.TimeTableConverter import TimeTableConverter
from controller.Controller import Controller
from service.Drive import Drive
from service.Sheets import Sheets
from service.Docs import Docs
from repo.DocsRepository import DocsRepository
from database.DBUtils import getConnection
from auth.credentials import get_credentials

from service.Web import Web

# QUERY_WEB_READ = "docs-homescreen-grid-item-thumbnail"

CURRENT_DATE = str(datetime.now()).split(' ')[0]
CREDENTIALS = get_credentials()
REPOSITORY = [DocsRepository(getConnection())]
ADAPTORS = [TimeTableAdaptor(REPOSITORY[0], CREDENTIALS)]
CONVERTERS = [TimeTableConverter(REPOSITORY[0], CURRENT_DATE)]

""" alternative (web driver instead of Google API)
connect to web driver
wb = Web(uc.Chrome(), QUERY_WEB_READ)
read_file_id = wb.crawl("/d", "=w")
"""


def build_app():
    dc = Docs(cred=CREDENTIALS)
    sh = Sheets(cred=CREDENTIALS)
    dr = Drive(cred=CREDENTIALS)
    # call service app
    se = Controller(dc, sh, dr, ADAPTORS, CONVERTERS)
    return dc, sh, dr, se


class Config:
    def __init__(self, sr):
        sr.daemon_process()
        # generate files test


if __name__ == '__main__':
    docs, sheets, drive, service = build_app()
    test_config = Config(service)
