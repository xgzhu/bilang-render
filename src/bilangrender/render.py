"""
Solution
"""

import argparse
import logging
import sys
from bilangrender.translate_line_by_line import SoupTranslatorV1
from bilangrender.remove_and_reconstruct import SoupTranslatorV2

from bilangrender import __version__

__author__ = "Xiaoguang Zhu"
__copyright__ = "Xiaoguang Zhu"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


import os
import requests
from bs4 import BeautifulSoup, Tag
api_key = os.getenv("GOOGLE_API_KEY")

def render(html_content, target_language="fr", option="translate_line_by_line"):
    """Entry func of render bilang html page

    Args:
        html_content (str): HTML content to translate.
        target_language (str): Target language code (e.g., 'fr' for French).

    Returns:
        str: Translated HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    translator = None
    if option == "translate_line_by_line":
        translator = SoupTranslatorV1(soup, target_language, translate)    
    elif option == "remove_and_reconstruct":
        translator = SoupTranslatorV2(soup, target_language, translate)
        
    if translator:
        translator.handle()
    else:
        raise Warning("Not Implemented")

    return soup.prettify()


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
    _logger.debug("Translate {} -> {}".format(html_content, response.json()["data"]["translations"][0]["translatedText"]))
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
