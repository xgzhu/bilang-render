"""
Solution 1.0
Translate line by line
"""

import logging
_logger = logging.getLogger(__name__)


from bs4 import BeautifulSoup, Tag

STOP_TAGS = ['p']
SKIP_TAGS = ['style', 'footer', 'script', 'img', 'form', 'code', 'br']


class SoupTranslatorV1:
    def __init__(self, soup, target_language, translator):
        self.soup = soup
        self.parTags = []
        self.target_language = target_language
        self.translator = translator

    def handle(self):
        self.handleSoup(self.soup)

    def handleSoup(self, soup):
        _logger.debug("[{}] {}".format(soup.name, soup.string))
        if isinstance(soup, Tag) and soup.name in SKIP_TAGS:
            return
        if isinstance(soup, Tag) and soup.name in STOP_TAGS:
            new_html = self.translate(soup.prettify())
            new_soup = BeautifulSoup(new_html, 'html.parser').find()
            soup.insert_after(new_soup)
            # _logger.debug(" -- trans1")
            return

        if isinstance(soup, Tag):  # 检查节点是否是一个 Tag 对象
            if list(soup.children):  # 如果 soup 有子节点
                self.parTags.append(soup.name)
                child_soups = list(soup.children)  # 固定子节点列表
                for child_soup in child_soups:
                    self.handleSoup(child_soup)
                self.parTags.pop()
            else:
                _logger.debug(f"No children for soup: {soup.name}")
        elif soup.string and soup.string.strip():
            # Create a new fragment containing the text, the <br/> tag, and the translated text
            new_text = soup.string.strip()
            br_tag = self.soup.new_tag("br")
            if 'nav' in self.parTags:
                br_tag = ' | '
            translated_text = self.translate(new_text)

            _logger.debug("Replace w/ {} {} {}".format(new_text, br_tag, translated_text))
            
            # Replace the current soup with these new elements
            soup.replace_with(new_text, br_tag, translated_text)
    
    def translate(self, text):
        return self.translator(text, self.target_language)