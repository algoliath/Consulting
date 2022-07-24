from adaptor.interface.Adaptor import Adaptor
from domain.factory import Columns
import logging as log

log.getLogger("Consultant-Adaptor").setLevel('DEBUG')


class ConsultantAdaptor(Adaptor):

    def __init__(self, repository):
        self.repository = repository
        self.columns = Columns.consultant_table()

    def supports(self, data):
        if len(data) == 0:
            return False
        dto = data[0]
        table_columns = self.columns
        log.info(f'table_columns={table_columns}')
        log.info(f'dto.keys={dto.keys()}')
        for col in table_columns:
            log.info(f'{col} in {dto} = {col in dto}')
            if col not in dto:
                return False
        for col in dto:
            log.info(f'{col} in {table_columns} = {col in table_columns}')
            if col not in table_columns:
                return False
        return True

    def handle(self, dto_map, prop_map):
        repository = self.repository
        # update target dto
        target_dto_map = {}
        for sid in dto_map:
            data = dto_map[sid]
            if self.supports(data):
                log.info(f'data = {data}')
                for dto in data:
                    log.info(f"dto = {dto}")
                    target_dto_map[dto['CONSULTANT ID']] = dto

        # update_repository
        update_dto_map = {}
        save_dto_map = {}
        table = repository.read()
        table_ids = []

        # get entity id
        for r in range(len(table)):
            table_ids.append(table[r][0])
        log.info(f'consultant_ids={table_ids}')

        for consultant_id in target_dto_map:
            log.info(f'consultant_dto={target_dto_map[consultant_id]}')
            if consultant_id in table_ids:
                update_dto_map[consultant_id] = target_dto_map[consultant_id]
            else:
                save_dto_map[consultant_id] = target_dto_map[consultant_id]

        log.info(f'consultant_update_dto_map={update_dto_map}')
        log.info(f'consultant_save_dto_map={save_dto_map}')
        repository.save(save_dto_map)
        repository.update(update_dto_map)
        return True
