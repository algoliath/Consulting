# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Recursively extracts the text from a Google Doc.
"""

import main.googleAPI.util.FilterUtil as Filter
import googleapiclient.discovery as discovery
from httplib2 import Http

DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'


def read_structural_elements(elements, in_table):
    """Recursively search through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
            :param in_table:
            :param elements:
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                if in_table:
                    text += read_paragraph_element(elem)
        if 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'), in_table | True)
        # elif 'tableOfContents' in value:
        #     The text in the TOC is also in a Structural Element.
        #     toc = value.get('tableOfContents')
        #     text += self.read_structural_elements(toc.get('content'))

    return text


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.
        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def update_param(content):
    param = {}
    key_value = content.split("\n")
    print(f'key_value={key_value}')
    for i in range(0, len(key_value)-1, 2):
        k = key_value[i]
        v = key_value[i + 1]
        param[k] = v
        i += 2
    return param


class Docs:

    def __init__(self, cred):
        self.credentials = cred
        self.docs_service = discovery.build('docs', 'v1', http=self.credentials.authorize(Http()),
                                            discoveryServiceUrl=DISCOVERY_DOC)
        self.param_map = {}

    def build_param_map(self, read_file):
        param_map = self.param_map
        try:
            for doc_id in read_file:
                docs = self.docs_service.documents().get(documentId=doc_id)
                body = docs.execute().get('body').get('content')
                content = read_structural_elements(body, False)
                if doc_id not in param_map:
                    param_map[doc_id] = {}
                param_map[doc_id]['content'] = content
        except Exception as error:
            print(f'build_param_map:{error}')
        return param_map

    def update_param_map(self, read_file):
        param_map = self.build_param_map(read_file)
        param_filter = []
        Filter.filter_key(read_file, param_map)
        try:
            for docId in param_map.keys():
                param = update_param(param_map[docId]['content'])
                param_map[docId] = param
                if not param:
                    param_filter.append(docId)
            for docId in param_filter:
                del param_map[docId]
        except Exception as error:
            print(f'update_param_map:{error}')
        return param_map


def main():
    """Uses the Docs API to print out the text of a document."""


if __name__ == '__main__':
    main()
