import os.path
import logging as log

from googleapiclient.discovery import build

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""


def apply_filter(file_id, cache):
    filter_id = []
    # filter
    for fid in cache:
        if fid not in file_id:
            filter_id.append(fid)
    for fid in filter_id:
        del cache[fid]


def build_drive(cred):
    service = build('drive', 'v3', credentials=cred)
    return service


class Drive:

    def __init__(self, cred):
        # If modifying these scopes, delete the file token.json.
        self.service = build_drive(cred)
        self.read_file = {}
        self.write_file = {}

    def read(self, query, mimetype, mode):
        try:
            if mode == 'batch':
                read_file_id = self.search_files(query)
            else:
                read_file_id = self.search_changed_files(mimetype)
            log.info(f'read_file_id: {read_file_id}')
            return read_file_id
        except Exception as error:
            log.info(f'read_files: {error}')
            raise error

    def update_and_read(self, file_id, mode, mime_type, params='parents, name, id'):
        cache = self.read_file
        try:
            if mime_type == 'sheets':
                cache = self.write_file
            # filter files if batch mode
            if mode == 'batch':
                apply_filter(file_id, cache)
            # inflate files if trigger mode
            for fid in file_id:
                if fid not in cache:
                    file = self.inflate_files(fid, params)
                    cache[fid] = file
            return cache
        except Exception as error:
            log.info(f'update_files={error}')
            raise error

    def create_file(self, file_metadata):
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        log.info('File ID: %s' % file.get('id'))
        return file.get('id')

    def modify_files(self, files, request):
        for file_id in files:
            file = self.service.files().get(fileId=file_id)
            if file:
                file.execute()
            self.service.files().update(fileId=file_id, body=request).execute()

    def search_files(self, query):
        log.info(f'query={query}')
        page_token = None
        files_id = []
        while True:
            response = self.service.files().list(q=query,
                                                 spaces='drive',
                                                 fields='nextPageToken, files(id, name)',
                                                 pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                log.info('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                files_id.append(file.get('id'))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        log.info(f'files_id={files_id}')
        return files_id

    def search_changed_files(self, mime_type):
        drive_service = self.service
        response = drive_service.changes().getStartPageToken().execute()
        page_token = int(response.get('startPageToken')) - 1
        page_token = str(page_token)
        files_id = []
        while True:
            response = drive_service.changes().list(pageToken=page_token,
                                                    spaces='drive',
                                                    ).execute()
            for changes in response.get('changes'):
                # Process change
                if changes.get('file').get('mimeType') == mime_type:
                    log.info('Found file: %s (%s) (mimeType:%s)' % (
                        changes.get('file').get('name'), changes.get('fileId'), changes.get('file').get('mimeType')))
                    files_id.append(changes.get('fileId'))

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return files_id

    def inflate_files(self, file_id, params):
        try:
            file = self.service.files().get(fileId=file_id, fields=params).execute()
            return file
        except RuntimeError as error:
            log.info(f'file inflating error occurred: {error}')

    def create_folder(self, title):
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        log.info('Folder ID: %s' % file.get('id'))
        return file.get('id')

    def move_folder(self, file_id, parents, folder_id):
        # Retrieve the existing parents to remove
        previous_parents = ",".join(parents)
        # Move the file to the new folder
        self.service.files().update(fileId=file_id,
                                    addParents=folder_id,
                                    removeParents=previous_parents,
                                    fields='id, parents').execute()


def main():
    pass


if __name__ == '__main__':
    main()

# deleting files are not recommended
# def delete_file(self, file_id):
#     try:
#         self.service.files().delete(fileId=file_id).execute()
#     except:
#         print('An error occurred')
