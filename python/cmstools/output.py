import os
import logging
import datetime
import re
import reader
from xml.parsers import expat

search_path = 'C:\RTS\Webs'
output = 'output.txt'

LOG_FILENAME = str(datetime.date.today())+'-output.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)


def _output(line):
    with open(output, 'a') as f:
        f.write(line)
        f.flush()
        
def _print(path, item, logFun):
    for domain in item.domains:
        s = 'Get-Content _base2.5Web.config | ForEach-Object {{ $_ -replace "domain.com", "{0}" }} | Set-Content "{1}"'
        r = s.format(domain, path)
        logFun(r)
        _output(r + '\n')
        
                
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
	
    for dirpath, dirnames, filenames in os.walk(search_path, topdown=True):
       for filename in filenames:
            if filename.lower() == 'web.config':
    ##            log.info('Web.config file found at:%s' % dirpath)
                fullpath = os.path.join(dirpath, filename)
                result = reader.cms_version(fullpath)
                if result == None:
                        continue
                v = result.version
                vs = ['2.5.1.0', '2.5.0.0']
                if v not in vs:
                    continue
                _print(fullpath, result, log.info)                


