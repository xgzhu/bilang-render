"""
Solution 2.0
1. remove unnecessary tags and attributions
2. translate
3. reconstruct
"""


import logging
_logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup, Tag, NavigableString

import copy

STOP_TAGS = ['p','a']
SKIP_TAGS = ['style', 'footer', 'script', 'img', 'form', 'code', 'br']


class SoupTranslatorV2:
    def __init__(self, soup, target_language, translate):
        self.soup = soup
        self.target_language = target_language
        self.translate = translate

    def handle(self):
        soup_preprocess = copy.copy(self.soup)
        self.clean_attributes(soup_preprocess)
        self.removeEmptyElements(soup_preprocess, self.soup)
        translated_text = self.translate(str(self.soup), self.target_language)
        soup_t = BeautifulSoup(translated_text, 'html.parser') ## be careful, whether to remove a wrap.
        self.reconstructElements(self.soup, soup_t)

    def removeEmptyElements(self, soup, soup_c):
        if isinstance(soup, Tag):
            if soup.name in SKIP_TAGS:
                soup.decompose()
                return True

            # 使用列表来避免在迭代时修改元素
            children = list(soup.children)
            children_c = list(soup_c.children)
            for idx, child in enumerate(children):
                child_c = children_c[idx]
                if self.removeEmptyElements(child, child_c):
                    # 如果是Tag且确定要移除，则直接用decompose()
                    if isinstance(child, Tag):
                        child.decompose()
                        child_c['bilangRemove'] = 'YES'

            # 如果当前标签无内容且无文本，则标记为可移除
            if not soup.contents and (soup.string is None or not soup.string.strip()):
                return True
            return False
        elif isinstance(soup, NavigableString):
            if not soup.string.strip():
                soup.extract()  # 移除空白的NavigableString
                return True
            return False

    def reconstructElements(self, soup, soup_t):
        if isinstance(soup, Tag):
            if soup.name in SKIP_TAGS:
                return

            _logger.debug("[{} <> {}] {} <> {}".format(soup.name, soup_t.name, self.getAllText(soup), self.getAllText(soup_t)))
            if soup_t.name  != soup.name:
                _logger.debug("  *** {} <> {}".format(str(soup), str(soup_t)))
                return

            if soup.name in STOP_TAGS:
                copied_element = copy.copy(soup_t)
                soup.append(copied_element)
                return
            
            # 使用列表来避免在迭代时修改元素
            children = list(soup.children)
            children_t = list(soup_t.children)
            idx_t = 0
            while idx_t < len(children_t) and (isinstance(children_t[idx_t], NavigableString) and children_t[idx_t].string.strip() is None):
                idx_t += 1
                _logger.debug(" ### calibrate idx_t to {}/{}, ".format(idx_t, len(children_t)))
            for _, child in enumerate(children):
                # if child['bilangRemove'] == 'YES':
                if isinstance(child, Tag) and 'bilangRemove' in child.attrs and child['bilangRemove'] == 'YES':
                    continue
                if isinstance(child, NavigableString) and not child.string.strip():
                    continue
                if isinstance(child, Tag) and child.name in SKIP_TAGS:
                    continue
                
                if idx_t >= len(children_t):
                    break
                    
                self.reconstructElements(child, children_t[idx_t])
                idx_t += 1
                while idx_t < len(children_t) and (children_t[idx_t].name == None or (isinstance(children_t[idx_t], NavigableString) and children_t[idx_t].string.strip() is None)):
                    idx_t += 1

        elif isinstance(soup, NavigableString):
            if soup_t.string:
                _logger.debug("  >>> {} + {}".format(soup.string.strip(), soup_t.string.strip()))
                soup.replace_with(soup.string.strip(), ' | ', soup_t.string.strip())
            elif soup.string.strip():
                _logger.debug("  *** MISSING {}".format(soup.string.strip()))

    ## static funcs
    def clean_attributes(self, soup):
        for tag in soup.find_all(True):
            tag.attrs = {}

    def getAllText(self, soup):
        if isinstance(soup, NavigableString):
            return soup.string.strip()
        rtn = ""
        if isinstance(soup, Tag):
            children = list(soup.children)
            for child in children:
                if isinstance(child, NavigableString):
                    rtn = rtn +  child.string.strip()
        return rtn

