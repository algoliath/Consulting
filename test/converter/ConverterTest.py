from datetime import datetime
from converter.PaymentTableConverter import PaymentTableConverter
import util.db_util.DataSource as dbUtils

CURRENT_DATE = str(datetime.now()).split(' ')[0]


class converter_test:

    def __init__(self, converter):
        self.converter = converter

    def update(self, query):
        self.converter.convert(query)


if __name__ == '__main__':
    converter_test = converter_test(
        PaymentTableConverter(connection=dbUtils.getConnection(), current_date=CURRENT_DATE))
    query = "SELECT * FROM CONSULTANT"
    converter_test.update(query)
