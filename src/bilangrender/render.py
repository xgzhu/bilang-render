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
api_key = os.getenv("GOOGLE_API_KEY")

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from bilangrender.skeleton import fib`,
# when using this Python module as a library.


def render(html_content, target_language="fr"):
    """Entry func of render bilang html page
    
    Args:
        html_content (str): HTML content to translate.
        target_language (str): Target language code (e.g., 'fr' for French).
        
    Returns:
        str: Translated HTML content.
    """
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": api_key,
        "q": html_content,
        "target": target_language,
        "format": "html"  # Treat input as HTML
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]["translations"][0]["translatedText"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
