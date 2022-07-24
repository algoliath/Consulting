from adaptor.interface.Adaptor import Adaptor
from util.TimeUtil import time_format
import domain.factory.Columns as columnFactory


class DocumentAdaptor(Adaptor):

    def __init__(self, repository, gmail):
        self.repository = repository
        self.columns = columnFactory.docs_table()
        self.gmail = gmail

    def supports(self, dto, target_columns=''):
        columns = self.columns
        if target_columns:
            columns = target_columns
        for col in columns:
            if col.upper() not in dto:
                return False
        return True

    def handle(self, dto_map, prop_map):
        repository = self.repository
        gmail = self.gmail

        # update dto
        target_dto_map = {}
        for docs_id in dto_map:
            dto = dto_map[docs_id]
            prop = prop_map[docs_id]
            if self.supports(dto):
                self.add_to_dto(dto, prop)
                target_dto_map[docs_id] = dto
                if not dto['TIME LOG']:
                    gmail.send_mail(docs_id, dto)

        # update repository
        update_dto_map = {}
        save_dto_map = {}
        table = repository.read()
        table_ids = []
        for r in range(len(table)):
            table_ids.append(table[r][0])
        print(f'table_ids={table_ids}')
        for docs_id in target_dto_map:
            if docs_id in table_ids:
                update_dto_map[docs_id] = target_dto_map[docs_id]
            else:
                save_dto_map[docs_id] = target_dto_map[docs_id]
        print(f'docs_update_dto_map={update_dto_map}')
        print(f'docs_save_dto_map={save_dto_map}')
        repository.save(save_dto_map)
        repository.update(update_dto_map)

    def add_to_dto(self, dto, prop):
        link = prop.get('webViewLink')
        log_start_time, log_end_time = time_format(dto["TIME LOG"], time_format='log')
        modified_time = time_format(prop.get('modifiedTime'), time_format='api')
        dto['TIME LAST MODIFIED'] = str(modified_time[0]) + ':' + str(modified_time[1])
        dto['URL'] = link
        dto['SPENT HOURS'] = int(log_end_time) - int(log_start_time)
