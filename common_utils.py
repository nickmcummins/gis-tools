import os
import subprocess


def list_unprocessed(basedir):
    return list(map(lambda unprocessed: f'{basedir}/{unprocessed}',
                    filter(lambda file: 'processed' not in file, os.listdir(basedir))))


def mv_processed(file):
    parts = file.split('/')
    file_processed = '/'.join(parts[0:len(parts) - 1]) + '/processed/' + parts[len(parts) - 1]
    print(f'Moving {file} to {file_processed} ...')
    os.popen(f'mv {file} {file_processed}').read()
    return file_processed


def directory_of(filepath):
    parts = filepath.split('/')
    return '/'.join(parts[0:len(parts) - 1])


def filename(filepath):
    parts = filepath.split('/')
    return parts[len(parts) - 1]


def to_windows_path(filepath):
    return 'Z:' + filepath.replace('/', "\\")


def run(cmd):
    print(f'Executing {cmd}')
    res = subprocess.run(cmd.split(' '))
    print(res)
    return res
