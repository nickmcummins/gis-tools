import json
import os
import subprocess
from os import path

from pyproj import CRS

from common_utils import to_windows_path, run

CELL_SIZE = '1'
ZONE = '0'
FUSION_DIR = '/home/nick/.wine/drive_c/FUSION'

def grid_surface_create(laz):
    gridsurfacecreate_exe = to_windows_path(f'{FUSION_DIR}/GridSurfaceCreate.exe')
    ground_dtm = to_windows_path(laz.groundsurfacemodel())
    lasfile = to_windows_path(laz.as_las())

    if not path.exists(laz.groundsurfacemodel()):
        run(f'wine64 {gridsurfacecreate_exe} {ground_dtm} {CELL_SIZE} {laz.xyunits()} {laz.zunits()} {laz.coordsys()} {ZONE} {laz.horizdatum()} {laz.vertdatum()} {lasfile}')
    else:
        print(f'Skipping creation of already existing ground surface model {laz.groundsurfacemodel()}.')


def canopy_model(laz):
    canopymodel_exe = to_windows_path(f'{FUSION_DIR}/CanopyModel.exe')
    ground_dtm = to_windows_path(laz.groundsurfacemodel())
    canopy_dtm = to_windows_path(laz.canopysurfacemodel())
    lasfile = to_windows_path(laz.as_las())

    if not path.exists(laz.canopysurfacemodel()):
        run(f'wine64 {canopymodel_exe} /ground:{ground_dtm} {canopy_dtm} {CELL_SIZE} {laz.xyunits()} {laz.zunits()} {laz.coordsys()} {ZONE} {laz.horizdatum()} {laz.vertdatum()} {lasfile}')
    else:
        print(f'Skipping creation of already existing canopy surface model {laz.canopysurfacemodel()}.')
    laz.rm_tmp_lasfile()


def canopy_maxima(laz):
    canopymodel_exe = to_windows_path(f'{FUSION_DIR}/canopymaxima.exe')
    canopy_dtm = to_windows_path(laz.canopysurfacemodel())
    canopymaxima_csv = to_windows_path(laz.canopymaxima_csv_createname())

    if not path.exists(laz.canopymaxima_csv_actualname()):
        run(f'wine64 {canopymodel_exe} /threshold:290 {canopy_dtm} {canopymaxima_csv}')
    else:
        print(f'Skipping creation of already existing canopy maxima file {laz.canopymaxima_csv_createname()}.')


def dtm_describe(dtm):
    dtmdescribe_exe = to_windows_path(f'{FUSION_DIR}/DTMDescribe.exe')
    dtmdescribe_csv = to_windows_path(dtm.dtmdescribe_csv())
    if not path.exists(dtmdescribe_csv):
        return run(f'wine64 {dtmdescribe_exe} {to_windows_path(dtm)} {dtmdescribe_csv}')
    else:
        print(f'Skipping creationg of already existing DTM csv file {dtmdescribe_csv}')


def describe_dtms(dtm_dir):
    dtms = list(filter(lambda file: file.endswith('.dtm'), os.listdir(dtm_dir)))
    for dtm in dtms:
        dtm_describe(dtm)



