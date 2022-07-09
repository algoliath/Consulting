def get_target_index(filter_id, filter_map):
    i = 0
    target_range = []
    indices = {}
    for doc_id in filter_map.keys():
        indices[doc_id] = i
        i += 1
    for doc_id in filter_id:
        target_range.append(indices[doc_id])
    return target_range


def filter_key(filter_id, filter_map):
    remove = []
    for doc_id in filter_map.keys():
        if doc_id not in filter_id:
            remove.append(doc_id)
    for doc_id in remove:
        del filter_map[doc_id]