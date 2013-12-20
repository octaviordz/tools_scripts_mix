# coding: utf8
import os
import logging
import datetime
import re
import collections
import tinycss2
import csv
import imp
parser_module = imp.find_module('parser', ['.\\'])
parser = imp.load_module('parser', *parser_module) 

#CSS_FILE_PATH = 'C:\\[your path]'
#JS_FILE_PATH = 'C:\\[your path]'
TEMPLATES_PATH = 'C:\\[your path]'


CSS_CLASS_REALM = 'rc-admin-realm'
CSS_CLASS_PREFIX = 'rc-admin-'
CSS_ELEMENT_CSS_CLASS= 'rc-admin'
_PERFORM_UPDATE = True
_UPDATE_ELEMENT_SELECTORS = False
_UPDATE_JS = False

LOG_FILENAME = str(datetime.date.today())+'-css.log'


TaskResult = collections.namedtuple('TaskResult', ('status', 'update_count'))
    
class Token:
    def __init__(self, line, column, tinycss_token):
        self._line = line
        self._column = column
        self.tinycss_token = tinycss_token
    @property
    def line(self):
        return self.tinycss_token.line
    @property
    def column(self):
        return self.tinycss_token.column


def check_file(filepath, process_fun, update_fun, update = False):
    update_count = 0
    status = 'ok'
    open_mode = 'r+'
    if not update:
        open_mode = 'r'
    try:
        with open(filepath, open_mode) as f:
            text = f.read()
            result = process_fun(text)
            if update:
                ntext = update_fun(text, result)
                #TODO:save backup
                #backup_file = filepath+'.issue-'+str(datetime.date.today())+'.back'
                #with open(backup_file, 'w+') as outf:
                #    outf.write(text)
                #    outf.flush()
                f.seek(0)
                f.truncate()
                f.write(ntext)
                f.flush()
    except (IOError, UnicodeDecodeError) as ex:
        log.error('Error: reading file: %s %s' % (filepath, ex))
        raise
    return TaskResult(status, update_count)


def replace_func_css_class(match):
        mgroup = match.group(0)
        css_class = match.group(1)
        diff = mgroup.replace(css_class, '', 1)
        css_class = css_class.strip('.')        
        new_class = ''.join(['.', CSS_CLASS_PREFIX, css_class, diff])
        return new_class
    
def replace_func_css_element(match):
        mgroup = match.group(0)
        element = match.group(1)
        diff = mgroup.replace(element, '', 1)
        new_selector = ''.join([element, '.', CSS_ELEMENT_CSS_CLASS, diff])
        return new_selector
    
def replace_text_css(text, css_classes, css_element_selectors, css_ids):
    #TODO: realm = ''.join(['.', CSS_CLASS_REALM])    
    for css_class in css_classes:
        prefindex = css_class.find(CSS_CLASS_PREFIX)
        if prefindex != -1:
            continue
        regex = ''.join([r'(\.', css_class, r')([^-;\w])'])
        #new_class = ''.join(['.', CSS_CLASS_PREFIX, css_class])
        #print('"%s"  %s' % (new_class, regex))
        text = re.sub(regex, replace_func_css_class, text)
    #TODO:double replace 
    #input.rc-admin-span11,    
    #input.rc-admin.rc-admin-span11,
    if _UPDATE_ELEMENT_SELECTORS:
        for element_selector in css_element_selectors:
            pefindex = element_selector.find(CSS_ELEMENT_CSS_CLASS)
            if pefindex == 0 or pefindex == 1:
                continue
            regex = ''.join([r'\b(', element_selector, r'\b)[^\.-:;\w]'])
            #new_selector = ''.join([element_selector, '.', CSS_ELEMENT_CSS_CLASS])
            #print('"%s"  %s' % (new_selector, regex))
            text = re.sub(regex, replace_func_css_element, text)
    #for css_id in css_ids:
    #    newId = 
    #    text.replace(''.join('#',css_id), newId)
    return text


def check_css_file(filepath, should_update = False):
    def process(text):
        result_list = tinycss2.parse_stylesheet(text)
        parser.process_result_list(result_list)
        rename_list = []
        for css_class in parser.CSS_CLASSES:
            old = css_class.lstrip('.')
            new = ''.join([CSS_CLASS_PREFIX, old]) 
            rename_list.append((old, new))
        with open('rename_list.csv', 'wb') as f:
            wr=csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerows(rename_list)
        return result_list
    def update(text, processed):
        result_list = processed
        parser.process_result_list(result_list)
        ntext = replace_text_css(
             text,
             parser.CSS_CLASSES, 
             parser.CSS_ELEMENT_SELECTORS, 
             parser.CSS_IDS,
             )
        return ntext
    return check_file(filepath, process, update, should_update)

    
def replace_text_js(text, rename_list):
    for old, new in rename_list:
        regex = ''.join([r'\b', old, r'\b'])
        text = re.sub(regex, new, text)
    return text


def check_js_file(filepath, update = False):
    def process(text):
        rename_list = []
        for css_class in parser.CSS_CLASSES:
            old = css_class.lstrip('.')
            new = ''.join([CSS_CLASS_PREFIX, old]) 
            rename_list.append((old, new))
        return rename_list
    def update(text, processed):
        rename_list = processed        
        ntext = replace_text_js(
             text,
             rename_list
             )
        return ntext
    return check_file(filepath, process, update, update)


def replace_text_template(text, rename_list):
    def repl_fun(match):
        mgroup = match.group(0)
        css_class = match.group(1)
        diff = mgroup.replace(css_class, '', 1)
        result = ''.join([new, diff])
        return result
    for old, new in rename_list:
        #regex = ''.join([r'(\b', old, r')([^-\.:;\w]|\b)'])
        regex = ''.join([r'(?<![-_\w])(', old, r')(?![-_\w])'])
        text = re.sub(regex, repl_fun, text)
    return text

def check_template_file(filepath, rename_list, update = False):
    def process(text):
        return None
    def update(text, processed):
        ntext = replace_text_template(
             text,
             rename_list
             )
        return ntext    
    return check_file(filepath, process, update, update)


def check_template_files(path, update = False):
    rename_list = []
    with open('rename_list.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            rename_list.append(row)    
    
    for dirpath, _dirnames, filenames in os.walk(path, True):
        for filename in filenames:
            fpath = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1]
            if ext == '.html':
                check_template_file(fpath, rename_list) 
    

def _print(path, logFun):
    logFun('%s' % (path))
        
def _print_info(path):
    _print(path, log.info)
        
def _print_warn(path):    
    _print(path, log.warn)

def _print_error(path):
    _print(path, log.error)    
        
if __name__ == '__main__':
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log = logging.getLogger(__name__)
    log.addHandler(console_handler)
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    #check_css_file(CSS_FILE_PATH, _PERFORM_UPDATE)
    check_template_files(TEMPLATES_PATH, _PERFORM_UPDATE)
    #check_template_files(JS_FILE_PATH, _UPDATE_JS)    
    #log.info(str.format(
    #    'File checked:{} selectors modified:{}',
    #    css_file_path,
    #    update_count)
    #)
