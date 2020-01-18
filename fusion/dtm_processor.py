import os
from os import path

from common_utils import directory_of, filename


class DtmTile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.directory = directory_of(filepath)
        self.filename = filename(filepath)

    def dtmdescribe_csv(self):
        return self.filepath.replace('.dtm', '.csv')


DTM_DIR = ''

def already_processed(dtm):
    dtmdescribe_csv = DtmTile(dtm).dtmdescribe_csv()
    is_processed = path.exists(dtmdescribe_csv)
    if is_processed:
        print(f'Skipping alredy-processed DTM {dtm}.')
    return is_processed

def list_unprocessed_dtms(dir=DTM_DIR):
    return list(filter(lambda file: file.endswith('.dtm') and not already_processed(file), os.listdir(dir)))

if __name__ == '__main__':
    unprocessed = list_unprocessed_dtms()
    for file in unprocessed:
        print(file)

    while len(unprocessed) > 0:
        print(f'{str(len(unprocessed))} dtm files remaining')

        dtmtile = DtmTile(f'{DTM_DIR}/{unprocessed[0]}')
        unprocessed = list_unprocessed_dtms()