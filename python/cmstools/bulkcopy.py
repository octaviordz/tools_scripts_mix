import os
import sys
import shutil
import datetime
import os
import stat
import logging
import datetime
import re


always_replace = False
#source folder
source = '/home/orc/Music/Within Temptation - Enter'
destinations = """
/home/orc/Documents/tmp/1
/home/orc/Documents/tmp/
"""

LOG_FILENAME = str(datetime.date.today())+'-bulkcopy.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)


def safe_mkdir(dst):
    try:
        os.makedirs(dst)
    except IOError as ex:
        log.error('%s' % ex)
    
def safe_copy(src, dst):
    if os.path.exists(dst) and not always_replace:
        return
    try:
        fileattr = None
        if os.path.exists(dst):
            fileattr = os.stat(dst)[0]
        if fileattr and (not fileattr & stat.S_IWRITE):
           os.chmod(dst, stat.S_IWRITE)
        shutil.copyfile(src, dst)
        print('copy %s' % dst)
    except IOError as ex:
        log.error('%s' % ex)

def copytree(src, dst):
    if os.path.isdir(src):
        if not os.path.exists(dst):
            safe_mkdir(dst)
        for name in os.listdir(src):
            copytree(os.path.join(src, name),
                     os.path.join(dst, name))
    else:
        safe_copy(src, dst)

def main(source, destination):
    for dirname in os.listdir(source):
        src = os.path.join(source, dirname)
        dst = os.path.join(destination, dirname)
        if os.path.isdir(src):
            copytree(src, dst)
        else:
            safe_copy(src, dst)

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    src = source
    dests = destinations.split('\n')
    for dst in dests:
        if dst == '':
            continue        
        main(src, dst)
