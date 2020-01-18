from common_utils import directory_of, filename


class LazTile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.directory = directory_of(filepath)
        self.filename = filename(filepath)

    def outliers_classified(self):
        return self.filepath.replace('.laz', '_outliers_classified.laz')

    def classified_outliers_removed(self):
        if '_classified_outliers_removed' in self.filepath:
            return self.filepath
        else:
            return self.filepath.replace('.laz', '_classified_outliers_removed.laz')

    def height_above_ground_file(self):
        return self.classified_outliers_removed().replace('.laz', '_HeightAboveGround.laz')

    def info_file(self):
        return self.height_above_ground_file().replace('.laz', '.json')

    def __str__(self):
        return self.filepath
