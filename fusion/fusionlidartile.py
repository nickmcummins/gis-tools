import os
from os import path

from common_utils import directory_of, filename


class FusionLidarTile:
    def __init__(self, filepath, to_original=None, known_crs=None):
        self.filepath = filepath
        self.directory = directory_of(filepath)
        self.filename = filename(filepath)
        self.to_original = to_original
        if known_crs is not None:
            self.projcrs = known_crs.sub_crs_list[0]
            self.vertcrs = known_crs.sub_crs_list[1]

    def original(self):
        original = self.filepath
        for replacestr in self.to_original.keys():
            replaceval = self.to_original[replacestr]
            original = original.replace(replacestr, replaceval)
        return original

    def as_las(self):
        lasfile = f"/tmp/{self.filename.replace('.laz', '.las')}"
        if not path.exists(lasfile):
            out = os.popen(f'las2las -i {self.filepath} -o {lasfile}').read()
        return lasfile

    def rm_tmp_lasfile(self):
        os.remove(self.as_las())
        print(f'Removed {self.as_las()}.')

    def horizdatum(self):
        if '1983' in self.projcrs.datum.name:
            return '2'
        else:
            return '0'

    def vertdatum(self):
        if '1988' in self.vertcrs.datum.name:
            return '2'
        else:
            return '0'

    def coordsys(self):
        if 'utm' in self.projcrs.name.lower():
            return '1'
        elif 'washington' in self.projcrs.name.lower():
            return '2'
        else:
            return '0'

    def xyunits(self):
        if self.projcrs.axis_info[0].unit_conversion_factor < 1.0:
            return 'F'
        else:
            return 'M'

    def zunits(self):
        if self.vertcrs.axis_info[0].unit_conversion_factor < 1.0:
            return 'F'
        else:
            return 'M'

    def groundsurfacemodel(self):
        surfacefile = self.filepath
        for replacestr in self.to_original.keys():
            replaceval = self.to_original[replacestr]
            if len(replaceval) == 0:
                surfacefile = surfacefile.replace(replacestr, replaceval)
        ext = surfacefile.split('.')[-1]
        surfacefile = surfacefile.replace(f'.{ext}', '_Ground.dtm')
        return surfacefile

    def canopysurfacemodel(self):
        return self.groundsurfacemodel().replace('_Ground', '_Canopy')

    def canopymaxima_csv_createname(self):
        return self.canopysurfacemodel().replace('_Canopy.dtm', '_CanopyMaxima.csv')

    def canopymaxima_csv_actualname(self):
        return self.canopymaxima_csv_createname().replace('_CanopyMaxima', '_CanopyMaxima_treelist')