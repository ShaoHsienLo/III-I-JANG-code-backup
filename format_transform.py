import os
import json
from loguru import logger


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as value_err:
        return False
    return True


read_path = r'C:\Users\samuello\Downloads\III\2022專案\韌性\data'
write_path = r'C:\Users\samuello\Downloads\III\2022專案\韌性\data'
files = os.listdir(read_path)
for file in files:
    logger.info('Formatting {} ...'.format(file))
    with open(os.path.join(read_path, file), 'r') as rf:
        write_filename = file[:-5] + '.txt'
        with open(os.path.join(write_path, write_filename), 'w') as wf:
            lines = rf.readlines()
            for line in lines:
                _line = line[:-2]
                if is_json(_line):
                    wf.write(_line)
                    wf.write('\n')
