import os
from os import path

from pyproj import CRS

from fusion.fusioncli import grid_surface_create, canopy_model, canopy_maxima
from fusion.fusionlidartile import FusionLidarTile

LAZS_DIR = '/home/nick/GIS/datasets/lidarportal.dnr.wa.gov/datasetsA/olympics_south_opsw_2019/laz/outliersremoved'

REPLACEMENTS = {
    #'_outliers_removed_HeightAboveGround': '',
    #'/laz': '/laz/processed'
}


def already_processed(laz):
    canopymaxima_csv = FusionLidarTile(laz, REPLACEMENTS).canopymaxima_csv_actualname()
    is_processed = path.exists(f'{LAZS_DIR}/{canopymaxima_csv}')
    if is_processed:
        print(f'Skipping already-processed laz {laz}.')
    return is_processed


def list_unprocessed_lazs(dir=LAZS_DIR):
    return list(filter(lambda file: file.endswith('.laz') and not already_processed(file), os.listdir(dir)))


if __name__ == '__main__':
    unprocessed = list_unprocessed_lazs()
    for file in unprocessed:
        print(file)

    while len(unprocessed) > 0:
        print(f'{str(len(unprocessed))} laz files remaining')

        laz = FusionLidarTile(f'{LAZS_DIR}/{unprocessed[0]}', REPLACEMENTS, CRS.from_epsg('8791'))
        grid_surface_create(laz)
        canopy_model(laz)
        canopy_maxima(laz)
        unprocessed = list_unprocessed_lazs()