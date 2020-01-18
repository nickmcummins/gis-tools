import json
import os
from os import path

from common_utils import run
import pdal


def remove_classified_outliers(laz):
    remove_classified_outliers_pipeline = """
    [
        {
            "type": "readers.las", 
            "compression": "laszip", 
            "filename": "%s"
        },
        {
            "type": "filters.range",
            "limits": "Classification![7:7],ClassFlags![8:8]"
        },
        {  
            "type": "writers.las", 
            "compression": "laszip", 
            "minor_version": "4",
            "filename": "%s",
            "forward": "all",
            "extra_dims": "all"
        }
    ]""" % (laz.filepath, laz.classified_outliers_removed())
    run_pipeline(remove_classified_outliers_pipeline, laz, 'remove classified outliers')


def classify_outliers(laz, mean_k='8', multiplier='2.0'):
    classify_outliers_pipeline = """
    [
        {
            "type": "readers.las", 
            "compression": "laszip", 
            "filename": "%s"
        },
        {
            "type":"filters.outlier",
            "method":"statistical",
            "mean_k":%s,
            "multiplier":%s
        },
        {
            "type": "filters.range",
            "limits": "Classification![7:7]"
        },
        {  
            "type": "writers.las", 
            "compression": "laszip", 
            "minor_version": "4",
            "filename": "%s",
            "forward": "all",
            "extra_dims": "all"
        }
    ]""" % (laz.filepath, mean_k, multiplier, laz.outliers_classified())
    run_pipeline(classify_outliers_pipeline, laz, 'filter outliers')


def add_height_above_ground(laz):
    hag_pipeline = """
    [
        {
            "type": "readers.las", 
            "compression": "laszip", 
            "filename": "%s"
        },
        {
            "type":"filters.hag"
        },
        {  
            "type": "writers.las", 
            "compression": "laszip", 
            "minor_version": "4",
            "filename": "%s",
            "forward": "all",
            "extra_dims": "all"
        }
    ]""" % (laz.filepath, laz.height_above_ground_file())

    run_pipeline(hag_pipeline, laz, 'add HeightAboveGround')


def laz_to_txt(laz,fields='HeightAboveGround', delim='\t'):
    txt_pipeline = """
    [
        {
            "type": "readers.las",
            "compression": "laszip",
            "filename": "%s"
        },
        {
            "type": "writers.text",
            "order": "%s",
            "keep_unspecified": "false",
            "delimiter": "%s",
            "filename":"%s"
        }
    ]""" % (laz, fields, delim, laz.replace('.laz', '_HeightAboveGround.txt'))
    run_pipeline(txt_pipeline, laz, 'convert to txt')


def run_pipeline(pipelinejson, laz, description):
    output_file = json.loads(pipelinejson)[-1]['filename']
    if path.exists(output_file):
        print(f'Skipping creation of already existing file {output_file}.')
    else:
        pipeline = pdal.Pipeline(pipelinejson)
        pipeline.validate()
        pipeline.loglevel = 8
        print(f'Executing {description} on {laz.filepath}.')
        pipeline.execute()
        print(f'Wrote {output_file}.')


def write_info(laz):
    if not path.exists(laz.info_file()):
        info = os.popen(f'pdal info {laz.height_above_ground_file()}').read()
        with open(laz.info_file(), 'w') as f:
            f.write(info)
    else:
        print(f'Skipping creation of already existing info file {laz.info_file()}.')


def info_summary(lazfile):
    summary = str(run(f'pdal info --summary {lazfile}'), 'utf-8')
    wkt = json.loads(summary)['summary']['srs']['wkt']
    #CRS.from_wkt(wkt)
    return summary
