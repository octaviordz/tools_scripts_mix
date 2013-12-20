# coding: utf8
import os
import logging
import datetime
import re
import tinycss
import collections

#css_file_path = 'C:\\[your path]'


LOG_FILENAME = str(datetime.date.today())+'-tokenizer.log'

def _print(path, logFun):    
    logFun('%s' % (path))
        
def _print_info(path):
    _print(path, log.info)
        
def _print_warn(path):    
    _print(path, log.warn)

def _print_error(path):
    _print(path, log.error)

def tokenize(css_source):
    #tinycss.tokenizer.tokenize_flat(css_source, False)
    tokens = tinycss.tokenizer.tokenize_flat(css_source, True)    
    print(len(tokens))
    return tokens

def main(filepath):
    open_mode = 'r'
    try:
        with open(filepath, open_mode) as f:
            text = f.read()
            result = tokenize(text)
    except (IOError, UnicodeDecodeError)as ex:
        log.error('Error: reading file: %s %s' % (filepath, ex))
        raise
        
if __name__ == '__main__':
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log = logging.getLogger(__name__)
    log.addHandler(console_handler)
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    main(css_file_path)
    
