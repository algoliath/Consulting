from adaptor.interface.Adaptor import Adaptor
import domain.table.Columns as column_factory


class ConsultantAdaptor(Adaptor):

    def __init__(self, repository):
        self.repository = repository
        self.columns = column_factory.consultant_table()

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
        # update target dto
        target_dto_map = {}
        for docs_id in dto_map:
            dto = dto_map[docs_id]
            for data in dto:
                if self.supports(data):
                    target_dto_map[data['CONSULTANT ID']] = data
        # update repository
        update_dto_map = {}
        save_dto_map = {}
        table = repository.read()
        table_ids = []
        for r in range(len(table)):
            table_ids.append(table[r][0])
        print(f'table_ids={table_ids}')
        for consultant_id in target_dto_map:
            if consultant_id in table_ids:
                update_dto_map[consultant_id] = target_dto_map[consultant_id]
            else:
                save_dto_map[consultant_id] = target_dto_map[consultant_id]
        repository.save(save_dto_map)
        repository.update(update_dto_map)
        print(f'consultant_update_dto_map={update_dto_map}')
        print(f'consultant_save_dto_map={save_dto_map}')
        return True
