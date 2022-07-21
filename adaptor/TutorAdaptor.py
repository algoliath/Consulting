from adaptor.interface.Adaptor import Adaptor
import domain.factory.table.Columns as column_factory


class TutorAdaptor(Adaptor):

    def __init__(self, repository):
        self.repository = repository
        self.columns = column_factory.tutor_table()

    def supports(self, dto, target_columns=''):
        columns = self.columns
        if target_columns:
            columns = target_columns
        for col in columns:
            if col.upper() not in dto:
                return False
        return True

    def handle(self, dto_map, prop_map):
        print(f'dto_map={dto_map}')
        repository = self.repository
        # update target dto
        target_dto_map = {}
        for docs_id in dto_map:
            dto = dto_map[docs_id]
            for data in dto:
                if self.supports(data):
                    target_dto_map[data['TUTOR ID']] = data
        # update repository
        update_dto_map = {}
        save_dto_map = {}
        table = repository.read()
        table_ids = []
        for r in range(len(table)):
            table_ids.append(table[r][0])
        print(f'table_ids={table_ids}')
        for tutor_id in target_dto_map:
            if tutor_id in table_ids:
                update_dto_map[tutor_id] = target_dto_map[tutor_id]
            else:
                save_dto_map[tutor_id] = target_dto_map[tutor_id]
        repository.save(save_dto_map)
        repository.update(update_dto_map)
        print(f'tutor_save_dto_map={save_dto_map}')
        print(f'tutor_update_dto_map={update_dto_map}')
        return True
