from datetime import datetime

from converter.PaymentTableConverter import PaymentTableConverter
import util.db_util.DataSource as dbUtils
from converter.StatsTableConverter import StatsTableConverter

CURRENT_DATE = str(datetime.now()).split(' ')[0]


class converter_test:

    def __init__(self, converter):
        self.converter = converter

    def update(self):
        self.converter.convert()


if __name__ == '__main__':
    converter_test = converter_test(
        StatsTableConverter('Package', 'Apps', connection=dbUtils.getConnection()))
    converter_test.update()
