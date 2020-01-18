from os import path

from batch_file_processor import BatchFileProcessor
from pdal_outliers.laztile import LazTile
from pdal_outliers.pdalcli import add_height_above_ground, write_info


class PdalHagProcessor(BatchFileProcessor):
    def already_processed(self, file):
        laz = LazTile(f'{self.directory}/{file}')
        height_above_ground_laz = laz.height_above_ground_file()
        is_processed = path.exists(height_above_ground_laz)
        has_info = path.exists(laz.info_file())
        if is_processed and has_info:
            print(f'Skipping already-processed laz {laz}.')
        return is_processed and has_info

    def is_candidate(self, file):
        return file.endswith('.laz') and '_HeightAboveGround' not in file and '_classified_outliers_removed' in file

    def process_file(self, file):
        laz = LazTile(file)
        add_height_above_ground(laz)
        write_info(laz)


if __name__ == '__main__':
    LAZS_DIR = '/home/nick/GIS/datasets/lidarportal.dnr.wa.gov/datasetsA/olympics_south_opsw_2019/laz/outliersremoved'
    PdalHagProcessor(LAZS_DIR).batch_process()
