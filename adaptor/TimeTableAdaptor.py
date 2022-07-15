from adaptor.Adaptor import Adaptor
from service.Gmail import Gmail

import util.TimeUtil as TimeUtil
import domain.table.ColumnFactory as columnFactory


# send email if log absent
def send_mail(gmail, docs_id, dto):
    try:
        if not gmail.message_sent(docs_id):
            message = gmail.create_message("2016123304@yonsei.ac.kr", dto['Email'],
                                           "Log missing", f"google docs link-{dto['URL']}")
            gmail.send_message("me", docs_id, message)
            print(f"Messages sent to {dto['Email']}")
    except Exception as error:
        print(f'send_email:{error}')
        raise error


class TimeTableAdaptor(Adaptor):

    def __init__(self, docs_repository, gmail_cred):
        self.repo = docs_repository
        self.columns = columnFactory.time_table()
        self.gmail = Gmail(gmail_cred)

    def supports(self, read_params, target_columns=''):
        columns = self.columns
        if target_columns:
            columns = target_columns
        for col in columns:
            if col not in read_params:
                return False
        return True

    def validates(self, read_params, target_columns=''):
        columns = self.columns
        if target_columns:
            columns = target_columns
        for col in columns:
            if not read_params[col]:
                return False
        return True

    def handle(self, dto_map, prop_map):
        gmail = self.gmail
        target_dto_map = {}
        for docs_id in dto_map:
            dto = dto_map[docs_id]
            if self.supports(dto) and self.validates(dto):
                link = prop_map.get('webViewLink')
                time = TimeUtil.time_regex(prop_map.get('modifiedTime'), time_format='api')
                dto_map['TimeLastModified'] = str(time[0]) + ':' + str(time[1])
                dto_map['URL'] = link
                target_dto_map[docs_id] = dto
            else:
                if self.supports(dto, 'Time Log') and self.validates(dto, 'Time Log'):
                    send_mail(gmail, docs_id, dto)
        self.repo.save(target_dto_map)
