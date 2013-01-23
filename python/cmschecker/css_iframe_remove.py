import os
import logging
import datetime
import re
import tinycss

search_path = 'C:\\RTS\\Webs'
#search_path = 'C:\\Users\\orc\\Documents\\Projects\\RealCMS.git\\Website'
REMOVE_ISSUE = True

LOG_FILENAME = str(datetime.date.today())+'-css.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)

class EndMark:
    def __init__(self, end_line, end_column):
        self.end_line = end_line
        self.end_column = end_column
    @property
    def line(self):
        pass
    @property
    def column(self):
        pass
        
class EndToken(EndMark):
    def __init__(self, end_line, end_column, tinycss_token):
        super(EndToken, self).__init__(end_line, end_column)
        self.tinycss_token = tinycss_token
    @property
    def line(self):
        return self.tinycss_token.line
    @property
    def column(self):
        return self.tinycss_token.column
        
class RuleEndToken(EndMark):
    def __init__(self, end_line, end_column, tinycss_rule):
        super(RuleEndToken, self).__init__(end_line, end_column)
        self.tinycss_rule = tinycss_rule
    @property
    def line(self):
        return self.tinycss_rule.line
    @property
    def column(self):
        return self.tinycss_rule.column
        

def find_rule_end(lines, line, column):    
    for linen in range(line, len(lines)+1):
        line_text = lines[linen-1]
        for columnn in range(column, len(line_text)+1):
            c = line_text[columnn-1]
            if c == '}':
                return (linen, columnn)
    return None
def new_text(text, lines, remove_list):
    result = []
    def remove_token(token, line, column):
        if line > token.end_line or (line == token.end_line and
                                     column >= token.end_column):
            remove_list.remove(token)
    def is_remove(line, column, char):
        if not remove_list:
            return False
        token = remove_list[0]
        #print('search:{},{}  token:{},{}, {}, {}'.format(
        #    line, column, token.line, token.column, token.end_line,
        #    token.end_column))
        between_lines = line >= token.line  and line <= token.end_line
        is_start_line = line == token.line
        is_end_line = line == token.end_line
        between_columns = column >= token.column and column <= token.end_column
        if between_lines:            
            if is_start_line and is_end_line:
                remove_token(token, line, column)
                return between_columns                            
            elif is_start_line:
                remove_token(token, line, column)
                return token.end_line > token.line
            elif is_end_line:
                remove_token(token, line, column)
                return column <= token.end_column
        remove_token(token, line, column)
        return False
    for linen in range(1, len(lines)+1):
        line_text = lines[linen-1]
        for columnn in range(1, len(line_text)+1):
            char = line_text[columnn-1]
            if not is_remove(linen, columnn, char):
                result.append(char)
            #else:
            #    print('i({0}, {1}):{2}'.format(linen, columnn, char))
        result.append('\n')
    return ''.join(result)
            
def check_iframe_problem(filepath, remove = False):
    removelist = []
    def _width(rule, declaration):
        if declaration.name == 'width':
            for token in declaration.value:
                if token.as_css() == '100%':
                    return True
        return False
    
    def _height(rule, declaration):
        if declaration.name == 'height':
            for token in declaration.value:
                if token.as_css() == '100px':
                    return True
        return False
    
    def is_issue(rule, declaration):
        widthissue = _width(rule, declaration)
        heightissue = _height(rule, declaration)
        return widthissue or heightissue
    
    def parse(text, lines):
        result = 'ok'
        #try:            
        p = tinycss.make_parser('page3')            
        stylesheet = p.parse_stylesheet(text)            
        for rule in stylesheet.rules:
            if rule.at_keyword != None:
                continue
            if rule.selector.as_css() == 'iframe':                    
                result = 'warn'
                declist = rule.declarations[:]
                #print([d.name for d in rule.declarations])
                for declaration in rule.declarations:
                    isissue = is_issue(rule, declaration)
                    if isissue:
                        result = 'error'
                    else:
                        declist.remove(declaration)
                if declist and len(rule.declarations) > len(declist):
                    #if there are delcarations that are not issues
                    #we don't remove the whole rule
                    for d in declist:
                        v = d.value[-1]
                        line = v.line
                        column = v.column + len(v.as_css())
                        print('value ' + v.as_css())
                        #print(line, d.column, column)
                        removelist.append(EndToken(line, column, d))
                else:
                    last = rule.declarations[-1]
                    end = find_rule_end(lines, last.line, last.column)
                    if end:
                        #print(end)
                        line, column = end
                        removelist.append(RuleEndToken(line, column, rule))
                    else:
                        raise ValueError()
        #except tinycss.parsing.ParseError as ex:
        #    log.warn('Error: parsing: %s %s' % (filepath, ex))
        #finally:
        return result
    
    with open(filepath, 'r+', encoding='utf-8') as f:
        text = f.read()
        lines = text.split('\n')
        result = parse(text, lines)
        if result != 'ok' and remove:
            ntext = new_text(text, lines, removelist)
            f.seek(0)
            f.truncate()
            f.write(ntext)
            f.flush()
            newfilepath = filepath+'.iframe-issue-'+str(datetime.date.today())
            print(newfilepath)
            with open(newfilepath, 'w+', encoding='utf-8') as f:
                f.write(text)
                f.flush()
    return result
        
def _print(path, logFun):    
    logFun('%s' % (path))
        
def _print_info(path):
    _print(path, log.info)
        
def _print_warn(path):    
    _print(path, log.warn)

def _print_error(path):
    _print(path, log.error)    
        
if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)    
    for dirpath, dirnames, filenames in os.walk(search_path, topdown=True):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext.lower() == '.css':
                #log.info('CSS file found at:%s' % dirpath)
                fullpath = os.path.join(dirpath, filename)
                result = check_iframe_problem(fullpath, REMOVE_ISSUE)
                if result == 'error':
                    _print_error(fullpath)
                elif result == 'warn':
                    _print_warn(fullpath)
