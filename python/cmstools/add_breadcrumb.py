import os
import logging
import datetime
import re
from collections import namedtuple

SEARCH_PATH = 'C:\\[your path]'
FIND_REPLACE = True
LOG_FILENAME = str(datetime.date.today())+'-txtreplace.log'
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log = logging.getLogger(__name__)
log.addHandler(console_handler)
_OK = 0
_ERROR = 1
_NA = 3
_FOUND = 4
FindReplace = namedtuple('FindReplace', 'path find replace action')
PAGE_RE = re.compile('PageId="(?P<id>\w+)"')

def get_id(item, text):
    id = None
    iter = PAGE_RE.finditer(text)
    if not iter:
        return
    for m in iter:
        id = m.group('id')
        if len(id) == 32:
            break
    if not id:
        return None
    rtext = item.replace
    nreplace = rtext.replace('{pageId}', id)
    return FindReplace(item.path, item.find, nreplace, None)
    

FIND_AND_REPLACE_ITEMS = (
#pages with /content.xslt 
FindReplace('/', '''						      </div></div></div><div class="container"><div class="padding"><div class="contentPadding">''',
'''						      </div></div></div><div class="container">
              <rts:BreadcrumbControl runat="server"
                WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
                PageId="{pageId}" /><div class="padding"><div class="contentPadding">''', get_id),
#/content.xslt (1 column layout)
FindReplace('/', '''            <div class="container">
              <div class="padding">
                <div class="contentPadding">''',
'''            <div class="container">
              <xsl:text disable-output-escaping="yes"><![CDATA[
              <rts:BreadcrumbControl runat="server"
                WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
                PageId="]]></xsl:text>
              <xsl:apply-templates select="rts:*/info/pageid" />
              <xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
              <div class="padding">
                <div class="contentPadding">''', None),
#pages with /content2.xslt 
FindReplace('/', '''						      </div></div></div><div class="container"><div class="contentLeftSide"><div class="padding"><div class="contentPadding">''',
'''						      </div></div></div><div class="container">
            <rts:BreadcrumbControl runat="server"
              WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
              PageId="{pageId}" /><div class="contentLeftSide"><div class="padding"><div class="contentPadding">''', get_id),
#/content2.xslt (2 column layout)
FindReplace('/', '''            <div class="container">
                  <div class="contentLeftSide">
                    <div class="padding">
                      <div class="contentPadding">''',
'''            <div class="container">
                  <xsl:text disable-output-escaping="yes"><![CDATA[
                  <rts:BreadcrumbControl runat="server"
                    WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
                    PageId="]]></xsl:text>
                  <xsl:apply-templates select="rts:*/info/pageid" />
                  <xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
                  <div class="contentLeftSide">
                    <div class="padding">
                      <div class="contentPadding">''', None),
#pages with /content3.xslt 
FindReplace('/', '''						      </div></div></div><div class="container"><div class="padding"><div class="contentPadding">''',
'''						      </div></div></div><div class="container">
            <rts:BreadcrumbControl runat="server"
              WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
              PageId="{pageId}" /><div class="padding"><div class="contentPadding">''', get_id),
#/content3.xslt (3 column layout)
FindReplace('/', '''            <div class="container">
                <div class="padding">
                  <div class="contentPadding">''',
'''            <div class="container">
                  <xsl:text disable-output-escaping="yes"><![CDATA[
                  <rts:BreadcrumbControl runat="server"
                    WebSiteId="917e227ce5a944a1b7d9240aca0c3cd2"
                    PageId="]]></xsl:text>
                  <xsl:apply-templates select="rts:*/info/pageid" />
                  <xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
                <div class="padding">
                  <div class="contentPadding">''', None),
#pages with realsites/content2.xslt 
FindReplace('/realsites', '''							</div></div><div class="contentTxtContainer"><div class="contentLeftSide"><div class="padding"><div class="contentPadding">''',
'''							</div></div><div class="contentTxtContainer">
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="{pageId}" /><div class="contentLeftSide"><div class="padding"><div class="contentPadding">''', get_id),
#realsites/content2.xslt (2 column layout)
FindReplace('/realsites', '''					<div class="contentTxtContainer">
						<div class="contentLeftSide">
							<div class="padding">''',
'''					<div class="contentTxtContainer">
						<xsl:text disable-output-escaping="yes"><![CDATA[
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="]]></xsl:text>
						<xsl:apply-templates select="rts:*/info/pageid" />
						<xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
						<div class="contentLeftSide">
							<div class="padding">''', None),
#pages with realsites/content3.xslt
FindReplace('/realsites', '''							</div></div><div class="contentTxtContainer"><div class="padding"><div class="contentPadding">''',
'''							</div></div><div class="contentTxtContainer">
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="{pageId}" /><div class="padding"><div class="contentPadding">''', get_id),
#realsites/content3.xslt (3 column layout)
FindReplace('/realsites', '''					<div class="contentTxtContainer">
						<div class="padding">
							<div class="contentPadding">''',
'''					<div class="contentTxtContainer">
						<xsl:text disable-output-escaping="yes"><![CDATA[
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="]]></xsl:text>
						<xsl:apply-templates select="rts:*/info/pageid" />
						<xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
						<div class="padding">
							<div class="contentPadding">''', None),
#pages with realsites/content4.xslt
FindReplace('/realsites', '''						</div></div><div class="contentTxtContainer"><div class="padding contentGrow"><div class="contentPadding">''',
'''						</div></div><div class="contentTxtContainer">
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="{pageId}" /><div class="padding contentGrow"><div class="contentPadding">''', get_id),
#realsites/content4.xslt (1 column layout)
FindReplace('/realsites', '''					<div class="contentTxtContainer">
						<div class="padding contentGrow">
							<div class="contentPadding">''',
'''					<div class="contentTxtContainer">
						<xsl:text disable-output-escaping="yes"><![CDATA[
						<rts:BreadcrumbControl runat="server"
							WebSiteId="d9b2fc33401a4cdea1a13e8599aafc70"
							PageId="]]></xsl:text>
						<xsl:apply-templates select="rts:*/info/pageid" />
						<xsl:text disable-output-escaping="yes"><![CDATA[" />]]></xsl:text>
						<div class="padding contentGrow">
							<div class="contentPadding">''', None),
)


    
def _print(msg, logFun):
    logFun('%s' % (msg))
    
def _print_debug(msg):
    _print(msg, log.debug)
    
def _print_info(msg):
    _print(msg, log.info)
        
def _print_warn(msg):
    _print(msg, log.warn)

def _print_error(msg):
    _print(msg, log.error)


def find_replace(filepath):  
    result = _NA
    try:
        with open(filepath, 'r+') as f:
            text = f.read()
            ntext = text
            for item in FIND_AND_REPLACE_ITEMS:
                path = item.path.replace('/', os.path.sep)
                path = path.strip(os.path.sep)
                path = os.path.join(SEARCH_PATH, path)
                if filepath.find(path) == -1:
                    #_print_debug(str.format('skip {} {}', filepath, path))
                    continue
                find_text = item.find
                replace_text = item.replace
                action = item.action
                index = ntext.find(find_text)
                if index != -1:
                    result = _FOUND
                    if action:
                        item = action(item, ntext)
                        if item:
                            replace_text = item.replace
                        else:
                            result = _ERROR
                            index = -1
                            continue
                if FIND_REPLACE and index != -1:
                    ntext = ntext.replace(find_text, replace_text)
                elif result == _FOUND:
                    break
            if FIND_REPLACE and result == _FOUND:
                new_filepath = filepath+'.issue-'+str(datetime.date.today())+'.back'
                log.info(new_filepath)
                with open(new_filepath, 'w+') as outf:
                    outf.write(text)
                    outf.flush()
                f.seek(0)
                f.truncate()
                f.write(ntext)
                f.flush()
                result = _OK
    except (IOError, UnicodeDecodeError)as ex:
        log.error('Error: reading file: %s %s' % (filepath, ex))
        result = _ERROR
    return result
        
    
if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    files_count = 0
    checked_count = 0
    updated_count = 0
    for dirpath, dirnames, filenames in os.walk(SEARCH_PATH, topdown=True):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            files_count += 1
            if ext.lower() == '.xslt' or ext.lower() == '.aspx':
                checked_count += 1
                fullpath = os.path.join(dirpath, filename)
                result = find_replace(fullpath)
                if result == _OK or result == _FOUND:
                    updated_count += 1
                elif result == _ERROR:
                    _print_error(fullpath)
    imsg = str.format('Files:{} checked:{} updated:{}',
                      files_count, checked_count, updated_count)
    if not FIND_REPLACE:
        imsg = str.format('Files:{} checked:{} found:{}',
                          files_count, checked_count, updated_count)
    log.info(imsg)
