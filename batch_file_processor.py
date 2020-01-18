import os
from abc import ABC, abstractmethod


class BatchFileProcessor(ABC):
    def __init__(self, directory):
        self.directory = directory

    @abstractmethod
    def already_processed(self, file):
        ...

    @abstractmethod
    def is_candidate(self, file):
        ...

    @abstractmethod
    def process_file(self, file):
        ...

    def list_unprocessed(self):
        return list(filter(lambda file: self.is_candidate(file) and not self.already_processed(file), os.listdir(self.directory)))

    def batch_process(self):
        unprocessed = self.list_unprocessed()
        for file in unprocessed:
            print(file)

        while len(unprocessed) > 0:
            print(f'{str(len(unprocessed))} files remaining')

            self.process_file(f'{self.directory}/{unprocessed[0]}')
            unprocessed = self.list_unprocessed()