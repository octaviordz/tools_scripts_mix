# coding: utf8
from __future__ import unicode_literals, division
import os
import logging
import datetime
import re
import cssselect
import tinycss2
import collections

#css_file_path = 'C:\\[your path]'


LOG_FILENAME = str(datetime.date.today())+'-parser.log'
_selector_parse = cssselect.parse

CSS_CLASSES = collections.defaultdict(bool)
CSS_IDS = collections.defaultdict(bool)
CSS_ELEMENT_SELECTORS = collections.defaultdict(list)


def add_class(class_name):
    if not CSS_CLASSES[class_name]:
        CSS_CLASSES[class_name]=True
        #print(class_name)

def add_identifier(identifier):
    if not CSS_IDS[identifier]:
        CSS_IDS[identifier]=True
        #print('id: %s' % identifier)

def add_element(element, rule):
    rules = CSS_IDS[element]
    if not rules:
        rules = [rule]
    else:
        rules.append(rule)
    CSS_ELEMENT_SELECTORS[element]= rules
    

def process_cssselect_comp(cssselector, rule):
    s = cssselector
    #if isinstace(s, cssselect.parser.Selector)
    while s != None:
        if isinstance(s, cssselect.parser.Class):
            #print('%s %s' % (s.class_name, s))
            add_class(s.class_name)
            break
        elif isinstance(s, cssselect.parser.CombinedSelector):
            process_cssselect_comp(s.selector, rule)
            process_cssselect_comp(s.subselector, rule)
            break
        elif isinstance(s, cssselect.parser.Element):
            if s.element:
                #print('%s %s %s' % (s, s.namespace, s.element))
                add_element(s.element, rule)
            break
        elif isinstance(s, cssselect.parser.Hash):
            #print('%s %s %s' % (s.id, s.selector, s))
            add_identifier(s.id)
        #else:
        #    print(type(s))
        #    pass
        s = s.selector

            
def parse_qualified_rule(rule):
    strselector = tinycss2.serializer.serialize(rule.prelude)
    if not strselector:
        return
    try:
        selector = cssselect.parse(strselector)
    except cssselect.SelectorError as ex:
        #log.error('Error: parsing css select: %s %s' % (strselector, ex))
        print('Error: parsing css select: %s %s' % (strselector, ex))
        raise
    for s in selector:
        process_cssselect_comp(s.parsed_tree, rule)


def _consume_rule(first_token, tokens):
    if first_token.type == 'at-keyword':
        #return _consume_at_rule(first_token, tokens)
        return tinycss2.ast.ParseError(
                first_token.source_line, first_token.source_column, 'invalid',
                'EOF reached before {} block for a qualified rule.')
    if first_token.type == '{} block':
        prelude = []
        block = first_token
    else:
        prelude = [first_token]
        for token in tokens:
            if token.type == '{} block':
                block = token
                break
            prelude.append(token)
        else:
            return tinycss2.ast.ParseError(
                prelude[-1].source_line, prelude[-1].source_column, 'invalid',
                'EOF reached before {} block for a qualified rule.')
    return tinycss2.ast.QualifiedRule(first_token.source_line, first_token.source_column,
                         prelude, block.content)
            
def parse_at_rule(rule):
    #print(rule.at_keyword)
    #print(rule.content)
    _tokens = rule.content or ()  
    tokens = iter(_tokens)
    content_rules = [_consume_rule(token, tokens) for token in tokens
            if token.type != 'whitespace']
    process_result_list(content_rules)
        
def process_result_list(result_list):
    for comp in result_list:
        if isinstance(comp, tinycss2.ast.QualifiedRule):
            parse_qualified_rule(comp)
        elif isinstance(comp, tinycss2.ast.AtRule):
            parse_at_rule(comp)
        elif  isinstance(comp, tinycss2.ast.ParseError):
            print('ParseError: %s %s' % (comp.message, comp.kind))
        else:
            print('Unknown: %s' % comp)
            

def main(filepath):
    open_mode = 'r'
    try:
        with open(filepath, open_mode) as f:
            text = f.read()
            result_list = tinycss2.parse_stylesheet(text)
            process_result_list(result_list)
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
    
