import os
import logging
import datetime
import re
from xml.parsers import expat

search_path = 'C:\RTS\Webs'
#search_path = 'C:\RTS\Webs\FileLinksWS'

LOG_FILENAME = str(datetime.date.today())+'-reader.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)


class Parser:
    def __init__(self):
        self.current = None
        self.cnode = None        
        self.buffer = u''
        self.p = expat.ParserCreate()
        self.p.buffer_text = True
        self.buffer_size = 256
        self.is_service_host_section = False
        self.p.StartElementHandler = self.start_element
        self.p.EndElementHandler = self.end_element
        self.p.CharacterDataHandler = self.char_data
        self.version = ''
        self.domains = []
    
    def start_element(self, name, attr):
        self.cnode = name
        if name.lower() == u'add':
            if self.is_service_host_section:
                    self.check_domain(name, attr)
                    return                
            assembly = attr.get('assembly')
            part1 = 'RTS.RealCMSComponents'
            if assembly != None and assembly.find(part1) != -1:
                reg = re.compile('RTS.RealCMSComponents, Version=([^,]*),')
                m = reg.search(assembly)
                if m != None:
                    self.version = m.group(1)
        elif name.lower()==u'servicehostingenvironment':
            self.is_service_host_section = True        
            
    def check_domain(self, name, attr):
        d = attr.get('prefix')
        if d != None:
            self.domains.append(d)
            
    def end_element(self, name):
        self.cnode = None
        if name.lower() == u'servicehostingenvironment':
            self.is_service_host_section = False
            self.current = None
        self.buffer = u''

    def char_data(self, data):
        if self.cnode == None:
            return
        self.buffer = u''.join((self.buffer, data))        

    def parse(self, data):
        self.p.Parse(data)

def cms_version(filepath):
    try:
        p = Parser()
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
            p.parse(data)
        return p
    except expat.ExpatError as ex:
        log.error('Error: parsing: %s %s' % (filepath, ex))
        
def _print(path, item, logFun):
    if not item.domains:
        logFun('%s|%s|%s' % (path, '', item.version))
    for domain in item.domains:
        logFun('%s|%s|%s' % (path, domain, item.version))
        
def _print_info(path, item):
    _print(path, item, log.info)
        
def _print_warn(path, item):
    _print(path, item, log.warn)
        
if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    
    for dirpath, dirnames, filenames in os.walk(search_path, topdown=True):
        for filename in filenames:
            if filename.lower() == 'web.config':
    ##            log.info('Web.config file found at:%s' % dirpath)
                fullpath = os.path.join(dirpath, filename)
                result = cms_version(fullpath)
                if result == None:
                        continue
                v = result.version                
                if v == '2.5.1.0':
                    _print_info(fullpath, result)
                else:
                    _print_warn(fullpath, result)
    ##log.info('version(%s): %s' % (v, fullpath))

