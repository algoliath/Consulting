from datetime import datetime
from main.googleAPI.adaptor.TimeLogAdaptor import TimeLogAdaptor
from main.googleAPI.controller.Controller import Controller
from main.googleAPI.converter.StatsTableConverter import StatsTableConverter
from main.googleAPI.converter.TimeLogTableConverter import TimeLogTableConverter
from main.googleAPI.service.Drive import Drive
from main.googleAPI.service.Sheets import Sheets
from main.googleAPI.service.Docs import Docs
from main.googleAPI.auth.credentials import get_credentials
from main.googleAPI.service.Web import Web
import undetected_chromedriver as uc

# QUERY_WEB_READ = "docs-homescreen-grid-item-thumbnail"
CREDENTIALS = get_credentials()
LOG_TABLE_KEYS = ['Student Name', 'Tutor', 'Email', 'Date', 'Course', 'Package', 'Time Log', 'Review',
                  'Last Modified Time', 'URL']
ADAPTORS = [TimeLogAdaptor(CREDENTIALS)]
CURRENT_DATE = str(datetime.now()).split(' ')[0]
CONVERTERS = [TimeLogTableConverter(ADAPTORS[0], CURRENT_DATE)]


def build_app():
    # connect to web driver
    # wb = Web(uc.Chrome(), QUERY_WEB_READ)
    # read_file_id = wb.crawl("/d", "=w")
    # import docs, sheets and drive
    dc = Docs(cred=CREDENTIALS)
    sh = Sheets(cred=CREDENTIALS)
    dr = Drive(cred=CREDENTIALS)
    # call service app
    se = Controller(dc, sh, dr, ADAPTORS, CONVERTERS)
    return dc, sh, dr, se


class Config:
    def __init__(self, sr):
        sr.run_app()
        # generate files test


if __name__ == '__main__':
    docs, sheets, drive, service = build_app()
    test_config = Config(service)
