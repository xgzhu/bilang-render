import pytest

from bilangrender import render

__author__ = "Xiaoguang Zhu"
__copyright__ = "Xiaoguang Zhu"
__license__ = "MIT"


def test_translate_line_by_line():
    """API Tests v1"""
    assert render("<span>hello</span>", option="translate_line_by_line") == "<span>\n hello\n <br/>\n Bonjour\n</span>\n"

def test_remove_and_reconstruct():
    """API Tests v2"""
    assert render("<span>hello</span>", option="remove_and_reconstruct") == "<span>\n hello\n |\n Bonjour\n</span>\n"

