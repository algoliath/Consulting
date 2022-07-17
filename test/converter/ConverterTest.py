from datetime import datetime

from converter.PaymentTableConverter import PaymentTableConverter
import database.DataSource as dbUtils

CURRENT_DATE = str(datetime.now()).split(' ')[0]


class converter_test:

    def __init__(self, converter):
        self.converter = converter

    def update(self):
        self.converter.convert()


if __name__ == '__main__':
    converter_test = converter_test(
        PaymentTableConverter(connection=dbUtils.getConnection(), current_date=CURRENT_DATE))
    converter_test.update()
