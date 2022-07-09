class BasicTableFormat:
    # table
    def table_format(self, param_map):
        m = len(param_map)
        # create table
        requests = [{
            'insertTable': {
                'rows': 5,
                'columns': 2,
                'location': {
                    "index": 1
                }
            }
        }]
        # insert table
        for row in reversed(range(m)):
            docs_text = param_map[row]
            index = 5 * (row + 1)
            for col in reversed(range(len(docs_text))):
                col_index = index + 2 * col
                insert_value = {
                    "insertText":
                        {
                            "text": docs_text[col],
                            "location":
                                {
                                    "index": col_index
                                }
                        }
                }
                requests.append(insert_value)
        return requests
