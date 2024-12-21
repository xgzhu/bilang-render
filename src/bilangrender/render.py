"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = bilangrender.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from bilangrender import __version__

__author__ = "Xiaoguang Zhu"
__copyright__ = "Xiaoguang Zhu"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


import os
import requests
from bs4 import BeautifulSoup, Tag
api_key = os.getenv("GOOGLE_API_KEY")

def render(html_content, target_language="fr"):
    """Entry func of render bilang html page

    Args:
        html_content (str): HTML content to translate.
        target_language (str): Target language code (e.g., 'fr' for French).

    Returns:
        str: Translated HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    attributions = {'soup':soup,'parTags':[]}
    handleNode(body, attributions, target_language)

    return soup.prettify()


STOP_TAGS = ['p']
SKIP_TAGS = ['style','footer','script','img','form']

def handleNode(node, attributions, target_language):
    print("[{}] {}".format(node.name, node.string))
    if isinstance(node, Tag) and node.name in SKIP_TAGS:
        return
    if isinstance(node, Tag) and node.name in STOP_TAGS:
        new_html = translate(node.prettify(), target_language)
        new_node = BeautifulSoup(new_html, 'html.parser').find()
        node.insert_after(new_node)
        # print(" -- trans1")
        return

    if isinstance(node, Tag):  # 检查节点是否是一个 Tag 对象
        if list(node.children):  # 如果 node 有子节点
            attributions['parTags'].append(node.name)
            child_nodes = list(node.children)  # 固定子节点列表
            for child_node in child_nodes:
                handleNode(child_node, attributions, target_language)
            attributions['parTags'].pop()
        else:
            print(f"No children for node: {node.name}")
    elif node.string and node.string.strip():
        # Create a new fragment containing the text, the <br/> tag, and the translated text
        new_text = node.string.strip()
        br_tag = attributions['soup'].new_tag("br")
        if 'nav' in attributions['parTags']:
            br_tag = ' | '
        translated_text = translate(new_text, target_language)
        
        # Replace the current node with these new elements
        node.replace_with(new_text, br_tag, translated_text)
        print(" -- trans2", new_text)


def translate(html_content, target_language="fr"):
    """
    Translates HTML content using Google Cloud Translation API.

    Args:
        api_key (str): Your Google Cloud API key.
        html_content (str): HTML content to translate.
        target_language (str): Target language code (e.g., 'fr' for French).

    Returns:
        str: Translated HTML content.
    """
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "q": html_content,
        "source": "en",
        "target": target_language,
        "format": "html"  # Treat input as HTML
    }
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    response = requests.post(url, headers=headers, json=data)  # Attach API key directly to the URL
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
