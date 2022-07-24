from adaptor.interface.Adaptor import Adaptor
import domain.factory.Columns as column_factory


class StudentAdaptor(Adaptor):

    def __init__(self, repository):
        self.repository = repository
        self.columns = column_factory.student_table()

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
        update_dto_map = {}
        save_dto_map = {}
        # update target dto
        target_dto_map = {}
        for sid in dto_map:
            dto = dto_map[sid]
            for data in dto:
                if self.supports(data):
                    target_dto_map[data['STUDENT ID']] = data

        print(f'target_dto_map={target_dto_map}')
        # update repository
        table = repository.read()
        table_ids = []
        for r in range(len(table)):
            table_ids.append(table[r][0])

        print(f'table_ids={table_ids}')
        for sid in target_dto_map:
            if sid in table_ids:
                update_dto_map[sid] = target_dto_map[sid]
            else:
                save_dto_map[sid] = target_dto_map[sid]
        repository.save(save_dto_map)
        repository.update(update_dto_map)