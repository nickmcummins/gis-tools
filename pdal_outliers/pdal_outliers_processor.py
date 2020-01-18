from os import path

from batch_file_processor import BatchFileProcessor
from pdal_outliers.laztile import LazTile
from pdal_outliers.pdalcli import remove_classified_outliers


class PdalOutliersProcessor(BatchFileProcessor):
    def already_processed(self, file):
        classified_outliers_removed_laz = LazTile(f'{self.directory}/{file}').classified_outliers_removed()
        is_processed = path.exists(classified_outliers_removed_laz)
        if is_processed:
            print(f'Skipping already-processed laz {file}.')
        return is_processed

    def is_candidate(self, file):
        return file.endswith('.laz') and '_classified_outliers_removed' not in file

    def process_file(self, file):
        laz = LazTile(file)
        remove_classified_outliers(laz)


if __name__ == '__main__':
    LAZS_DIR = '/home/nick/GIS/datasets/lidarportal.dnr.wa.gov/datasetsA/olympics_south_opsw_2019/laz'
    PdalOutliersProcessor(LAZS_DIR).batch_process()
