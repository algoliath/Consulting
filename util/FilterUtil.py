def filter_id(filter_id, filter_map):
    target_id = []
    for file_id in filter_id:
        if file_id in filter_map:
            target_id.append(file_id)
    return target_id


def filter_key(filter_id, filter_map):
    remove = []
    for file_id in filter_map.keys():
        if file_id not in filter_id:
            remove.append(file_id)
    for file_id in remove:
        del filter_map[file_id]