class Adaptor:

    def __init__(self):
        pass

    def supports(self, read_params) -> bool:
        pass

    def add_to_dto(self, read_params):
        pass

    def handle(self, read_id, read_file, read_params):
        pass
