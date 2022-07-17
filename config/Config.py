from datetime import datetime

from adaptor.ConsultantAdaptor import ConsultantAdaptor
from adaptor.DocumentAdaptor import DocumentAdaptor
from adaptor.StudentAdaptor import StudentAdaptor
from adaptor.TutorAdaptor import TutorAdaptor
from converter.PaymentTableConverter import PaymentTableConverter
from converter.TimeTableConverter import TimeTableConverter
from controller.Controller import Controller
from repo.ConsultantRepository import ConsultantRepository
from repo.StudentRepository import StudentRepository
from service.Drive import Drive
from service.Gmail import Gmail
from service.Sheets import Sheets
from service.Docs import Docs
from repo.DocsRepository import DocsRepository
from repo.TutorRepository import TutorRepository
from database.DataSource import getConnection
from auth.credentials import get_credentials

CURRENT_DATE = str(datetime.now()).split(' ')[0]
CREDENTIALS = get_credentials()
DB_CONNECTION = getConnection()
REPOSITORY = [DocsRepository(DB_CONNECTION), StudentRepository(DB_CONNECTION),
              TutorRepository(DB_CONNECTION), ConsultantRepository(DB_CONNECTION)]
ADAPTORS = [DocumentAdaptor(REPOSITORY[0], Gmail(CREDENTIALS)), StudentAdaptor(REPOSITORY[1]),
            TutorAdaptor(REPOSITORY[2]), ConsultantAdaptor(REPOSITORY[3])]
CONVERTERS = [TimeTableConverter(REPOSITORY[0], CURRENT_DATE), PaymentTableConverter(DB_CONNECTION, CURRENT_DATE)]

""" alternative (web driver instead of Google API)
from service.Web import Web
QUERY_WEB_READ = "docs-homescreen-grid-item-thumbnail"
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
